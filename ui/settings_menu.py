# ui/settings_menu.py

import os
import time
from rich.console import Console

from ui.utils import create_menu_panel, get_menu_choice, handle_menu_navigation

console = Console()

def render_submenu_header(menu_name: str, emoji: str = "⚙️"):
    """Cabeçalho simples para submenus - SEM arte ASCII"""
    os.system('cls' if os.name == 'nt' else 'clear')
    header = f"{emoji} {menu_name}"
    console.print(f"\n[bold bright_cyan]{header}[/]")
    console.print("[bright_blue]" + "─" * (len(header) + 1) + "[/]")
    console.print()

def get_settings_menu_content() -> str:
    """Retorna o conteúdo do painel do menu de configurações."""
    return """
[bold bright_blue]General Settings[/]
[bright_blue][1][/] [bright_white]API Keys & Validation[/]
[bright_blue][2][/] [bright_white]Voice Settings[/]
[bright_blue][3][/] [bright_white]Output Directory[/]
[bright_blue][4][/] [bright_white]GitHub Repository[/]
[bright_blue][5][/] [bright_white]Cleanup Tools[/]

[bold bright_blue]Course Processor[/]
[bright_blue][6][/] [bright_white]Processing Preferences[/]

[bright_blue][0][/] [bright_white]Back to Main Menu[/]
"""

def show_settings_menu():
    """Loop do menu de configurações."""
    while True:
        render_submenu_header("CONFIGURAÇÕES", "⚙️")
        content = get_settings_menu_content()
        panel = create_menu_panel(content, "Settings Options")
        console.print(panel)

        choice = get_menu_choice("Select option", 6)
        result = handle_menu_navigation(choice, 6)

        if result == "back":
            break
        elif result == "invalid":
            time.sleep(1)
            continue
        else:
            console.print(f"[bold bright_yellow]Option {result} is not yet implemented.[/]")
            time.sleep(1.5)

