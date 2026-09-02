#!/usr/bin/env python3
"""Validate schema v2, v3, and v4 workpackage YAML records and specs."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any

from workpackage_schema import validate_schema_contract


WORKPACKAGE_ID_RE = re.compile(r"^WP-\d{4}$")
SLICE_ID_RE = re.compile(r"^(WP-\d{4})-S\d+$")
AC_ID_RE = re.compile(r"^(WP-\d{4}-S\d+)-AC\d+$")
TOP_LEVEL_RE = re.compile(r"^([a-z_]+):(.*)$")
NESTED_RE = re.compile(r"^  ([a-z_]+):(.*)$")
SCOPE_ITEM_RE = re.compile(r"^    -(?:\s+(.*))?$")
SLICE_ITEM_RE = re.compile(r"^  - id:\s*(.+?)\s*$")
SLICE_FIELD_RE = re.compile(r"^    ([a-z_]+):(?:\s*(.*))?$")
CHILD_ITEM_RE = re.compile(r"^      - (?:(id|cmd):\s*)?(.+?)\s*$")
CHILD_FIELD_RE = re.compile(r"^        ([a-z_]+):\s*(.+?)\s*$")

ALLOWED_TOP_LEVEL_KEYS = {
    "schema_version",
    "id",
    "title",
    "status",
    "owner",
    "spec_ref",
    "goal",
    "scope",
    "slices",
}
SLICE_KEYS = {
    "id",
    "kind",
    "title",
    "status",
    "summary",
    "ac",
    "checks",
    "questions",
    "notes",
    "completion",
}
AC_KEYS = {"id", "status", "text"}
CHECK_KEYS = {"cmd", "required", "status", "notes"}
WORKPACKAGE_STATUSES = {"planned", "active", "blocked", "paused", "complete"}
ITEM_STATUSES = {"todo", "doing", "done", "blocked", "skipped"}
REQUIRED_SLICE_KEYS = {"id", "title", "status", "summary", "ac", "checks", "questions", "notes", "completion"}


def strip_scalar(value: str) -> str:
    value = value.strip()
    if value == "[]":
        return value
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def parse_scalar(value: str) -> Any:
    stripped = strip_scalar(value)
    if stripped == "true":
        return True
    if stripped == "false":
        return False
    return stripped


def new_slice(slice_id: str) -> dict[str, Any]:
    return {"id": strip_scalar(slice_id), "ac": [], "checks": []}


def parse_workpackage_yaml(path: Path) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    record: dict[str, Any] = {"scope": {"in": [], "out": []}, "slices": []}
    section: str | None = None
    scope_list: str | None = None
    current_slice: dict[str, Any] | None = None
    child_list: str | None = None
    current_child: dict[str, str] | None = None

    for line_number, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        if "\t" in raw_line:
            errors.append(f"{path}:{line_number}: tabs are not allowed")
            continue
        if raw_line != raw_line.rstrip():
            errors.append(f"{path}:{line_number}: trailing whitespace")

        top_match = TOP_LEVEL_RE.match(raw_line)
        if top_match:
            key, value = top_match.groups()
            if key not in ALLOWED_TOP_LEVEL_KEYS:
                errors.append(f"{path}:{line_number}: unsupported top-level key `{key}`")
            section = key
            scope_list = None
            current_slice = None
            child_list = None
            current_child = None
            if value.strip():
                record[key] = strip_scalar(value)
            continue

        nested_match = NESTED_RE.match(raw_line)
        if nested_match and section == "scope":
            scope_list = nested_match.group(1)
            if scope_list not in {"in", "out"}:
                errors.append(f"{path}:{line_number}: unsupported scope key `{scope_list}`")
            continue

        scope_item = SCOPE_ITEM_RE.match(raw_line)
        if scope_item and section == "scope" and scope_list in {"in", "out"}:
            record["scope"][scope_list].append(strip_scalar(scope_item.group(1) or ""))
            continue

        slice_match = SLICE_ITEM_RE.match(raw_line)
        if slice_match and section == "slices":
            current_slice = new_slice(slice_match.group(1))
            record["slices"].append(current_slice)
            child_list = None
            current_child = None
            continue

        slice_field = SLICE_FIELD_RE.match(raw_line)
        if slice_field and section == "slices" and current_slice is not None:
            key, value = slice_field.groups()
            if key not in SLICE_KEYS:
                errors.append(f"{path}:{line_number}: unsupported slice key `{key}`")
            if key in {"ac", "checks", "questions", "notes", "completion"}:
                child_list = key
                current_child = None
                if value and value.strip() == "[]":
                    current_slice[key] = []
            else:
                current_slice[key] = strip_scalar(value or "")
                child_list = None
                current_child = None
            continue

        child_item = CHILD_ITEM_RE.match(raw_line)
        if child_item and current_slice is not None and child_list:
            keyed_field, value = child_item.groups()
            if child_list in {"ac", "checks"}:
                current_child = {}
                current_slice.setdefault(child_list, []).append(current_child)
                if keyed_field:
                    expected = "id" if child_list == "ac" else "cmd"
                    if keyed_field != expected:
                        errors.append(f"{path}:{line_number}: expected `{expected}` item under `{child_list}`")
                    current_child[keyed_field] = strip_scalar(value)
                else:
                    errors.append(f"{path}:{line_number}: expected keyed item under `{child_list}`")
                continue
            current_slice.setdefault(child_list, []).append(strip_scalar(value))
            current_child = None
            continue

        child_field = CHILD_FIELD_RE.match(raw_line)
        if child_field and current_child is not None and child_list in {"ac", "checks"}:
            key, value = child_field.groups()
            allowed = AC_KEYS if child_list == "ac" else CHECK_KEYS
            if key not in allowed:
                errors.append(f"{path}:{line_number}: unsupported `{child_list}` key `{key}`")
            current_child[key] = parse_scalar(value)
            continue

        errors.append(f"{path}:{line_number}: unsupported YAML shape")

    return record, errors


def validate_workpackage(yaml_path: Path) -> list[str]:
    errors: list[str] = []
    record, parse_errors = parse_workpackage_yaml(yaml_path)
    errors.extend(parse_errors)

    required = ["schema_version", "id", "title", "status", "owner", "goal", "scope", "slices"]
    for key in required:
        if key not in record or record[key] is None or record[key] == "":
            errors.append(f"{yaml_path}: missing `{key}`")

    schema_version = str(record.get("schema_version"))
    if schema_version not in {"2", "3", "4"}:
        errors.append(f"{yaml_path}: schema_version must be 2, 3, or 4")
    workpackage_id = str(record.get("id", ""))
    if not WORKPACKAGE_ID_RE.match(workpackage_id):
        errors.append(f"{yaml_path}: id must match `WP-0000` style")
        return errors
    if not yaml_path.name.startswith(workpackage_id):
        errors.append(f"{yaml_path}: filename must start with `{workpackage_id}`")
    if record.get("status") not in WORKPACKAGE_STATUSES:
        errors.append(f"{yaml_path}: invalid status `{record.get('status')}`")
    spec_ref = str(record.get("spec_ref", "")).strip()
    if spec_ref:
        if Path(spec_ref).name != spec_ref or "/" in spec_ref or "\\" in spec_ref:
            errors.append(f"{yaml_path}: spec_ref must be a colocated filename")
        elif not spec_ref.startswith(f"{workpackage_id}-") or not spec_ref.endswith(".spec.md"):
            errors.append(
                f"{yaml_path}: spec_ref must start with `{workpackage_id}-` "
                "and end with `.spec.md`"
            )
        elif not yaml_path.with_name(spec_ref).exists():
            errors.append(f"{yaml_path}: spec_ref `{spec_ref}` does not exist")
    if not record.get("scope", {}).get("in"):
        errors.append(f"{yaml_path}: scope.in must contain at least one item")
    if not record.get("scope", {}).get("out"):
        errors.append(f"{yaml_path}: scope.out must contain at least one item")

    seen_slices: set[str] = set()
    for slice_record in record.get("slices", []):
        slice_id = str(slice_record.get("id", ""))
        missing_keys = REQUIRED_SLICE_KEYS - set(slice_record)
        for key in sorted(missing_keys):
            errors.append(f"{yaml_path}: slice `{slice_id or '<missing>'}` missing `{key}`")
        if slice_id in seen_slices:
            errors.append(f"{yaml_path}: duplicate slice id `{slice_id}`")
        seen_slices.add(slice_id)
        if not slice_id.startswith(f"{workpackage_id}-"):
            errors.append(f"{yaml_path}: slice `{slice_id}` must start with `{workpackage_id}-`")
        if not SLICE_ID_RE.match(slice_id):
            errors.append(f"{yaml_path}: slice `{slice_id}` must match `WP-0000-S1` style")
        if slice_record.get("status") not in ITEM_STATUSES:
            errors.append(f"{yaml_path}: slice `{slice_id}` has invalid status `{slice_record.get('status')}`")
        if not slice_record.get("summary"):
            errors.append(f"{yaml_path}: slice `{slice_id}` missing summary")
        if not slice_record.get("ac"):
            errors.append(f"{yaml_path}: slice `{slice_id}` must contain at least one acceptance criterion")
        for criterion in slice_record.get("ac", []):
            criterion_id = str(criterion.get("id", ""))
            if not AC_ID_RE.match(criterion_id):
                errors.append(f"{yaml_path}: criterion `{criterion_id}` must match `WP-0000-S1-AC1` style")
            if not criterion_id.startswith(f"{slice_id}-"):
                errors.append(f"{yaml_path}: criterion `{criterion_id}` must start with `{slice_id}-`")
            if criterion.get("status") not in ITEM_STATUSES:
                errors.append(f"{yaml_path}: criterion `{criterion_id}` has invalid status `{criterion.get('status')}`")
            if not criterion.get("text"):
                errors.append(f"{yaml_path}: criterion `{criterion_id}` missing text")
        for check in slice_record.get("checks", []):
            if not check.get("cmd"):
                errors.append(f"{yaml_path}: slice `{slice_id}` contains check without cmd")
            if check.get("status") not in ITEM_STATUSES:
                errors.append(f"{yaml_path}: check `{check.get('cmd')}` has invalid status `{check.get('status')}`")
            if "notes" not in check:
                errors.append(f"{yaml_path}: check `{check.get('cmd')}` missing notes")

    for error_code in validate_schema_contract(record):
        errors.append(f"{yaml_path}: {error_code}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "root",
        nargs="?",
        default="docs/workpackages",
        help="workpackages directory to validate",
    )
    args = parser.parse_args()
    root = Path(args.root)
    errors: list[str] = []
    if not root.exists():
        errors.append(f"{root}: directory does not exist")
    else:
        for markdown_record in sorted(root.glob("WP-*.md")):
            if markdown_record.name.endswith(".spec.md"):
                continue
            errors.append(
                f"{markdown_record}: legacy top-level Markdown record is not allowed; "
                "use a colocated `.spec.md` companion file"
            )
        for legacy_folder in sorted(path for path in root.iterdir() if path.is_dir() and path.name.startswith("WP-")):
            errors.append(f"{legacy_folder}: legacy nested workpackage directory is not allowed")
        for yaml_path in sorted(root.glob("*.yaml")):
            if not yaml_path.name.startswith("WP-"):
                errors.append(f"{yaml_path}: workpackage YAML filename must start with `WP-`")
                continue
            errors.extend(validate_workpackage(yaml_path))
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print(f"Validated schema v2/v3/v4 workpackage records under {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
