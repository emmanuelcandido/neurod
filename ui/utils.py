# ui/utils.py

from rich.console import Console
from rich.panel import Panel
from rich.box import ROUNDED
from rich.prompt import IntPrompt, Prompt, Confirm
from typing import Union
from utils.logger import logger

console = Console()

def create_menu_panel(content: str, title: str) -> Panel:
    """Painel de menu sem emoji na borda"""
    return Panel(
        content,
        title=f"[bold bright_blue]{title}[/bold bright_blue]",
        border_style="bright_blue",
        box=ROUNDED,
        padding=(1, 2)
    )

def get_menu_choice(prompt: str = "Enter your choice", max_option: int = None) -> str:
    """Input padrão com navegação ESC e validação numérica"""
    try:
        if max_option:
            choice = IntPrompt.ask(
                f"\n[bold bright_white]➤ {prompt} (0 to go back)[/bold bright_white]",
                choices=[str(i) for i in range(0, max_option + 1)],
                show_choices=False
            )
            return str(choice)
        else:
            choice = console.input(f"\n[bold bright_white]➤ {prompt} (ESC to go back): [/bold bright_white]").strip()
            return choice
    except KeyboardInterrupt:
        logger.info("User cancelled input (Ctrl+C).")
        console.print("\n[bright_yellow]⚠️ Returning to previous menu (ESC/Ctrl+C)[/bright_yellow]")
        return "0"
    except EOFError:
        logger.info("Input ended unexpectedly (Ctrl+D).")
        console.print("\n[bright_yellow]⚠️ Input ended (Ctrl+D)[/bright_yellow]")
        return "0"

def handle_menu_navigation(choice: str, max_option: int) -> Union[int, str]:
    """Manipula navegação de menu com validação"""
    if choice.lower() in ['0', 'back', 'b']:
        return "back"
    
    try:
        num_choice = int(choice)
        if 1 <= num_choice <= max_option:
            return num_choice
        else:
            logger.warning(f"Invalid menu choice: {choice}. Expected between 1 and {max_option}.")
            console.print(f"[bright_yellow]⚠️ Please enter a number between 1 and {max_option}[/bright_yellow]")
            return "invalid"
    except ValueError:
        logger.warning(f"Invalid menu input: {choice}. Not a number.")
        console.print("[bright_yellow]⚠️ Please enter a valid number[/bright_yellow]")
        return "invalid"

def safe_input(prompt: str, input_type: str = "text", **kwargs) -> Union[str, int, bool, None]:
    """Input seguro com tratamento de interrupções"""
    try:
        if input_type == "int":
            return IntPrompt.ask(f"[bold bright_white]➤ {prompt}[/bold bright_white]", **kwargs)
        elif input_type == "bool":
            return Confirm.ask(f"[bold bright_white]➤ {prompt}[/bold bright_white]", **kwargs)
        else:
            return Prompt.ask(f"[bold bright_white]➤ {prompt}[/bold bright_white]", **kwargs)
    except (KeyboardInterrupt, EOFError):
        logger.info("User cancelled input (Ctrl+C or Ctrl+D).")
        console.print("\n[bright_yellow]⚠️ Input cancelled[/bright_yellow]")
        return None

