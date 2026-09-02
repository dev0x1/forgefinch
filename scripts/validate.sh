#!/usr/bin/env bash
set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1

repository_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
plugin_creator_root="${CODEX_PLUGIN_CREATOR_ROOT:-$HOME/.codex/skills/.system/plugin-creator}"
skill_creator_root="${CODEX_SKILL_CREATOR_ROOT:-$HOME/.codex/skills/.system/skill-creator}"
python_runtime=("${CODEX_PLUGIN_PYTHON:-python3}")

if ! "${python_runtime[@]}" -c 'import yaml' >/dev/null 2>&1; then
  if command -v uv >/dev/null 2>&1; then
    python_runtime=(uv run --with pyyaml python)
  else
    echo "Plugin validation requires Python with PyYAML or uv." >&2
    exit 1
  fi
fi

"${python_runtime[@]}" -m json.tool "$repository_root/.agents/plugins/marketplace.json" >/dev/null
"${python_runtime[@]}" -m json.tool "$repository_root/.claude-plugin/marketplace.json" >/dev/null
"${python_runtime[@]}" "$repository_root/scripts/validate_marketplace.py"

for plugin_path in "$repository_root"/plugins/*; do
  "${python_runtime[@]}" "$plugin_creator_root/scripts/validate_plugin.py" "$plugin_path"
  while IFS= read -r skill_path; do
    "${python_runtime[@]}" "$skill_creator_root/scripts/quick_validate.py" "$skill_path"
  done < <(find "$plugin_path/skills" -mindepth 1 -maxdepth 1 -type d -print | sort)
done

if [[ -n "${CLAUDE_BIN:-}" ]] || command -v claude >/dev/null 2>&1; then
  "$repository_root/scripts/validate-claude.sh"
fi

planning_skill="$repository_root/plugins/forgefinch-core/skills/workpackage-planning"
"${python_runtime[@]}" "$planning_skill/tests/test_workpackage_schema.py"
"${python_runtime[@]}" "$planning_skill/tests/test_validate_workpackages.py"

if find "$repository_root/plugins" -type d \( -name __pycache__ -o -name agents \) \
  ! -path '*/forgefinch-core/skills/*/agents' -print -quit | grep -q .; then
  echo "Unexpected generated cache or legacy agent metadata found." >&2
  exit 1
fi

if rg -n --hidden --glob '!scripts/validate.sh' \
  '(api[_-]?key|client[_-]?secret|private[_-]?key)[[:space:]]*[:=][[:space:]]*[^[:space:]]+' \
  "$repository_root/plugins"; then
  echo "Potential credential material found in plugin files." >&2
  exit 1
fi

git -C "$repository_root" diff --check
echo "Forgefinch plugin marketplace validation passed."
