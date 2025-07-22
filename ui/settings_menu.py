'''# ui/settings_menu.py

import os
import time
from rich.console import Console
from rich.table import Table
from rich.box import ROUNDED

from ui.utils import create_menu_panel, get_menu_choice, handle_menu_navigation
from services.security_service import load_api_keys, save_api_keys

console = Console()

def render_submenu_header(menu_name: str, emoji: str = "⚙️"):
    """Cabeçalho simples para submenus - SEM arte ASCII"""
    os.system('cls' if os.name == 'nt' else 'clear')
    header = f"{emoji} {menu_name}"
    console.print(f"
[bold bright_cyan]{header}[/]")
    console.print("[bright_blue]" + "─" * (len(header) + 1) + "[/]")
    console.print()

from rich.prompt import Prompt

def configure_api_keys():
    """Permite ao usuário inserir e salvar novas chaves de API."""
    render_submenu_header("CONFIGURE API KEYS", "🔑")
    console.print("[dim white]Enter your API keys below. Press Enter to keep the current value.[/]")
    
    current_keys = load_api_keys()
    new_keys = {}

    for key_name, readable_name in [("openai_api_key", "OpenAI"), ("anthropic_api_key", "Anthropic"), ("gemini_api_key", "Gemini"), ("github_token", "GitHub")]:
        current_value = current_keys.get(key_name, "")
        new_value = Prompt.ask(
            f"  [bright_white]➤ Enter {readable_name} API Key[/]", 
            default=f"...{current_value[-4:]}" if current_value else "Not Set"
        )
        # Se o usuário apenas apertar Enter, o valor retornado será o default.
        # Se o valor não mudou, mantemos o antigo.
        if new_value == (f"...{current_value[-4:]}" if current_value else "Not Set"):
            new_keys[key_name] = current_value
        else:
            new_keys[key_name] = new_value

    save_api_keys(new_keys)
    console.print("\n[bright_green]✓ API keys saved successfully![/]")
    time.sleep(1.5)


from services.validation_service import test_anthropic_api

# ... (código anterior)

def show_api_keys_menu():
    """Mostra o menu de validação e configuração de chaves de API."""
    api_status = {
        "Claude API": "[yellow]Not Tested[/]",
        "ChatGPT API": "[yellow]Not Tested[/]",
        "Gemini API": "[yellow]Not Tested[/]",
        "Google Drive": "[yellow]Not Tested[/]",
        "Whisper API": "[yellow]Not Tested[/]",
    }

    while True:
        render_submenu_header("API KEYS & VALIDATION", "🔑")
        
        keys = load_api_keys()
        
        table = Table(title="[bold bright_blue]API Status[/]", box=ROUNDED)
        table.add_column("API Name", style="bright_white")
        table.add_column("Key", style="dim white")
        table.add_column("Status", style="white")

        table.add_row("Claude API", f'...{keys.get("anthropic_api_key", "Not Set")[-4:]}' if keys.get("anthropic_api_key") else "Not Set", api_status["Claude API"])
        table.add_row("ChatGPT API", f'...{keys.get("openai_api_key", "Not Set")[-4:]}' if keys.get("openai_api_key") else "Not Set", api_status["ChatGPT API"])
        table.add_row("Gemini API", f'...{keys.get("gemini_api_key", "Not Set")[-4:]}' if keys.get("gemini_api_key") else "Not Set", api_status["Gemini API"])
        table.add_row("Google Drive", "Configured via OAuth", api_status["Google Drive"])
        table.add_row("Whisper API", "Uses OpenAI Key", api_status["Whisper API"])

        console.print(table)

        content = """
[bright_blue][1][/] [bright_white]Refresh All Status[/]
[bright_blue][2][/] [bright_white]Test Individual API[/]
[bright_blue][3][/] [bright_white]Configure API Keys[/]
[bright_blue][0][/] [bright_white]Back to Settings[/]
"""
        panel = create_menu_panel(content, "API Options")
        console.print(panel)

        choice = get_menu_choice("Select option", 3)
        result = handle_menu_navigation(choice, 3)

        if result == "back":
            break
        elif result == "invalid":
            time.sleep(1)
            continue
        elif result == 1: # Refresh All Status
            with console.status("[bold blue]Testing APIs...[/]"):
                success, message = test_anthropic_api()
                if success:
                    api_status["Claude API"] = f"[bright_green]✓ Active[/]"
                else:
                    api_status["Claude API"] = f"[bright_red]✗ Failed: {message}[/]"
                # Adicionar testes para outras APIs aqui
            console.print("Status updated.")
            time.sleep(1)
        elif result == 3:
            configure_api_keys()
        else:
            console.print(f"[bold bright_yellow]Option {result} is not yet implemented.[/]")
            time.sleep(1.5)


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
        elif result == 1:
            show_api_keys_menu()
        else:
            console.print(f"[bold bright_yellow]Option {result} is not yet implemented.[/]")
            time.sleep(1.5)
''

