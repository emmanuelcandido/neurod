# ui/course_processor_menu.py

import os
import time
from rich.console import Console
from rich.align import Align
from rich.text import Text

from ui.utils import create_menu_panel, get_menu_choice, handle_menu_navigation

console = Console()

def render_submenu_header(menu_name: str, emoji: str = "⚙️"):
    """Cabeçalho simples para submenus - SEM arte ASCII"""
    os.system('cls' if os.name == 'nt' else 'clear')
    header = f"{emoji} {menu_name}"
    console.print(f"\n[bold bright_cyan]{header}[/]")
    console.print("[bright_blue]" + "─" * (len(header) + 1) + "[/]")
    console.print()

def get_course_processor_menu_content() -> str:
    """Retorna o conteúdo do painel do menu do processador de cursos."""
    return """
[bold bright_blue]Core Processing[/]
[bright_blue][1][/] [bright_white]Process Complete Course[/]

[bold bright_blue]Individual Operations[/]
[bright_blue][2][/] [bright_white]Convert Courses to Audio[/]
[bright_blue][3][/] [bright_white]Transcribe Audio Files[/]
[bright_blue][4][/] [bright_white]Generate AI Course Summaries[/]
[bright_blue][5][/] [bright_white]Create Unified Audio[/]
[bright_blue][6][/] [bright_white]Generate Timestamps Only[/]
[bright_blue][7][/] [bright_white]Generate Course TTS Audio Notes[/]

[bold bright_blue]Cloud & Distribution[/]
[bright_blue][8][/] [bright_white]Upload Course to Google Drive[/]
[bright_blue][9][/] [bright_white]Update courses.xml[/]
[bright_blue][10][/] [bright_white]Update GitHub Repository[/]

[bold bright_blue]Course Management[/]
[bright_blue][11][/] [bright_white]Course Status Check[/]
[bright_blue][12][/] [bright_white]Forget Course[/]
[bright_blue][13][/] [bright_white]Clear All Data[/]

[bright_blue][0][/] [bright_white]Back to Main Menu[/]
"""

from ui.utils import create_menu_panel, get_menu_choice, handle_menu_navigation, safe_input
from services.video_service import process_course_videos_to_audio

# ... (código anterior)

def show_course_processor_menu():
    """Loop do menu do processador de cursos."""
    while True:
        render_submenu_header("COURSE PROCESSOR", "🎓")
        content = get_course_processor_menu_content()
        panel = create_menu_panel(content, "Course Processor Options")
        console.print(panel)

        choice = get_menu_choice("Select option", 13)
        result = handle_menu_navigation(choice, 13)

        if result == "back":
            break
        elif result == "invalid":
            time.sleep(1)
            continue
        elif result == 2: # Convert Courses to Audio
            course_dir = safe_input("Enter the path to the course directory: ")
            if course_dir:
                output_dir = safe_input("Enter the output directory for audio files: ")
                if output_dir:
                    process_course_videos_to_audio(course_dir, output_dir)
            time.sleep(2)
        else:
            console.print(f"[bold bright_yellow]Option {result} is not yet implemented.[/]")
            time.sleep(1.5)

