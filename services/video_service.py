# services/video_service.py

import os
import subprocess
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn

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

def convert_video_to_audio(video_path: str, output_audio_path: str, progress: Progress = None, task_id = None):
    """Converte um arquivo de vídeo para MP3 128kbps usando ffmpeg."""
    command = [
        "ffmpeg",
        "-i", video_path,
        "-vn",  # No video
        "-ar", "44100",  # Audio sample rate
        "-acodec", "libmp3lame",  # MP3 codec
        "-b:a", "128k",  # Audio bitrate
        output_audio_path
    ]

    try:
        # Cria o diretório de saída se não existir
        os.makedirs(os.path.dirname(output_audio_path), exist_ok=True)

        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
        
        # Simula progresso (ffmpeg não dá progresso fácil para stdout/stderr)
        if progress and task_id is not None:
            progress.update(task_id, description=f"Converting [bright_white]{os.path.basename(video_path)}[/]...")
            # Para uma barra de progresso mais precisa, precisaríamos parsear a saída do ffmpeg
            # Por enquanto, uma simulação simples ou um spinner é suficiente.
            # A barra de progresso será atualizada pelo chamador se for uma operação longa.
            progress.update(task_id, advance=100) # Completa a tarefa imediatamente para este exemplo

        stdout, stderr = process.communicate()

        if process.returncode != 0:
            raise Exception(f"FFmpeg error: {stdout}")

        console.print(f"[bright_green]✓ Converted: {os.path.basename(video_path)}[/]")
        return True
    except FileNotFoundError:
        console.print("[bright_red]✗ Error: ffmpeg not found. Please install ffmpeg and add it to your PATH.[/]")
        return False
    except Exception as e:
        console.print(f"[bright_red]✗ Error converting {os.path.basename(video_path)}: {e}[/]")
        return False

def process_course_videos_to_audio(course_directory: str, output_base_directory: str):
    """Processa todos os vídeos em um diretório de curso para áudio, mantendo a hierarquia."""
    video_extensions = (".mp4", ".avi", ".mkv", ".mov")
    processed_count = 0
    total_videos = 0

    # Contar total de vídeos para a barra de progresso
    for root, _, files in os.walk(course_directory):
        for file in files:
            if file.lower().endswith(video_extensions):
                total_videos += 1

    if total_videos == 0:
        console.print(f"[bright_yellow]No videos found in {course_directory}[/]")
        return

    with create_progress_bar("Converting videos to audio") as progress:
        main_task = progress.add_task("Overall Progress", total=total_videos)

        for root, _, files in os.walk(course_directory):
            for file in files:
                if file.lower().endswith(video_extensions):
                    video_path = os.path.join(root, file)
                    
                    # Calcula o caminho relativo para manter a hierarquia
                    relative_path = os.path.relpath(video_path, course_directory)
                    output_sub_dir = os.path.dirname(relative_path)
                    output_filename = os.path.splitext(os.path.basename(file))[0] + ".mp3"
                    
                    output_audio_path = os.path.join(output_base_directory, output_sub_dir, output_filename)

                    if convert_video_to_audio(video_path, output_audio_path, progress, main_task):
                        processed_count += 1
                    progress.update(main_task, advance=1)

        progress.update(main_task, completed=total_videos, description="Conversion Complete")
        console.print(f"\n[bright_green]✅ Finished converting {processed_count} of {total_videos} videos to audio.[/]")

# Exemplo de uso (para testes)
if __name__ == "__main__":
    # Crie um diretório de teste com alguns vídeos para testar
    # Ex: test_course/lesson1/video1.mp4
    #     test_course/lesson2/video2.mov
    test_course_dir = "./test_course"
    test_output_dir = "./output_audio"
    
    # Crie alguns arquivos dummy para simular vídeos
    os.makedirs(os.path.join(test_course_dir, "lesson1"), exist_ok=True)
    os.makedirs(os.path.join(test_course_dir, "lesson2"), exist_ok=True)
    with open(os.path.join(test_course_dir, "lesson1", "video1.mp4"), "w") as f: f.write("dummy video content")
    with open(os.path.join(test_course_dir, "lesson2", "video2.mov"), "w") as f: f.write("dummy video content")

    console.print(f"[bold bright_blue]Starting video to audio conversion for {test_course_dir}[/]")
    process_course_videos_to_audio(test_course_dir, test_output_dir)
    console.print(f"[bold bright_blue]Output saved to {test_output_dir}[/]")

    # Limpar arquivos dummy
    # import shutil
    # shutil.rmtree(test_course_dir)
    # shutil.rmtree(test_output_dir)