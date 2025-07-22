# services/tts_service.py

import asyncio
import edge_tts
import os
from rich.console import Console
from rich.progress import Progress

console = Console()

async def generate_tts_audio(text: str, output_path: str, voice: str = "pt-BR-FranciscaNeural", progress: Progress = None, task_id = None) -> (bool, str):
    """Gera áudio a partir de texto usando edge-tts."""
    try:
        if progress and task_id is not None:
            progress.update(task_id, description=f"Generating TTS audio to [bright_white]{os.path.basename(output_path)}[/]...")

        communicate = edge_tts.Communicate(text, voice)
        
        # Cria o diretório de saída se não existir
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        await communicate.save(output_path)

        if progress and task_id is not None:
            progress.update(task_id, completed=100, description="TTS audio generated.")

        console.print(f"[bright_green]✓ TTS audio saved to: {output_path}[/]")
        return True, output_path
    except Exception as e:
        return False, f"Error generating TTS audio: {e}"

# Exemplo de uso (para testes)
if __name__ == "__main__":
    async def main_test():
        test_text = "Olá, este é um teste de síntese de voz com Edge TTS."
        test_output_path = "./test_tts_output.mp3"
        
        console.print(f"[bold bright_blue]Starting TTS audio generation...[/]")
        success, result = await generate_tts_audio(test_text, test_output_path)
        if success:
            console.print(f"[bright_green]TTS audio created: {result}[/]")
        else:
            console.print(f"[bright_red]Error:[/]{result}")

        # Limpar arquivo dummy
        # if os.path.exists(test_output_path):
        #     os.remove(test_output_path)

    asyncio.run(main_test())
