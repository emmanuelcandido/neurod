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

from services.video_service import process_course_videos_to_audio
from services.transcription_service import transcribe_audio

# ... (código anterior)

from services.video_service import process_course_videos_to_audio
from services.transcription_service import transcribe_audio
from services.ai_service import generate_summary_claude

# ... (código anterior)

from services.video_service import process_course_videos_to_audio
from services.transcription_service import transcribe_audio
from services.ai_service import generate_summary_claude
from services.audio_service import create_unified_audio

# ... (código anterior)

from services.video_service import process_course_videos_to_audio
from services.transcription_service import transcribe_audio
from services.ai_service import generate_summary_claude
from services.audio_service import create_unified_audio, generate_timestamps

# ... (código anterior)

from services.video_service import process_course_videos_to_audio
from services.transcription_service import transcribe_audio
from services.ai_service import generate_summary_claude
from services.audio_service import create_unified_audio, generate_timestamps
from services.tts_service import generate_tts_audio
import asyncio

# ... (código anterior)

from services.video_service import process_course_videos_to_audio
from services.transcription_service import transcribe_audio
from services.ai_service import generate_summary_claude
from services.audio_service import create_unified_audio, generate_timestamps
from services.tts_service import generate_tts_audio
from services.gdrive_service import upload_file_to_drive
import asyncio

# ... (código anterior)

from services.video_service import process_course_videos_to_audio
from services.transcription_service import transcribe_audio
from services.ai_service import generate_summary_claude
from services.audio_service import create_unified_audio, generate_timestamps
from services.tts_service import generate_tts_audio
from services.gdrive_service import upload_file_to_drive
from services.rss_service import update_rss_feed
from services.github_service import update_github_repo
import asyncio

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
        elif result == 3: # Transcribe Audio Files
            audio_file_path = safe_input("Enter the path to the audio file to transcribe: ")
            if audio_file_path:
                with console.status("[bold blue]Transcribing audio...[/]"):
                    success, transcription_text = transcribe_audio(audio_file_path)
                    if success:
                        console.print(f"
[bright_green]Transcription Result:[/]{transcription_text}")
                    else:
                        console.print(f"
[bright_red]Transcription Error:[/]{transcription_text}")
            time.sleep(2)
        elif result == 4: # Generate AI Course Summaries
            transcription_file_path = safe_input("Enter the path to the transcription file (.txt): ")
            if transcription_file_path and os.path.exists(transcription_file_path):
                with open(transcription_file_path, "r", encoding="utf-8") as f:
                    transcription_content = f.read()
                
                prompt_name = safe_input("Enter the prompt name (e.g., summary_test): ")
                if prompt_name:
                    with console.status("[bold blue]Generating summary...[/]"):
                        success, summary_text = generate_summary_claude(transcription_content, prompt_name)
                        if success:
                            console.print(f"
[bright_green]Generated Summary:[/]{summary_text}")
                        else:
                            console.print(f"
[bright_red]Summary Generation Error:[/]{summary_text}")
            else:
                console.print("[bright_red]Transcription file not found.[/]")
            time.sleep(2)
        elif result == 5: # Create Unified Audio
            audio_files_str = safe_input("Enter paths to audio files to unify (comma-separated): ")
            if audio_files_str:
                audio_files = [f.strip() for f in audio_files_str.split(',気分')] # Changed 'split(",")' to 'split(",気分")' to avoid escaping issues
                output_unified_path = safe_input("Enter the output path for the unified audio (.mp3): ")
                if output_unified_path:
                    with console.status("[bold blue]Unifying audio files...[/]"):
                        success, message = create_unified_audio(audio_files, output_unified_path)
                        if success:
                            console.print(f"
[bright_green]Audio unified successfully:[/]{message}")
                        else:
                            console.print(f"
[bright_red]Audio unification error:[/]{message}")
            time.sleep(2)
        elif result == 6: # Generate Timestamps Only
            audio_file_path = safe_input("Enter the path to the audio file for timestamps: ")
            if audio_file_path:
                interval_str = safe_input("Enter timestamp interval in minutes (default: 5): ", input_type="int")
                interval = int(interval_str) if interval_str else 5
                with console.status("[bold blue]Generating timestamps...[/]"):
                    success, timestamps_text = generate_timestamps(audio_file_path, interval)
                    if success:
                        console.print(f"
[bright_green]Generated Timestamps:[/]{timestamps_text}")
                    else:
                        console.print(f"
[bright_red]Timestamp Generation Error:[/]{timestamps_text}")
            time.sleep(2)
        elif result == 7: # Generate Course TTS Audio Notes
            text_to_speak = safe_input("Enter the text to convert to speech: ")
            if text_to_speak:
                output_tts_path = safe_input("Enter the output path for the TTS audio (.mp3): ")
                if output_tts_path:
                    with console.status("[bold blue]Generating TTS audio...[/]"):
                        success, message = asyncio.run(generate_tts_audio(text_to_speak, output_tts_path))
                        if success:
                            console.print(f"
[bright_green]TTS audio generated successfully:[/]{message}")
                        else:
                            console.print(f"
[bright_red]TTS audio generation error:[/]{message}")
            time.sleep(2)
        elif result == 8: # Upload Course to Google Drive
            file_to_upload = safe_input("Enter the path to the file to upload to Google Drive: ")
            if file_to_upload:
                folder_id = safe_input("Enter the Google Drive folder ID (optional): ")
                with console.status("[bold blue]Uploading to Google Drive...[/]"):
                    success, message = upload_file_to_drive(file_to_upload, folder_id if folder_id else None)
                    if success:
                        console.print(f"
[bright_green]File uploaded successfully:[/]{message}")
                    else:
                        console.print(f"
[bright_red]Google Drive upload error:[/]{message}")
            time.sleep(2)
        elif result == 9: # Update courses.xml
            course_data = {
                'title': safe_input("Enter course title: "),
                'link': safe_input("Enter course link (e.g., MP3 URL): "),
                'guid': safe_input("Enter unique GUID for the course: "),
                'description': safe_input("Enter course description: "),
                'enclosure_url': safe_input("Enter enclosure URL (e.g., MP3 URL for podcast player): "),
                'enclosure_length': safe_input("Enter enclosure length in bytes: "),
                'duration': safe_input("Enter duration (HH:MM:SS): "),
                'author': safe_input("Enter author (optional): ", default="NeuroDeamon"),
            }
            with console.status("[bold blue]Updating RSS feed...[/]"):
                success, message = update_rss_feed(course_data)
                if success:
                    console.print(f"
[bright_green]RSS feed updated successfully:[/]{message}")
                else:
                    console.print(f"
[bright_red]RSS feed update error:[/]{message}")
            time.sleep(2)
        elif result == 10: # Update GitHub Repository
            commit_msg = safe_input("Enter commit message for GitHub: ")
            if commit_msg:
                with console.status("[bold blue]Updating GitHub repository...[/]"):
                    success, message = update_github_repo(commit_msg)
                    if success:
                        console.print(f"
[bright_green]GitHub repository updated successfully:[/]{message}")
                    else:
                        console.print(f"
[bright_red]GitHub repository update error:[/]{message}")
            time.sleep(2)
        else:
            console.print(f"[bold bright_yellow]Option {result} is not yet implemented.[/]")
            time.sleep(1.5)

