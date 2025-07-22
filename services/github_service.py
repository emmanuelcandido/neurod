# services/github_service.py

import os
from git import Repo, GitCommandError
from rich.console import Console
from rich.progress import Progress

console = Console()

GITHUB_REPO_PATH = os.path.join("github", "neurodeamon-feeds")

def update_github_repo(commit_message: str, progress: Progress = None, task_id = None) -> (bool, str):
    """Faz commit e push de arquivos para o repositório GitHub."""
    try:
        if not os.path.exists(GITHUB_REPO_PATH):
            return False, f"GitHub repository path not found: {GITHUB_REPO_PATH}. Please initialize it as a Git repository."

        repo = Repo(GITHUB_REPO_PATH)
        
        if progress and task_id is not None:
            progress.update(task_id, description="Adding files to Git...")

        repo.git.add(A=True) # Adiciona todos os arquivos modificados/novos

        if not repo.is_dirty(untracked_files=True):
            console.print("[bright_yellow]No changes to commit in GitHub repository.[/]")
            if progress and task_id is not None:
                progress.update(task_id, completed=100, description="No changes.")
            return True, "No changes to commit."

        if progress and task_id is not None:
            progress.update(task_id, description=f"Committing changes: [bright_white]{commit_message}[/]...")

        repo.index.commit(commit_message)

        if progress and task_id is not None:
            progress.update(task_id, description="Pushing to GitHub...")

        origin = repo.remotes.origin
        origin.push()

        if progress and task_id is not None:
            progress.update(task_id, completed=100, description="GitHub update complete.")

        console.print(f"[bright_green]✓ GitHub repository updated successfully.[/]")
        return True, "GitHub repository updated."
    except GitCommandError as e:
        return False, f"Git command error: {e}"
    except Exception as e:
        return False, f"An unexpected error occurred during GitHub update: {e}"

# Exemplo de uso (para testes)
if __name__ == "__main__":
    async def main_test():
        # Para testar, você precisa ter um repositório Git inicializado em github/neurodeamon-feeds
        # e configurado com um remote.
        # Ex: 
        # cd github/neurodeamon-feeds
        # git init
        # git remote add origin <your_repo_url>
        # git pull origin master (se já tiver conteúdo)

        # Crie um arquivo dummy para testar o commit
        os.makedirs(GITHUB_REPO_PATH, exist_ok=True)
        with open(os.path.join(GITHUB_REPO_PATH, "test_file.txt"), "w") as f: f.write("Test content")

        console.print(f"[bold bright_blue]Starting GitHub repository update...[/]")
        success, result = update_github_repo("Test commit from NeuroDeamon")
        if success:
            console.print(f"[bright_green]GitHub update successful: {result}[/]")
        else:
            console.print(f"[bright_red]GitHub update failed: {result}[/]")

        # Limpar arquivo dummy
        # os.remove(os.path.join(GITHUB_REPO_PATH, "test_file.txt"))

    import asyncio
    asyncio.run(main_test())
