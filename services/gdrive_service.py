# services/gdrive_service.py

import os
import io
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from rich.console import Console
from rich.progress import Progress

console = Console()

# Se modificar esses escopos, delete o arquivo token.json.
SCOPES = ['https://www.googleapis.com/auth/drive.file']

CREDENTIALS_FILE = os.path.join("config", "credentials.json")
TOKEN_FILE = os.path.join("config", "token.json")

def get_gdrive_service(progress: Progress = None, task_id = None):
    """Autentica e retorna o serviço da Google Drive API."""
    creds = None
    # O arquivo token.json armazena os tokens de acesso e refresh do usuário,
    # e é criado automaticamente quando o fluxo de autorização é concluído pela primeira vez.
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    # Se não há credenciais válidas disponíveis, permite que o usuário faça login.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            if progress and task_id is not None:
                progress.update(task_id, description="Refreshing Google Drive credentials...")
            creds.refresh(Request())
        else:
            if not os.path.exists(CREDENTIALS_FILE):
                console.print("[bright_red]✗ Error: credentials.json not found in the 'config' directory.[/]")
                console.print("[bright_yellow]Please download your Google API credentials (client_secret.json) and rename it to credentials.json.[/]")
                console.print("[bright_yellow]Visit Google Cloud Console -> APIs & Services -> Credentials -> Create Credentials -> OAuth client ID -> Desktop app.[/]")
                return None

            if progress and task_id is not None:
                progress.update(task_id, description="Authorizing Google Drive access...")
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            
            # Este é o ponto onde o usuário precisaria interagir com o navegador.
            # Para um CLI, isso é um desafio. Assumimos que o usuário fará isso manualmente
            # ou que o token.json já existe de uma execução anterior.
            console.print("[bright_yellow]Please open the following URL in your browser to authorize Google Drive access:[/]")
            auth_url, _ = flow.authorization_url(prompt='consent')
            console.print(f"[bright_blue]{auth_url}[/]")
            code = console.input("[bold bright_white]Enter the authorization code from your browser: [/]")
            flow.fetch_token(code=code)
            creds = flow.credentials
        # Salva as credenciais para a próxima execução
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
    
    if progress and task_id is not None:
        progress.update(task_id, advance=100) # Completa a tarefa

    return build('drive', 'v3', credentials=creds)

def upload_file_to_drive(file_path: str, folder_id: str = None, progress: Progress = None, task_id = None) -> (bool, str):
    """Faz upload de um arquivo para o Google Drive."""
    service = get_gdrive_service(progress, task_id) # Reutiliza o progresso da autenticação
    if not service:
        return False, "Google Drive service not available."

    if not os.path.exists(file_path):
        return False, f"File not found: {file_path}"

    file_name = os.path.basename(file_path)
    file_metadata = {'name': file_name}
    if folder_id:
        file_metadata['parents'] = [folder_id]

    media = MediaFileUpload(file_path, resumable=True)

    try:
        if progress and task_id is not None:
            progress.update(task_id, description=f"Uploading [bright_white]{file_name}[/] to Google Drive...")

        file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        
        if progress and task_id is not None:
            progress.update(task_id, completed=100, description="Upload complete.")

        console.print(f"[bright_green]✓ File '{file_name}' uploaded to Google Drive. File ID: {file.get('id')}[/]")
        return True, file.get('id')
    except HttpError as error:
        console.print(f"[bright_red]✗ An error occurred: {error}[/]")
        return False, str(error)
    except Exception as e:
        return False, f"An unexpected error occurred during upload: {e}"

# Exemplo de uso (para testes)
if __name__ == "__main__":
    async def main_test():
        # Crie um arquivo dummy para testar o upload
        test_file = "./test_upload.txt"
        with open(test_file, "w") as f: f.write("This is a test file for Google Drive upload.")

        console.print(f"[bold bright_blue]Starting Google Drive upload...[/]")
        # Substitua 'your_folder_id' pelo ID de uma pasta no seu Google Drive, se quiser fazer upload para uma pasta específica
        success, result = upload_file_to_drive(test_file, folder_id=None)
        if success:
            console.print(f"[bright_green]Upload successful. File ID: {result}[/]")
        else:
            console.print(f"[bright_red]Upload failed: {result}[/]")

        # Limpar arquivo dummy
        # if os.path.exists(test_file):
        #     os.remove(test_file)

    import asyncio
    asyncio.run(main_test())
