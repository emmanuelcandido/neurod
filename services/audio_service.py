# services/audio_service.py

import os
from pydub import AudioSegment
from rich.console import Console
from rich.progress import Progress

console = Console()

def create_unified_audio(audio_files: list[str], output_path: str, progress: Progress = None, task_id = None) -> (bool, str):
    """Unifica múltiplos arquivos de áudio em um único MP3."""
    if not audio_files:
        return False, "No audio files provided for unification."

    combined_audio = AudioSegment.empty()
    
    if progress and task_id is not None:
        progress.update(task_id, description="Initializing audio unification...")

    try:
        for i, file_path in enumerate(audio_files):
            if not os.path.exists(file_path):
                return False, f"Audio file not found: {file_path}"
            
            if progress and task_id is not None:
                progress.update(task_id, description=f"Adding [bright_white]{os.path.basename(file_path)}[/] to unified audio...")
                progress.update(task_id, advance=100 / len(audio_files))

            audio = AudioSegment.from_file(file_path)
            combined_audio += audio

        # Cria o diretório de saída se não existir
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        if progress and task_id is not None:
            progress.update(task_id, description=f"Exporting unified audio to [bright_white]{os.path.basename(output_path)}[/]...")

        combined_audio.export(output_path, format="mp3")
        
        if progress and task_id is not None:
            progress.update(task_id, completed=100, description="Unified audio exported.")

        console.print(f"[bright_green]✓ Unified audio saved to: {output_path}[/]")
        return True, output_path
    except Exception as e:
        return False, f"Error unifying audio files: {e}"

def generate_timestamps(audio_path: str, interval_minutes: int = 5, progress: Progress = None, task_id = None) -> (bool, str):
    """Gera timestamps para um arquivo de áudio em intervalos fixos."""
    if not os.path.exists(audio_path):
        return False, f"Audio file not found: {audio_path}"

    try:
        audio = AudioSegment.from_file(audio_path)
        total_milliseconds = len(audio)
        timestamps = []
        
        if progress and task_id is not None:
            progress.update(task_id, description=f"Generating timestamps for [bright_white]{os.path.basename(audio_path)}[/]...")

        current_ms = 0
        while current_ms < total_milliseconds:
            minutes = int((current_ms / (1000 * 60)) % 60)
            seconds = int((current_ms / 1000) % 60)
            timestamps.append(f"{minutes:02d}:{seconds:02d}")
            current_ms += interval_minutes * 60 * 1000

        timestamps_str = "\n".join(timestamps)

        if progress and task_id is not None:
            progress.update(task_id, completed=100, description="Timestamps generated.")

        console.print(f"[bright_green]✓ Timestamps generated for {os.path.basename(audio_path)}[/]")
        return True, timestamps_str
    except Exception as e:
        return False, f"Error generating timestamps: {e}"

# Exemplo de uso (para testes)
if __name__ == "__main__":
    # Crie alguns arquivos de áudio dummy para testar
    # Requer ffmpeg instalado e no PATH para pydub funcionar
    dummy_audio_dir = "./dummy_audios"
    os.makedirs(dummy_audio_dir, exist_ok=True)

    # Criar arquivos de áudio dummy (pode ser mp3, wav, etc.)
    # Para um teste real, você precisaria de arquivos de áudio válidos
    # from pydub.generators import Sine
    # sine_wave = Sine(440).to_audio_segment(duration=1000)
    # sine_wave.export(os.path.join(dummy_audio_dir, "audio1.mp3"), format="mp3")
    # sine_wave.export(os.path.join(dummy_audio_dir, "audio2.mp3"), format="mp3")

    # Para este exemplo, vamos apenas simular os caminhos
    audio_files_to_unify = [
        os.path.join(dummy_audio_dir, "audio1.mp3"),
        os.path.join(dummy_audio_dir, "audio2.mp3")
    ]
    output_unified_audio = "./unified_output.mp3"

    console.print(f"[bold bright_blue]Starting audio unification...[/]")
    success, result = create_unified_audio(audio_files_to_unify, output_unified_audio)
    if success:
        console.print(f"[bright_green]Unified audio created: {result}[/]")
    else:
        console.print(f"[bright_red]Error:[/]{result}")

    # Teste de geração de timestamps
    dummy_long_audio = "./long_audio.mp3"
    # Crie um arquivo de áudio longo para testar
    # from pydub.generators import Sine
    # long_sine_wave = Sine(440).to_audio_segment(duration=300000) # 5 minutos
    # long_sine_wave.export(dummy_long_audio, format="mp3")

    console.print(f"\n[bold bright_blue]Starting timestamp generation...[/]")
    success, timestamps = generate_timestamps(dummy_long_audio, interval_minutes=1)
    if success:
        console.print(f"[bright_green]Generated Timestamps:[/]\n{timestamps}")
    else:
        console.print(f"[bright_red]Error:[/]{timestamps}")

    # Limpar arquivos dummy
    # import shutil
    # shutil.rmtree(dummy_audio_dir)
    # if os.path.exists(output_unified_audio):
    #     os.remove(output_unified_audio)
    # if os.path.exists(dummy_long_audio):
    #     os.remove(dummy_long_audio)
