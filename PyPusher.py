import subprocess
import os
import sys
from typing import List, Optional

class GitCommandError(Exception):
    pass

def execute_command(command: List[str], cwd: str) -> str:
    """Exécute une commande shell et retourne sa sortie."""
    try:
        result = subprocess.run(command, cwd=cwd, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        raise GitCommandError(f"Erreur lors de l'exécution de la commande: {e.stderr}")

def check_command_output(command: List[str], cwd: str) -> Optional[str]:
    """Vérifie la sortie d'une commande sans lever d'exception."""
    try:
        return execute_command(command, cwd)
    except GitCommandError:
        return None

class GitRepository:
    def __init__(self, project_dir: str, repo_url: str):
        self.project_dir = project_dir
        self.repo_url = repo_url

    def initialize(self):
        """Initialise le dépôt Git et configure le dépôt distant."""
        if self._is_git_repo():
            print("Le répertoire contient déjà un dépôt Git.")
            return

        self._init_repo()
        self._add_files()
        self._initial_commit()
        self._setup_remote()
        self._handle_branch_naming()
        self._sync_with_remote()

    def _is_git_repo(self) -> bool:
        return os.path.exists(os.path.join(self.project_dir, ".git"))

    def _init_repo(self):
        execute_command(['git', 'init'], self.project_dir)

    def _add_files(self):
        execute_command(['git', 'add', '.'], self.project_dir)

    def _initial_commit(self):
        if not self._has_changes():
            print("Aucun fichier à ajouter et à committer.")
            return
        execute_command(['git', 'commit', '-m', 'Initial commit'], self.project_dir)

    def _has_changes(self) -> bool:
        status = check_command_output(['git', 'status', '--porcelain'], self.project_dir)
        return bool(status)

    def _setup_remote(self):
        if not self._has_remote():
            print("Ajout du dépôt distant...")
            execute_command(['git', 'remote', 'add', 'origin', self.repo_url], self.project_dir)

    def _has_remote(self) -> bool:
        return check_command_output(['git', 'remote', 'show', 'origin'], self.project_dir) is not None

    def _handle_branch_naming(self):
        if self._has_local_master():
            execute_command(['git', 'branch', '-m', 'master', 'main'], self.project_dir)
        else:
            print("La branche 'master' n'existe pas localement. Ignorer le renommage.")

        if self._has_remote_master():
            execute_command(['git', 'push', 'origin', '--delete', 'master'], self.project_dir)
        else:
            print("La branche 'master' n'existe pas sur le dépôt distant. Ignorer la suppression.")

    def _has_local_master(self) -> bool:
        branches = check_command_output(['git', 'branch'], self.project_dir)
        return branches and 'master' in branches

    def _has_remote_master(self) -> bool:
        remote_branches = check_command_output(['git', 'ls-remote', '--heads', 'origin'], self.project_dir)
        return remote_branches and 'refs/heads/master' in remote_branches

    def _sync_with_remote(self):
        execute_command(['git', 'pull', 'origin', 'main', '--rebase'], self.project_dir)
        execute_command(['git', 'push', '-u', 'origin', 'main'], self.project_dir)

def main():
    project_dir = input("Enter directory path: ")
    repo_url = input("Enter Github repository URL: ")

    if not os.path.exists(project_dir):
        print(f"Le répertoire spécifié n'existe pas: {project_dir}")
        return

    try:
        repo = GitRepository(project_dir, repo_url)
        repo.initialize()
    except GitCommandError as e:
        print(f"Erreur Git: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
