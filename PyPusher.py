import subprocess
import sys
from config import REPO_PATH, REMOTE_URL, COMMIT_MESSAGE

def run_command(command):
    try:
        subprocess.check_call(command)
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'exécution de git: {e}")
        sys.exit(1)

def check_output(command):
    try:
        return subprocess.check_output(command, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError:
        return None

def init_git_repo(repo_path, remote_url, commit_message):
    run_command(['git', '-C', repo_path, 'init'])
    run_command(['git', '-C', repo_path, 'add', '.'])
    run_command(['git', '-C', repo_path, 'commit', '-m', commit_message])
    
    if check_output(['git', '-C', repo_path, 'remote', 'show', 'origin']) is None:
        print("Le dépôt distant n'existe pas. Ajout du dépôt distant...")
        run_command(['git', '-C', repo_path, 'remote', 'add', 'origin', remote_url])

    run_command(['git', '-C', repo_path, 'push', '-u', 'origin', 'master'])

if __name__ == "__main__":
    init_git_repo(REPO_PATH, REMOTE_URL, COMMIT_MESSAGE)
