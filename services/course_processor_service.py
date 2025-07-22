# services/course_processor_service.py

import os
import json
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn

from utils.database import get_db_connection
from utils.logger import logger
from services.video_service import process_course_videos_to_audio
from services.transcription_service import transcribe_audio
from services.ai_service import generate_summary_claude
from services.audio_service import create_unified_audio, generate_timestamps
from services.tts_service import generate_tts_audio
from services.gdrive_service import upload_file_to_drive
from services.rss_service import update_rss_feed
from services.github_service import update_github_repo

console = Console()

def create_progress_bar(description: str = "Processing"):
    """Cria barra de progresso padrão"""
    return Progress(
        SpinnerColumn(),
        TextColumn("[bold bright_blue]{task.description}[/]"),
        BarColumn(bar_width=40, style="bright_blue", complete_style="bright_green"),
        TaskProgressColumn(),
        console=console,
        transient=False
    )

def _update_course_status(course_id: int, status: str, stage: str = None, metadata: dict = None):
    """Atualiza o status e o estágio de processamento de um curso no DB."""
    conn = get_db_connection()
    cursor = conn.cursor()
    update_sql = "UPDATE courses SET status = ?" 
    params = [status]
    if stage:
        update_sql += ", processing_stage = ?"
        params.append(stage)
    if metadata:
        update_sql += ", metadata_json = ?"
        params.append(json.dumps(metadata))
    update_sql += " WHERE id = ?"
    params.append(course_id)
    cursor.execute(update_sql, tuple(params))
    conn.commit()
    conn.close()
    logger.info(f"Course {course_id} status updated to {status} at stage {stage if stage else 'N/A'}.")

