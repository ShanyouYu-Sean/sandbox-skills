#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_NAME="al-sites"

if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 is required" >&2
  exit 1
fi

if [ -n "${CODEX_HOME:-}" ]; then
  CODEX_DIR="${CODEX_HOME%/}"
else
  CODEX_DIR="${HOME}/.codex"
fi

SKILL_ROOT="${CODEX_DIR}/skills"
DEST="${SKILL_ROOT}/${SKILL_NAME}"

mkdir -p "${SKILL_ROOT}"
rm -rf "${DEST}"
cp -R "${REPO_ROOT}/skills/${SKILL_NAME}" "${DEST}"

python3 "${DEST}/scripts/install_mcp_config.py"

echo "Installed ${SKILL_NAME} to ${DEST}"
