#!/usr/bin/env bash
set -euo pipefail

repository_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
claude_bin="${CLAUDE_BIN:-}"

if [[ -z "$claude_bin" ]]; then
  claude_bin="$(command -v claude || true)"
fi
if [[ -z "$claude_bin" || ! -x "$claude_bin" ]]; then
  echo "Claude validation requires CLAUDE_BIN or a claude executable on PATH." >&2
  exit 1
fi

"$claude_bin" plugin validate --strict "$repository_root"
for plugin_path in "$repository_root"/plugins/*; do
  "$claude_bin" plugin validate --strict "$plugin_path"
done

echo "Claude Code marketplace and plugin validation passed."