def _log_operation(course_id: int, op_type: str, status: str, error_msg: str = None, details: dict = None):
    """Registra uma operação no DB."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO operations (course_id, operation_type, status, error_message, details_json) VALUES (?, ?, ?, ?, ?)",
        (course_id, op_type, status, error_msg, json.dumps(details) if details else None)
    )
    conn.commit()
    conn.close()
    if status == "success":
        logger.info(f"Operation {op_type} for course {course_id} completed successfully.")
    else:
        logger.error(f"Operation {op_type} for course {course_id} failed: {error_msg}")

def process_complete_course(course_name: str, course_directory: str, output_base_directory: str):
    """Orquestra o processamento completo de um curso."""
    logger.info(f"Starting full course processing for: {course_name}")
    console.print(f"\n[bold bright_blue]Starting full course processing for: {course_name}[/]")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO courses (name, directory_path, status, processing_stage) VALUES (?, ?, ?, ?)",
                   (course_name, course_directory, "in_progress", "discovery"))
    course_id = cursor.lastrowid
    conn.commit()
    conn.close()

    course_metadata = {"audio_files": [], "transcription": None, "summary": None, "unified_audio": None, "timestamps": None, "gdrive_id": None}

    steps = [
        {"name": "Video to Audio Conversion", "func": process_course_videos_to_audio, "args": (course_directory, os.path.join(output_base_directory, course_name, "audios")), "stage": "converting_audio"},
        {"name": "Audio Transcription", "func": transcribe_audio, "args": (None,), "stage": "transcribing"}, # Audio path will be dynamic
        {"name": "AI Summary Generation", "func": generate_summary_claude, "args": (None, "summary_test"), "stage": "summarizing"}, # Transcription and prompt dynamic
        {"name": "Audio Unification", "func": create_unified_audio, "args": (None, os.path.join(output_base_directory, course_name, f"{course_name}.mp3")), "stage": "unifying_audio"},
        {"name": "Timestamp Generation", "func": generate_timestamps, "args": (None,), "stage": "generating_timestamps"}, # Audio path dynamic
        {"name": "Google Drive Upload", "func": upload_file_to_drive, "args": (None,), "stage": "uploading_gdrive"}, # File path dynamic
        {"name": "RSS Feed Update", "func": update_rss_feed, "args": (None,), "stage": "updating_rss"}, # Course data dynamic
        {"name": "GitHub Repository Update", "func": update_github_repo, "args": (f"Add {course_name} podcast"), "stage": "updating_github"},
    ]

    with create_progress_bar("Overall Course Processing") as overall_progress:
        overall_task = overall_progress.add_task("Processing...", total=len(steps))

        for i, step in enumerate(steps):
            overall_progress.update(overall_task, description=f"Step {i+1}/{len(steps)}: [bold]{step['name']}[/]")
            _update_course_status(course_id, "in_progress", step['stage'])
            
            success = False
            message = ""

            if step['name'] == "Video to Audio Conversion":
                success, message = step['func'](*step['args'], progress=overall_progress, task_id=overall_task)
                if success:
                    # Aqui, precisaríamos de uma forma de obter os caminhos dos áudios gerados
                    # Por enquanto, vamos simular que eles estão em output_base_directory/course_name/audios
                    audio_output_dir = os.path.join(output_base_directory, course_name, "audios")
                    course_metadata["audio_files"] = [os.path.join(audio_output_dir, f) for f in os.listdir(audio_output_dir) if f.endswith(".mp3")]

            elif step['name'] == "Audio Transcription":
                if course_metadata["audio_files"]:
                    # Transcreve o primeiro áudio para simplificar, ou todos e concatena
                    success, transcription_text = transcribe_audio(course_metadata["audio_files"][0], progress=overall_progress, task_id=overall_task)
                    if success:
                        course_metadata["transcription"] = transcription_text
                        # Salvar transcrição em arquivo
                        transcription_file = os.path.join(output_base_directory, course_name, "transcription.txt")
                        with open(transcription_file, "w", encoding="utf-8") as f: f.write(transcription_text)
                        message = transcription_file
                else:
                    success, message = False, "No audio files to transcribe."

            elif step['name'] == "AI Summary Generation":
                if course_metadata["transcription"]:
                    success, summary_text = generate_summary_claude(course_metadata["transcription"], step['args'][1], progress=overall_progress, task_id=overall_task)
                    if success:
                        course_metadata["summary"] = summary_text
                        # Salvar resumo em arquivo
                        summary_file = os.path.join(output_base_directory, course_name, "summary.md")
                        with open(summary_file, "w", encoding="utf-8") as f: f.write(summary_text)
                        message = summary_file
                else:
                    success, message = False, "No transcription to summarize."

            elif step['name'] == "Audio Unification":
                if course_metadata["audio_files"]:
                    success, unified_audio_path = create_unified_audio(course_metadata["audio_files"], step['args'][1], progress=overall_progress, task_id=overall_task)
                    if success:
                        course_metadata["unified_audio"] = unified_audio_path
                        message = unified_audio_path
                else:
                    success, message = False, "No audio files to unify."

            elif step['name'] == "Timestamp Generation":
                if course_metadata["unified_audio"]:
                    success, timestamps_text = generate_timestamps(course_metadata["unified_audio"], progress=overall_progress, task_id=overall_task)
                    if success:
                        course_metadata["timestamps"] = timestamps_text
                        # Salvar timestamps em arquivo
                        timestamps_file = os.path.join(output_base_directory, course_name, "timestamps.txt")
                        with open(timestamps_file, "w", encoding="utf-8") as f: f.write(timestamps_text)
                        message = timestamps_file
                else:
                    success, message = False, "No unified audio for timestamps."

            elif step['name'] == "Google Drive Upload":
                if course_metadata["unified_audio"]:
                    success, gdrive_id = upload_file_to_drive(course_metadata["unified_audio"], progress=overall_progress, task_id=overall_task)
                    if success:
                        course_metadata["gdrive_id"] = gdrive_id
                        message = gdrive_id
                else:
                    success, message = False, "No unified audio to upload."

            elif step['name'] == "RSS Feed Update":
                if course_metadata["unified_audio"] and course_metadata["summary"]:
                    # Dados dummy para o RSS, precisaríamos de dados reais do curso
                    rss_data = {
                        'title': course_name,
                        'link': "https://example.com/" + os.path.basename(course_metadata["unified_audio"]), # Link temporário
                        'guid': course_name + "-" + str(datetime.now().timestamp()),
                        'description': course_metadata["summary"],
                        'enclosure_url': "https://example.com/" + os.path.basename(course_metadata["unified_audio"]), # Link temporário
                        'enclosure_length': str(os.path.getsize(course_metadata["unified_audio"])) if os.path.exists(course_metadata["unified_audio"]) else "0",
                        'duration': "00:00:00", # Precisa calcular a duração real
                        'author': "NeuroDeamon",
                    }
                    success, message = update_rss_feed(rss_data, progress=overall_progress, task_id=overall_task)
                else:
                    success, message = False, "Missing unified audio or summary for RSS update."

            elif step['name'] == "GitHub Repository Update":
                success, message = update_github_repo(step['args'][0], progress=overall_progress, task_id=overall_task)

            if success:
                _log_operation(course_id, step['name'], "success", details={'message': message})
                overall_progress.update(overall_task, advance=1)
            else:
                _log_operation(course_id, step['name'], "failed", error_msg=message)
                console.print(f"[bright_red]✗ Step '{step['name']}' failed: {message}[/]")
                _update_course_status(course_id, "failed", step['stage'], course_metadata)
                return False # Para o processamento se uma etapa falhar

    _update_course_status(course_id, "completed", "finished", course_metadata)
    logger.info(f"Full course processing completed for: {course_name}")
    console.print(f"\n[bold bright_green]✅ Full course processing completed for: {course_name}[/]")
    return True

# Exemplo de uso (para testes)
if __name__ == "__main__":
    # Para testar, você precisaria de:
    # 1. Um diretório de curso com vídeos (ex: test_course/video.mp4)
    # 2. Chaves de API configuradas em config/api_keys.json
    # 3. credentials.json para Google Drive
    # 4. Um repositório Git inicializado em github/neurodeamon-feeds

    test_course_name = "MyTestCourse"
    test_course_dir = "./test_course_videos"
    test_output_dir = "./processed_courses"

    # Criar diretório de teste e um vídeo dummy
    os.makedirs(test_course_dir, exist_ok=True)
    # with open(os.path.join(test_course_dir, "intro.mp4"), "w") as f: f.write("dummy video content")

    # Crie um prompt de exemplo em prompts/course_processor/summary_test.md
    # Conteúdo: "Summarize the following transcription: {{TRANSCRIPTION}}"
    os.makedirs(os.path.join("prompts", "course_processor"), exist_ok=True)
    with open(os.path.join("prompts", "course_processor", "summary_test.md"), "w", encoding="utf-8") as f:
        f.write("Summarize the following transcription: {{TRANSCRIPTION}}")

    # Execute o processamento completo
    # process_complete_course(test_course_name, test_course_dir, test_output_dir)

    console.print("Para testar o fluxo completo, descomente a chamada da função process_complete_course e configure os pré-requisitos.")
