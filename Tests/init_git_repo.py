import unittest
from unittest.mock import patch, call
import subprocess

from PyPusher import init_git_repo
from config import REPO_PATH, REMOTE_URL, COMMIT_MESSAGE

class TestInitGitRepo(unittest.TestCase):

    @patch('subprocess.check_call')
    @patch('subprocess.check_output')
    def test_init_git_repo(self, mock_check_output, mock_check_call):
        # Simuler l'absence du dépôt distant
        mock_check_output.side_effect = subprocess.CalledProcessError(1, 'git')

        init_git_repo(REPO_PATH, REMOTE_URL, COMMIT_MESSAGE)

        # Vérifier que les appels subprocess ont été faits avec les bons arguments
        expected_calls = [
            call(['git', '-C', REPO_PATH, 'init']),
            call(['git', '-C', REPO_PATH, 'add', '.']),
            call(['git', '-C', REPO_PATH, 'commit', '-m', COMMIT_MESSAGE]),
            # call(['git', '-C', REPO_PATH, 'remote', 'show', 'origin'], stderr=subprocess.STDOUT),
            call(['git', '-C', REPO_PATH, 'remote', 'add', 'origin', REMOTE_URL]),
            call(['git', '-C', REPO_PATH, 'push', '-u', 'origin', 'master'])
        ]
        mock_check_call.assert_has_calls(expected_calls)

    @patch('subprocess.check_call')
    @patch('subprocess.check_output')
    def test_remote_already_exists(self, mock_check_output, mock_check_call):
        # Simuler l'existence du dépôt distant
        mock_check_output.return_value = 'origin'

        init_git_repo(REPO_PATH, REMOTE_URL, COMMIT_MESSAGE)

        # Vérifier que le dépôt distant n'est pas ajouté à nouveau
        unexpected_call = call(['git', '-C', REPO_PATH, 'remote', 'add', 'origin', REMOTE_URL])
        self.assertNotIn(unexpected_call, mock_check_call.mock_calls)

if __name__ == '__main__':
    unittest.main()
