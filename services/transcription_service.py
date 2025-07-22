# services/transcription_service.py

import openai
import os
from rich.console import Console
from rich.progress import Progress
from services.security_service import load_api_keys

console = Console()

def transcribe_audio(audio_path: str, progress: Progress = None, task_id = None) -> (bool, str):
    """Transcreve um arquivo de áudio usando a API do OpenAI Whisper."""
    keys = load_api_keys()
    api_key = keys.get("openai_api_key")

    if not api_key or api_key == "sk-your-key-here":
        return False, "OpenAI API key not set. Please configure it in settings."

    if not os.path.exists(audio_path):
        return False, f"Audio file not found: {audio_path}"

    try:
        client = openai.OpenAI(api_key=api_key)
        
        if progress and task_id is not None:
            progress.update(task_id, description=f"Transcribing [bright_white]{os.path.basename(audio_path)}[/]...")

        with open(audio_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
        
        if progress and task_id is not None:
            progress.update(task_id, advance=100) # Completa a tarefa

        console.print(f"[bright_green]✓ Transcribed: {os.path.basename(audio_path)}[/]")
        return True, transcript.text
    except openai.AuthenticationError:
        return False, "OpenAI Authentication failed. Check your API key."
    except openai.APIConnectionError as e:
        return False, f"OpenAI API connection error: {e}"
    except openai.RateLimitError:
        return False, "OpenAI API rate limit exceeded. Please wait and try again."
    except Exception as e:
        return False, f"An unexpected error occurred during transcription: {e}"

# Exemplo de uso (para testes)
if __name__ == "__main__":
    # Crie um arquivo de áudio dummy para testar
    # Ex: dummy_audio.mp3
    dummy_audio_path = "./dummy_audio.mp3"
    with open(dummy_audio_path, "w") as f: f.write("dummy audio content")

    console.print(f"[bold bright_blue]Starting audio transcription for {dummy_audio_path}[/]")
    success, result = transcribe_audio(dummy_audio_path)
    if success:
        console.print(f"[bright_green]Transcription:[/]\n{result}")
    else:
        console.print(f"[bright_red]Error:[/]{result}")

    os.remove(dummy_audio_path)
