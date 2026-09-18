"""Integration tests using disposable repositories; no third-party packages."""
import pathlib
import subprocess
import tempfile
import unittest

SCRIPT = pathlib.Path(__file__).resolve().parents[1] / 'git-check.sh'


class GitCheckTests(unittest.TestCase):
    def run_tool(self, *args):
        return subprocess.run(['bash', str(SCRIPT), *map(str, args)],
                              capture_output=True, text=True)

    def git(self, repo, *args):
        return subprocess.run(['git', '-C', str(repo), *args], check=True,
                              capture_output=True, text=True)

    def test_help_and_extra_arguments(self):
        self.assertEqual(self.run_tool('--help').returncode, 0)
        self.assertEqual(self.run_tool('one', 'two').returncode, 2)

    def test_invalid_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            result = self.run_tool(directory)
            self.assertEqual(result.returncode, 1)
            self.assertIn('not inside a Git working tree', result.stderr)

    def test_empty_repository_with_spaces(self):
        with tempfile.TemporaryDirectory(prefix='git check ') as directory:
            self.git(directory, 'init')
            result = self.run_tool(directory)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn('No commits yet.', result.stdout)

    def test_changes_history_and_no_mutation(self):
        with tempfile.TemporaryDirectory(prefix='git check ') as directory:
            repo = pathlib.Path(directory)
            self.git(repo, 'init')
            file = repo / 'example.txt'
            file.write_text('first\n')
            self.git(repo, 'add', 'example.txt')
            self.git(repo, '-c', 'user.name=Test', '-c', 'user.email=test@example.com',
                     'commit', '-m', 'Initial example')
            file.write_text('first\nsecond\n')
            self.git(repo, 'add', 'example.txt')
            file.write_text('first\nsecond\nthird\n')
            before = self.git(repo, 'status', '--porcelain').stdout
            index_before = (repo / '.git' / 'index').read_bytes()
            result = self.run_tool(repo)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn('Initial example', result.stdout)
            self.assertIn('MM example.txt', result.stdout)
            self.assertEqual(result.stdout.count('example.txt |'), 2)
            self.assertEqual(before, self.git(repo, 'status', '--porcelain').stdout)
            self.assertEqual(index_before, (repo / '.git' / 'index').read_bytes())
            self.assertEqual(file.read_text(), 'first\nsecond\nthird\n')


if __name__ == '__main__':
    unittest.main()
