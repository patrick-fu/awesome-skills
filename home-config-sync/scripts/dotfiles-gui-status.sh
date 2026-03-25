#!/usr/bin/env bash

set -euo pipefail

repo_dir="${HOME}/.dotfiles"
git_file="${HOME}/.git"
expected_gitfile="gitdir: ${repo_dir}"

if [[ ! -d "${repo_dir}" ]]; then
  echo "dotfiles repo not found: ${repo_dir}" >&2
  exit 1
fi

current_bare="$(git --git-dir="${repo_dir}" config --get core.bare || echo true)"
current_worktree="$(git --git-dir="${repo_dir}" config --get core.worktree || true)"

if [[ -f "${git_file}" ]]; then
  current_gitfile="$(<"${git_file}")"
  if [[ "${current_gitfile}" == "${expected_gitfile}" && "${current_bare}" == "false" && "${current_worktree}" == ".." ]]; then
    echo "enabled"
    git -C "${HOME}" status --short --branch
    exit 0
  fi

  echo "unexpected" >&2
  echo "${git_file} exists but does not match the expected GUI mode state." >&2
  exit 1
fi

if [[ -d "${git_file}" ]]; then
  echo "unexpected" >&2
  echo "${git_file} is a directory; refusing to treat this as GUI mode." >&2
  exit 1
fi

if [[ "${current_bare}" == "true" && -z "${current_worktree}" ]]; then
  echo "disabled"
  git --git-dir="${repo_dir}" --work-tree="${HOME}" status --short --branch
  exit 0
fi

echo "unexpected" >&2
echo "Repository config is partially switched." >&2
exit 1
