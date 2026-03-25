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

if [[ ! -e "${git_file}" && "${current_bare}" == "true" && -z "${current_worktree}" ]]; then
  echo "dotfiles GUI mode is already disabled."
  git --git-dir="${repo_dir}" --work-tree="${HOME}" status --short --branch
  exit 0
fi

if [[ ! -f "${git_file}" ]]; then
  echo "${git_file} is missing or is not a gitfile; refusing to modify repo mode." >&2
  exit 1
fi

current_gitfile="$(<"${git_file}")"
if [[ "${current_gitfile}" != "${expected_gitfile}" ]]; then
  echo "${git_file} does not point to ${repo_dir}; refusing to remove it." >&2
  exit 1
fi

rm "${git_file}"
git --git-dir="${repo_dir}" config --unset core.worktree
git --git-dir="${repo_dir}" config core.bare true

echo "dotfiles GUI mode disabled."
git --git-dir="${repo_dir}" --work-tree="${HOME}" status --short --branch
