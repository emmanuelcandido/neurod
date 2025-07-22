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

    # Limpar arquivos dummy
    # import shutil
    # shutil.rmtree(dummy_audio_dir)
    # if os.path.exists(output_unified_audio):
    #     os.remove(output_unified_audio)
