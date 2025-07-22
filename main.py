# IMPORTS OBRIGATÓRIOS - ORDEM FIXA
import time
import os
import sys
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.box import ROUNDED
from rich.align import Align
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.prompt import Prompt, IntPrompt, Confirm
from pyfiglet import Figlet
from typing import List, Dict, Optional, Union

# Funções do design.md (serão movidas para utils/ui.py depois)
# Por enquanto, vamos mantê-las aqui para simplicidade.

console = Console()

def render_main_title(app_name: str):
    """Renderiza título principal com fonte 'big' - APENAS para menu principal"""
    os.system('cls' if os.name == 'nt' else 'clear')
    figlet = Figlet(font="big")
    art = figlet.renderText(app_name)
    centered_art = Align.center(Text(art, style="bold bright_cyan"))
    console.print(centered_art)
    console.print()

from utils.database import initialize_database

def main():
    """Função principal da aplicação."""
    initialize_database()
    render_main_title("NeuroDeamon")
    console.print("[bold bright_green]Bem-vindo ao NeuroDeamon Course Processor![/]")
    console.print("A estrutura inicial do projeto foi criada.")
    console.print("Próximo passo: Implementar a navegação completa do menu.")

if __name__ == "__main__":
    main()
