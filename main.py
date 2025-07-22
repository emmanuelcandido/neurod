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
from utils.database import initialize_database, get_db_connection
from utils.logger import logger, setup_logging
from ui.utils import create_menu_panel
from ui.course_processor_menu import show_course_processor_menu
from ui.settings_menu import show_settings_menu
from services.course_processor_service import process_complete_course

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

def check_for_interrupted_courses():
    """Verifica se há cursos com processamento interrompido e pergunta ao usuário se deseja retomar."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, directory_path, processing_stage FROM courses WHERE status = 'in_progress'")
    interrupted_courses = cursor.fetchall()
    conn.close()

    if interrupted_courses:
        console.print("\n[bold bright_yellow]⚠️ Detected interrupted course processing:[/]")
        for course in interrupted_courses:
            console.print(f"  - Course: [bright_white]{course['name']}[/] (ID: {course['id']}) at stage: [bright_white]{course['processing_stage']}[/]")
        
        resume_choice = Prompt.ask("[bold bright_white]Do you want to resume processing? (yes/no)[/]").lower()
        if resume_choice == 'yes':
            # Por enquanto, vamos retomar o primeiro curso interrompido
            # Em uma versão mais robusta, o usuário poderia escolher qual retomar
            course_to_resume = interrupted_courses[0]
            logger.info(f"Resuming course {course_to_resume['name']} (ID: {course_to_resume['id']}) from stage {course_to_resume['processing_stage']}")
            # Chamar a função de processamento completo com o ID do curso e o estágio
            # A função process_complete_course precisaria ser adaptada para retomar
            # Por enquanto, apenas um placeholder
            console.print("[bold bright_green]Resuming functionality not fully implemented yet. Please restart the process manually.[/]")
            time.sleep(2)
        else:
            console.info("User chose not to resume processing.")

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
            logger.info("Exiting application.")
            break
        elif choice in ['2', '3', '4', '10', '11']:
            console.print("[bold bright_yellow]This feature is not yet implemented.[/]")
            time.sleep(1.5)
        else:
            console.print(f"[bold bright_red]Invalid option: {choice}[/]")
            time.sleep(1)


def main():
    """Função principal da aplicação."""
    setup_logging()
    logger.info("NeuroDeamon application started.")
    initialize_database()
    check_for_interrupted_courses()
    main_menu()

if __name__ == "__main__":
    main()
