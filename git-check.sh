#!/usr/bin/env bash
# Print a read-only overview of a Git repository.
set -euo pipefail

usage() {
    printf 'Usage: bash git-check.sh [repository-path]\n'
    printf 'Show Git status, unstaged/staged change summaries, and five recent commits.\n'
}

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
    usage
    exit 0
fi
if (( $# > 1 )); then
    usage >&2
    exit 2
fi
if ! command -v git >/dev/null 2>&1; then
    printf 'Error: Git is required.\n' >&2
    exit 1
fi

repo="${1:-.}"
if ! git -C "$repo" rev-parse --is-inside-work-tree 2>/dev/null | command grep -qx true; then
    printf 'Error: %s is not inside a Git working tree.\n' "$repo" >&2
    exit 1
fi

printf '\n== Status ==\n'
git -C "$repo" status --short --branch
printf '\n== Unstaged changes ==\n'
git -C "$repo" --no-pager diff --stat
printf '\n== Staged changes ==\n'
git -C "$repo" --no-pager diff --cached --stat
printf '\n== Recent commits (up to 5) ==\n'
if git -C "$repo" rev-parse --verify HEAD >/dev/null 2>&1; then
    git -C "$repo" --no-pager log -5 --oneline
else
    printf 'No commits yet.\n'
fi
