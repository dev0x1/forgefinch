#!/usr/bin/env python3
"""Focused contract tests for workpackage schema v3 and v4 semantics."""

from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
MODULE_PATH = ROOT.parent / "scripts" / "workpackage_schema.py"
FIXTURE_PATH = ROOT / "fixtures" / "verification-slice-cases.json"
SPEC = importlib.util.spec_from_file_location("workpackage_schema", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
validate_schema_contract = MODULE.validate_schema_contract


def check(status: str = "done", required: bool = True, notes: str = "Passed locally.") -> dict:
    return {"cmd": "focused-check", "required": required, "status": status, "notes": notes}


def criterion(status: str = "done") -> dict:
    return {"id": "WP-9000-S1-AC1", "status": status, "text": "Prove the package goal."}


def implementation(status: str = "done") -> dict:
    return {
        "id": "WP-9000-S1",
        "kind": "implementation",
        "status": status,
        "ac": [criterion("done" if status == "done" else "doing")],
        "checks": [check("done" if status == "done" else "todo")],
        "questions": [],
        "notes": [],
        "completion": [],
    }


def verification(status: str = "done") -> dict:
    return {
        "id": "WP-9000-S2",
        "kind": "verification",
        "status": status,
        "ac": [criterion("done" if status == "done" else "todo")],
        "checks": [check("done" if status == "done" else "todo")],
        "questions": [],
        "notes": [],
        "completion": [],
    }


def quality_review(status: str = "done") -> dict:
    return {
        "id": "WP-9000-S2",
        "kind": "quality_review",
        "status": status,
        "ac": [criterion("done" if status == "done" else "todo")],
        "checks": [
            {
                "cmd": "just code-quality-review",
                "required": True,
                "status": "done" if status == "done" else "todo",
                "notes": "Passed the findings-first code-quality review.",
            }
        ],
        "questions": [],
        "notes": [],
        "completion": [],
    }


def base_record() -> dict:
    return {
        "schema_version": 3,
        "status": "complete",
        "slices": [implementation(), verification()],
    }


def schema4_record() -> dict:
    return {
        "schema_version": 4,
        "status": "complete",
        "slices": [implementation(), quality_review(), verification()],
    }


def record_for(name: str) -> dict:
    if name.startswith("v4_") or name == "valid_schema_4":
        record = schema4_record()
        if name == "valid_schema_4":
            return record
        if name == "v4_missing_quality_review":
            record["slices"][1]["kind"] = "implementation"
        elif name == "v4_duplicate_quality_review":
            record["slices"] = [implementation(), quality_review(), quality_review(), verification()]
        elif name == "v4_review_placed_early":
            record["slices"] = [quality_review(), implementation(), verification()]
        elif name == "v4_review_started_early":
            record["status"] = "active"
            record["slices"] = [implementation("doing"), quality_review("doing"), verification("todo")]
        elif name == "v4_missing_quality_gate":
            record["slices"][1]["checks"] = [check()]
        elif name == "v4_implementation_without_checks":
            record["status"] = "active"
            record["slices"][0]["status"] = "doing"
            record["slices"][0]["checks"] = []
            record["slices"][1] = quality_review("todo")
            record["slices"][2] = verification("todo")
        elif name == "v4_done_review_with_unfinished_gate":
            record["status"] = "active"
            record["slices"][1]["checks"][0]["status"] = "todo"
            record["slices"][2] = verification("todo")
        elif name == "v4_required_check_skipped_while_active":
            record["status"] = "active"
            record["slices"][0] = implementation("doing")
            record["slices"][0]["checks"][0] = check(
                "skipped", True, "The required environment is currently unavailable."
            )
            record["slices"][1] = quality_review("todo")
            record["slices"][2] = verification("todo")
        elif name == "v4_done_slice_with_open_question":
            record["status"] = "active"
            record["slices"][0]["questions"] = ["Which owner closes this dependency?"]
            record["slices"][1] = quality_review("todo")
            record["slices"][2] = verification("todo")
        elif name == "v4_done_slice_with_unfinished_acceptance":
            record["status"] = "active"
            record["slices"][0]["ac"][0]["status"] = "todo"
            record["slices"][1] = quality_review("todo")
            record["slices"][2] = verification("todo")
        elif name == "v4_verification_started_before_review":
            record["status"] = "active"
            record["slices"] = [implementation(), quality_review("todo"), verification("doing")]
        elif name == "v4_non_mapping_check":
            record["slices"][0]["checks"] = [None]
        else:
            raise AssertionError(f"No record builder for case {name}")
        return record

    record = base_record()
    if name == "legacy_schema_2":
        return {"schema_version": 2, "status": "complete", "slices": [{"status": "done"}]}
    if name == "valid_one_slice":
        return {"schema_version": 3, "status": "complete", "slices": [implementation()]}
    if name == "valid_justified_optional_skip":
        record["slices"][0]["checks"].append(
            check("skipped", False, "Accessibility is not affected by this parser-only change.")
        )
    elif name == "valid_marker_documentation":
        record["slices"][-1]["completion"] = [
            "Documented the [defect-open] evidence prefix for future delivery records."
        ]
    elif name == "valid_reopened_implementation":
        record["status"] = "active"
        record["slices"][0] = implementation("doing")
        record["slices"][1] = verification("todo")
    elif name in {
        "valid_multi_slice",
        "valid_public_api_package",
        "valid_external_service_package",
        "valid_database_package",
        "valid_desktop_package",
    }:
        pass
    elif name == "missing_verification":
        record["slices"][1]["kind"] = "implementation"
    elif name == "duplicate_verification":
        record["slices"] = [verification(), verification()]
    elif name == "verification_placed_early":
        record["slices"] = [verification(), implementation()]
    elif name == "empty_verification_acceptance":
        record["slices"][-1]["ac"] = []
    elif name == "empty_verification_checks":
        record["slices"][-1]["checks"] = []
    elif name == "blocked_implementation_dependency":
        record["status"] = "active"
        record["slices"][0] = implementation("blocked")
        record["slices"][1] = verification("doing")
    elif name in {"unfinished_acceptance_on_complete", "unmet_goal_constraint"}:
        record["slices"][-1]["ac"][0]["status"] = "todo"
    elif name == "missing_required_test_layer":
        record["slices"][-1]["checks"][0] = check("todo", True, "Required integration layer has no evidence.")
    elif name == "required_check_skipped":
        record["slices"][-1]["checks"][0] = check("skipped", True, "Required environment unavailable.")
    elif name == "required_check_blocked":
        record["slices"][-1]["checks"][0] = check("blocked", True, "Required environment unavailable.")
    elif name == "optional_skip_without_reason":
        record["slices"][-1]["checks"][0] = check("skipped", False, "N/A")
    elif name == "open_defect_hidden_in_verification":
        record["slices"][-1]["notes"] = ["[defect-open] Integrated save still loses data."]
    else:
        raise AssertionError(f"No record builder for case {name}")
    return record


def main() -> int:
    catalog = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert catalog["schema_version"] == 1
    names = [case["name"] for case in catalog["cases"]]
    assert len(names) == len(set(names))
    for case in catalog["cases"]:
        errors = validate_schema_contract(copy.deepcopy(record_for(case["name"])))
        if case["valid"]:
            assert errors == [], f"{case['name']} unexpectedly failed: {errors}"
        else:
            assert case["error"] in errors, f"{case['name']} errors were {errors}"
    client_record = schema4_record()
    client_record["slices"][1]["checks"][0]["cmd"] = "pnpm code-quality-review"
    assert validate_schema_contract(client_record) == []
    print(f"Validated {len(names)} workpackage schema semantic cases.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
