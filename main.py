# IMPORTS OBRIGATÓRIOS - ORDEM FIXA
import time
import os
import sys
from rich.console import Console
from rich.align import Align
from rich.text import Text
from pyfiglet import Figlet
from typing import List, Dict
from rich.prompt import Prompt

# Funções de UI e DB
from utils.database import initialize_database
from ui.utils import create_menu_panel
from ui.course_processor_menu import show_course_processor_menu
from ui.settings_menu import show_settings_menu

console = Console()

def render_main_title(app_name: str):
    """Renderiza título principal com fonte 'big'"""
    os.system('cls' if os.name == 'nt' else 'clear')
    figlet = Figlet(font="big")
    art = figlet.renderText(app_name)
    centered_art = Align.center(Text(art, style="bold bright_cyan"))
    console.print(centered_art)
    console.print()

def get_main_menu_content() -> str:
    """Retorna o conteúdo do painel do menu principal."""
    return """
[bold bright_blue]Media[/]
[bright_blue][1][/] [bright_white]Course Processor[/]
[bright_blue][2][/] [bright_white]YouTube Manager[/] [dim white](coming soon)[/]
[bright_blue][3][/] [bright_white]Feed Manager[/] [dim white](coming soon)[/]
[bright_blue][4][/] [bright_white]Snipd Tools[/] [dim white](coming soon)[/]

[bold bright_blue]System[/]
[bright_blue][9][/] [bright_white]Settings[/]
[bright_blue][10][/] [bright_white]Monitor[/] [dim white](coming soon)[/]
[bright_blue][11][/] [bright_white]Logs[/] [dim white](coming soon)[/]
[bright_blue][12][/] [bright_white]Exit[/]
"""

def main_menu():
    """Loop do menu principal."""
    while True:
        render_main_title("NeuroDeamon")
        content = get_main_menu_content()
        panel = create_menu_panel(content, "MAIN MENU")
        console.print(panel)

        valid_choices = ['1', '2', '3', '4', '9', '10', '11', '12']
        
        choice = Prompt.ask(
            "\n[bold bright_white]➤ Select option (12 to exit)[/]",
            choices=valid_choices,
            show_choices=False
        )

        if choice == '1':
            show_course_processor_menu()
        elif choice == '9':
            show_settings_menu()
        elif choice == '12':
            console.print("[bold bright_yellow]Exiting...[/]")
            break
        elif choice in ['2', '3', '4', '10', '11']:
            console.print("[bold bright_yellow]This feature is not yet implemented.[/]")
            time.sleep(1.5)
        else:
            console.print(f"[bold bright_red]Invalid option: {choice}[/]")
            time.sleep(1)


def main():
    """Função principal da aplicação."""
    initialize_database()
    main_menu()

if __name__ == "__main__":
    main()
