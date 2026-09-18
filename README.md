# git-check

## Section 1 — Command Description

`git-check` gives a quick, read-only overview of a Git repository: its branch and file status, separate summaries of unstaged and staged changes, and its five most recent commits. It does not add, commit, delete, or push files.

### How to run it

Requirements: Bash and Git (macOS, Linux, or Git Bash on Windows).

Download or clone this repository, open its folder in a terminal, and run:

```bash
# Inspect the current folder
bash git-check.sh

# Inspect another repository (quote paths containing spaces)
bash git-check.sh "/path/to/my repository"

# Show usage
bash git-check.sh --help
```

The default path is the terminal's current directory. Invalid paths and folders outside a Git working tree produce an error. Repositories without commits show `No commits yet.`

### Commands it combines

| Command | Purpose |
| --- | --- |
| `git status --short --branch` | Show the branch and changed/untracked files |
| `git diff --stat` | Summarize tracked changes that are not staged |
| `git diff --cached --stat` | Summarize staged changes |
| `git log -5 --oneline` | Show up to five recent commits |

Each command uses `git -C` to inspect the requested folder. `git rev-parse` validates the working tree and checks whether a first commit exists. `--no-pager` keeps output in the terminal. Untracked files appear in status but do not appear in diff summaries.

### Design and validation

The script uses labeled sections so the output is easy to read. Quoted arguments handle spaces in paths. Staged and unstaged summaries are separate because they describe different versions of a file. The tool intentionally avoids network commands and changing repository contents.

Optional integration tests require Python 3:

```bash
python3 -m unittest discover -s tests -v
```

The tests create temporary repositories and cover help, invalid arguments, invalid folders, paths with spaces, a repository without commits, staged/unstaged changes, history, and preservation of file/index contents.

## Section 2 — AI-Assisted Programming

### What I asked AI

I asked Codex to finish the work, directly access my GitHub, create a public repository, upload the code, and write the required README.

### Where AI helped

Codex selected this small command-line tool, wrote the Bash implementation, wrote the integration tests, prepared this README, and assisted with GitHub publishing. This includes substantial AI-generated programming, beyond learning Git commands or following setup instructions.

### Where I had to think independently

I supplied the assignment requirements and requested the work. The implementation and design decisions in this version were made by AI; I cannot honestly claim independent coding or debugging that I did not perform. I still need to understand the script and determine whether this amount of AI assistance is allowed by the assignment before submitting it.

### What AI got wrong or missed

AI could not assume access to my GitHub: the GitHub CLI was unavailable and the available browser was signed out. AI also cannot establish that I understand the code or that a fully generated solution complies with the assignment's AI rules. The solution makes a scope assumption because the provided instructions did not specify a particular tool to build.
