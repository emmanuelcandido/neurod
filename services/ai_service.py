# services/ai_service.py

import anthropic
import os
from rich.console import Console
from rich.progress import Progress
from services.security_service import load_api_keys

console = Console()

PROMPTS_DIR = os.path.join("prompts", "course_processor")

def load_prompt(prompt_name: str) -> str:
    """Carrega um prompt de um arquivo .md."""
    prompt_path = os.path.join(PROMPTS_DIR, f"{prompt_name}.md")
    if not os.path.exists(prompt_path):
        raise FileNotFoundError(f"Prompt file not found: {prompt_path}")
    with open(prompt_path, "r", encoding="utf-8") as f:
        return f.read()

def generate_summary_claude(transcription_text: str, prompt_name: str, progress: Progress = None, task_id = None) -> (bool, str):
    """Gera um resumo usando a API da Anthropic (Claude)."""
    keys = load_api_keys()
    api_key = keys.get("anthropic_api_key")

    if not api_key or api_key == "your-key-here":
        return False, "Anthropic API key not set. Please configure it in settings."

    try:
        client = anthropic.Anthropic(api_key=api_key, timeout=60.0)
        prompt_template = load_prompt(prompt_name)
        
        full_prompt = prompt_template.replace("{{TRANSCRIPTION}}", transcription_text)

        if progress and task_id is not None:
            progress.update(task_id, description=f"Generating summary with Claude using prompt [bright_white]{prompt_name}[/]...")

        message = client.messages.create(
            model="claude-3-sonnet-20240229", # Usando Sonnet como padrão, pode ser configurável
            max_tokens=2000, # Limite de tokens para a resposta
            messages=[
                {"role": "user", "content": full_prompt}
            ]
        )
        
        if progress and task_id is not None:
            progress.update(task_id, advance=100) # Completa a tarefa

        console.print(f"[bright_green]✓ Summary generated with Claude using prompt {prompt_name}[/]")
        return True, message.content[0].text
    except FileNotFoundError as e:
        return False, str(e)
    except anthropic.AuthenticationError:
        return False, "Anthropic Authentication failed. Check your API key."
    except anthropic.APIConnectionError as e:
        return False, f"Anthropic API connection error: {e}"
    except anthropic.RateLimitError:
        return False, "Anthropic API rate limit exceeded. Please wait and try again."
    except Exception as e:
        return False, f"An unexpected error occurred during summary generation: {e}"

# Exemplo de uso (para testes)
if __name__ == "__main__":
    # Crie um prompt de exemplo em prompts/course_processor/summary_test.md
    # Conteúdo: "Summarize the following transcription: {{TRANSCRIPTION}}"
    os.makedirs(PROMPTS_DIR, exist_ok=True)
    with open(os.path.join(PROMPTS_DIR, "summary_test.md"), "w", encoding="utf-8") as f:
        f.write("Summarize the following transcription: {{TRANSCRIPTION}}")

    dummy_transcription = "This is a long transcription about the benefits of AI in education. AI can personalize learning, automate grading, and provide instant feedback. However, ethical considerations and data privacy are important." 

    console.print(f"[bold bright_blue]Starting AI summary generation...[/]")
    success, summary = generate_summary_claude(dummy_transcription, "summary_test")
    if success:
        console.print(f"[bright_green]Generated Summary:[/]\n{summary}")
    else:
        console.print(f"[bright_red]Error:[/]{summary}")

    # Limpar arquivo dummy
    os.remove(os.path.join(PROMPTS_DIR, "summary_test.md"))
