#!/usr/bin/env bash

set -euo pipefail

repo_dir="${HOME}/.dotfiles"
git_file="${HOME}/.git"
expected_gitfile="gitdir: ${repo_dir}"

if [[ ! -d "${repo_dir}" ]]; then
  echo "dotfiles repo not found: ${repo_dir}" >&2
  exit 1
fi

if [[ -d "${git_file}" ]]; then
  echo "${git_file} is a directory; refusing to overwrite it." >&2
  exit 1
fi

if [[ -f "${git_file}" ]]; then
  current_gitfile="$(<"${git_file}")"
  if [[ "${current_gitfile}" != "${expected_gitfile}" ]]; then
    echo "${git_file} already exists and does not point to ${repo_dir}." >&2
    exit 1
  fi
fi

current_bare="$(git --git-dir="${repo_dir}" config --get core.bare || echo true)"
current_worktree="$(git --git-dir="${repo_dir}" config --get core.worktree || true)"

if [[ -f "${git_file}" && "${current_bare}" == "false" && "${current_worktree}" == ".." ]]; then
  echo "dotfiles GUI mode is already enabled."
  git -C "${HOME}" status --short --branch
  exit 0
fi

git --git-dir="${repo_dir}" config core.bare false
git --git-dir="${repo_dir}" config core.worktree ..
printf '%s\n' "${expected_gitfile}" > "${git_file}"

echo "dotfiles GUI mode enabled."
git -C "${HOME}" status --short --branch
