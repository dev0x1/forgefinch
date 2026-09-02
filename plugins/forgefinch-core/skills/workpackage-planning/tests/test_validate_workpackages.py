#!/usr/bin/env python3
"""Integration tests for the strict workpackage YAML validator."""

from __future__ import annotations

import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = SKILL_ROOT / "scripts/validate_workpackages.py"


def schema3_record(
    *,
    package_status: str = "complete",
    implementation_status: str = "done",
    verification_status: str = "done",
    verification_kind: str = "verification",
    verification_check_status: str = "done",
    verification_check_required: str = "true",
    verification_notes: str = "Passed the package gate.",
) -> str:
    implementation_ac = "done" if implementation_status == "done" else "todo"
    implementation_check = "done" if implementation_status == "done" else "todo"
    verification_ac = "done" if verification_status == "done" else "todo"
    return textwrap.dedent(
        f"""\
        schema_version: 3
        id: WP-9000
        title: "Validator fixture"
        status: {package_status}
        owner: test
        goal: "Fixture is valid, verified by validator evidence, while preserving compatibility."
        scope:
          in:
            - "Validator behavior."
          out:
            - "Product behavior."
        slices:
          - id: WP-9000-S1
            kind: implementation
            title: "Implement"
            status: {implementation_status}
            summary: "Implement behavior."
            ac:
              - id: WP-9000-S1-AC1
                status: {implementation_ac}
                text: "Behavior exists."
            checks:
              - cmd: "focused-check"
                required: true
                status: {implementation_check}
                notes: "Focused check result."
            questions: []
            notes: []
            completion: []
          - id: WP-9000-S2
            kind: {verification_kind}
            title: "Verify"
            status: {verification_status}
            summary: "Close the complete goal."
            ac:
              - id: WP-9000-S2-AC1
                status: {verification_ac}
                text: "Complete goal and constraints pass."
            checks:
              - cmd: "whole-package-check"
                required: {verification_check_required}
                status: {verification_check_status}
                notes: "{verification_notes}"
            questions: []
            notes: []
            completion: []
        """
    )


def schema4_record(
    *,
    implementation_status: str = "done",
    quality_status: str = "done",
    quality_kind: str = "quality_review",
    quality_command: str = "just code-quality-review",
    verification_status: str = "done",
) -> str:
    package_status = (
        "complete"
        if {implementation_status, quality_status, verification_status} == {"done"}
        else "active"
    )
    implementation_ac = "done" if implementation_status == "done" else "todo"
    implementation_check = "done" if implementation_status == "done" else "todo"
    quality_ac = "done" if quality_status == "done" else "todo"
    quality_check = "done" if quality_status == "done" else "todo"
    verification_ac = "done" if verification_status == "done" else "todo"
    verification_check = "done" if verification_status == "done" else "todo"
    return textwrap.dedent(
        f"""\
        schema_version: 4
        id: WP-9000
        title: "Validator fixture"
        status: {package_status}
        owner: test
        goal: "Fixture is implemented, reviewed, and verified while preserving compatibility."
        scope:
          in:
            - "Validator behavior."
          out:
            - "Product behavior."
        slices:
          - id: WP-9000-S1
            kind: implementation
            title: "Implement"
            status: {implementation_status}
            summary: "Implement behavior."
            ac:
              - id: WP-9000-S1-AC1
                status: {implementation_ac}
                text: "Behavior exists."
            checks:
              - cmd: "focused-check"
                required: true
                status: {implementation_check}
                notes: "Focused check result."
            questions: []
            notes: []
            completion: []
          - id: WP-9000-S2
            kind: {quality_kind}
            title: "Review"
            status: {quality_status}
            summary: "Review the complete implementation delta."
            ac:
              - id: WP-9000-S2-AC1
                status: {quality_ac}
                text: "Findings-first review reports no unresolved defect."
            checks:
              - cmd: "{quality_command}"
                required: true
                status: {quality_check}
                notes: "Code-quality review result."
            questions: []
            notes: []
            completion: []
          - id: WP-9000-S3
            kind: verification
            title: "Verify"
            status: {verification_status}
            summary: "Close the complete goal."
            ac:
              - id: WP-9000-S3-AC1
                status: {verification_ac}
                text: "Complete goal and constraints pass."
            checks:
              - cmd: "whole-package-check"
                required: true
                status: {verification_check}
                notes: "Whole-package check result."
            questions: []
            notes: []
            completion: []
        """
    )


class ValidatorIntegrationTests(unittest.TestCase):
    def validate(self, content: str) -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "WP-9000-validator-fixture.yaml").write_text(content, encoding="utf-8")
            return subprocess.run(
                [sys.executable, str(VALIDATOR), str(root)],
                cwd=SKILL_ROOT,
                check=False,
                capture_output=True,
                text=True,
            )

    def test_accepts_schema_3_multi_slice_package(self) -> None:
        result = self.validate(schema3_record())
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_accepts_schema_4_package_with_mandatory_quality_review(self) -> None:
        result = self.validate(schema4_record())
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_rejects_schema_4_package_without_quality_review_kind(self) -> None:
        result = self.validate(schema4_record(quality_kind="implementation"))
        self.assertIn("workpackage_requires_quality_review", result.stderr)

    def test_rejects_schema_4_quality_review_without_required_gate(self) -> None:
        result = self.validate(schema4_record(quality_command="focused-check"))
        self.assertIn("quality_review_requires_code_quality_check", result.stderr)

    def test_rejects_schema_4_review_start_before_implementation_completion(self) -> None:
        result = self.validate(
            schema4_record(implementation_status="doing", quality_status="doing", verification_status="todo")
        )
        self.assertIn("quality_review_started_before_implementation_complete", result.stderr)

    def test_accepts_historical_schema_2_without_new_fields(self) -> None:
        record = schema3_record().replace("schema_version: 3", "schema_version: 2")
        record = record.replace("    kind: implementation\n", "")
        record = record.replace("    kind: verification\n", "")
        record = record.replace("        required: true\n", "")
        result = self.validate(record)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_rejects_missing_verification_slice(self) -> None:
        result = self.validate(schema3_record(verification_kind="implementation"))
        self.assertIn("multi_slice_package_requires_verification", result.stderr)

    def test_rejects_verification_start_before_implementation_completion(self) -> None:
        result = self.validate(
            schema3_record(
                package_status="active",
                implementation_status="doing",
                verification_status="doing",
                verification_check_status="todo",
            )
        )
        self.assertIn("verification_started_before_implementation_complete", result.stderr)

    def test_rejects_required_skipped_check_on_completion(self) -> None:
        result = self.validate(schema3_record(verification_check_status="skipped"))
        self.assertIn("complete_package_has_unfinished_required_check", result.stderr)

    def test_accepts_justified_non_required_skip(self) -> None:
        result = self.validate(
            schema3_record(
                verification_check_status="skipped",
                verification_check_required="false",
                verification_notes="Accessibility is not affected by this parser-only fixture.",
            )
        )
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
