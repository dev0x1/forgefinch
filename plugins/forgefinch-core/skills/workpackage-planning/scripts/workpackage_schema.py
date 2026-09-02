"""Parser-neutral semantic rules for workpackage schema versions."""

from __future__ import annotations

from typing import Any


LEGACY_SCHEMA_VERSION = 2
VERIFICATION_SCHEMA_VERSION = 3
QUALITY_REVIEW_SCHEMA_VERSION = 4
VERIFICATION_SLICE_KINDS = {"implementation", "verification"}
QUALITY_REVIEW_SLICE_KINDS = {"implementation", "quality_review", "verification"}
STARTED_STATUSES = {"doing", "done"}
OPEN_DEFECT_MARKER = "[defect-open]"
CODE_QUALITY_REVIEW_COMMANDS = {
    "just code-quality-review",
    "pnpm code-quality-review",
}


def validate_schema_contract(record: dict[str, Any]) -> list[str]:
    """Return stable semantic error codes for a parsed workpackage record."""

    schema_version = _integer(record.get("schema_version"))
    if schema_version == LEGACY_SCHEMA_VERSION:
        return []
    if schema_version not in {
        VERIFICATION_SCHEMA_VERSION,
        QUALITY_REVIEW_SCHEMA_VERSION,
    }:
        return ["unsupported_schema_version"]

    errors: list[str] = []
    slices = record.get("slices")
    if not isinstance(slices, list) or not slices:
        return [f"schema_v{schema_version}_requires_slices"]

    allowed_kinds = (
        VERIFICATION_SLICE_KINDS
        if schema_version == VERIFICATION_SCHEMA_VERSION
        else QUALITY_REVIEW_SLICE_KINDS
    )
    quality_review_indexes: list[int] = []
    verification_indexes: list[int] = []
    for index, slice_record in enumerate(slices):
        if not isinstance(slice_record, dict):
            errors.append(f"schema_v{schema_version}_slice_must_be_mapping")
            continue
        kind = slice_record.get("kind")
        if kind not in allowed_kinds:
            errors.append(f"schema_v{schema_version}_slice_kind_required")
        elif kind == "quality_review":
            quality_review_indexes.append(index)
        elif kind == "verification":
            verification_indexes.append(index)
        if (
            schema_version == QUALITY_REVIEW_SCHEMA_VERSION
            and kind == "implementation"
        ):
            if not _items(slice_record, "ac"):
                errors.append("implementation_slice_requires_acceptance")
            if not _items(slice_record, "checks"):
                errors.append("implementation_slice_requires_checks")
        for check in _items(slice_record, "checks"):
            if not isinstance(check, dict):
                errors.append(f"schema_v{schema_version}_check_must_be_mapping")
                continue
            if not isinstance(check.get("required"), bool):
                errors.append(f"schema_v{schema_version}_check_required_boolean")
            if check.get("required") is True and check.get("status") == "skipped":
                errors.append("required_check_cannot_be_skipped")
            if check.get("status") == "skipped" and not _skip_reason_is_concrete(check):
                errors.append("skipped_check_requires_reason")

        if (
            schema_version == QUALITY_REVIEW_SCHEMA_VERSION
            and slice_record.get("status") == "done"
        ):
            if any(_item_status(item) != "done" for item in _items(slice_record, "ac")):
                errors.append("done_slice_has_unfinished_acceptance")
            for check in _items(slice_record, "checks"):
                if not isinstance(check, dict):
                    errors.append("done_slice_has_unfinished_required_check")
                    continue
                if check.get("required") is True and check.get("status") != "done":
                    errors.append("done_slice_has_unfinished_required_check")
                if check.get("required") is False and not _optional_check_is_resolved(check):
                    errors.append("done_slice_has_unresolved_optional_check")
            if _items(slice_record, "questions"):
                errors.append("done_slice_has_open_questions")

    if schema_version == VERIFICATION_SCHEMA_VERSION:
        _validate_schema_v3_slice_order(slices, verification_indexes, errors)
    else:
        _validate_schema_v4_slice_order(
            slices,
            quality_review_indexes,
            verification_indexes,
            errors,
        )

    quality_review = next(
        (
            item
            for item in slices
            if isinstance(item, dict) and item.get("kind") == "quality_review"
        ),
        None,
    )
    if quality_review is not None:
        if not _items(quality_review, "ac"):
            errors.append("quality_review_slice_requires_acceptance")
        quality_checks = _items(quality_review, "checks")
        if not quality_checks:
            errors.append("quality_review_slice_requires_checks")
        if not any(
            isinstance(item, dict)
            and item.get("cmd") in CODE_QUALITY_REVIEW_COMMANDS
            and item.get("required") is True
            for item in quality_checks
        ):
            errors.append("quality_review_requires_code_quality_check")
        quality_index = slices.index(quality_review)
        if quality_review.get("status") in STARTED_STATUSES and not all(
            _slice_is_resolved(item) for item in slices[:quality_index]
        ):
            errors.append("quality_review_started_before_implementation_complete")

    verification = (
        slices[-1]
        if isinstance(slices[-1], dict)
        and slices[-1].get("kind") == "verification"
        else None
    )
    if verification is not None:
        if not _items(verification, "ac"):
            errors.append("verification_slice_requires_acceptance")
        if not _items(verification, "checks"):
            errors.append("verification_slice_requires_checks")
        if verification.get("status") in STARTED_STATUSES and not all(
            _slice_is_resolved(item) for item in slices[:-1]
        ):
            errors.append("verification_started_before_implementation_complete")

    if _has_open_defect(record):
        if record.get("status") == "complete" or any(
            _slice_kind(item) in {"quality_review", "verification"}
            and _item_status(item) in STARTED_STATUSES
            for item in slices
        ):
            errors.append("open_defect_requires_reopened_implementation")

    if record.get("status") == "complete":
        for slice_record in slices:
            if not isinstance(slice_record, dict):
                errors.append("complete_package_has_unfinished_slice")
                continue
            if slice_record.get("status") != "done":
                errors.append("complete_package_has_unfinished_slice")
            if any(_item_status(item) != "done" for item in _items(slice_record, "ac")):
                errors.append("complete_package_has_unfinished_acceptance")
            for check in _items(slice_record, "checks"):
                if not isinstance(check, dict):
                    errors.append("complete_package_has_unfinished_required_check")
                    continue
                if check.get("required") is True and check.get("status") != "done":
                    errors.append("complete_package_has_unfinished_required_check")
                if check.get("required") is False and check.get("status") not in {
                    "done",
                    "skipped",
                }:
                    errors.append("complete_package_has_unresolved_optional_check")
            if _items(slice_record, "questions"):
                errors.append("complete_package_has_open_questions")

    return _deduplicate(errors)


def _validate_schema_v3_slice_order(
    slices: list[Any],
    verification_indexes: list[int],
    errors: list[str],
) -> None:
    if len(slices) == 1:
        if _slice_kind(slices[0]) != "implementation":
            errors.append("one_slice_package_must_be_implementation")
        return

    if not verification_indexes:
        errors.append("multi_slice_package_requires_verification")
    elif len(verification_indexes) > 1:
        errors.append("multi_slice_package_has_duplicate_verification")
    if verification_indexes and verification_indexes[-1] != len(slices) - 1:
        errors.append("verification_slice_must_be_last")
    if any(_slice_kind(item) != "implementation" for item in slices[:-1]):
        errors.append("pre_verification_slices_must_be_implementation")


def _validate_schema_v4_slice_order(
    slices: list[Any],
    quality_review_indexes: list[int],
    verification_indexes: list[int],
    errors: list[str],
) -> None:
    if len(slices) < 3:
        errors.append("schema_v4_requires_implementation_review_and_verification")

    if not quality_review_indexes:
        errors.append("workpackage_requires_quality_review")
    elif len(quality_review_indexes) > 1:
        errors.append("workpackage_has_duplicate_quality_review")
    if quality_review_indexes and quality_review_indexes[-1] != len(slices) - 2:
        errors.append("quality_review_slice_must_be_penultimate")

    if not verification_indexes:
        errors.append("workpackage_requires_verification")
    elif len(verification_indexes) > 1:
        errors.append("workpackage_has_duplicate_verification")
    if verification_indexes and verification_indexes[-1] != len(slices) - 1:
        errors.append("verification_slice_must_be_last")

    if len(slices) >= 2 and any(
        _slice_kind(item) != "implementation" for item in slices[:-2]
    ):
        errors.append("pre_review_slices_must_be_implementation")


def _slice_kind(slice_record: Any) -> Any:
    return slice_record.get("kind") if isinstance(slice_record, dict) else None


def _item_status(item: Any) -> Any:
    return item.get("status") if isinstance(item, dict) else None


def _slice_is_resolved(slice_record: Any) -> bool:
    if not isinstance(slice_record, dict):
        return False
    if slice_record.get("status") != "done":
        return False
    if any(_item_status(item) != "done" for item in _items(slice_record, "ac")):
        return False
    for check in _items(slice_record, "checks"):
        if not isinstance(check, dict):
            return False
        if check.get("required") is True and check.get("status") != "done":
            return False
        if check.get("required") is False:
            if not _optional_check_is_resolved(check):
                return False
    return not _items(slice_record, "questions")


def _optional_check_is_resolved(check: dict[str, Any]) -> bool:
    return check.get("status") == "done" or (
        check.get("status") == "skipped" and _skip_reason_is_concrete(check)
    )


def _skip_reason_is_concrete(check: dict[str, Any]) -> bool:
    notes = str(check.get("notes", "")).strip()
    return len(notes) >= 12 and notes.lower() not in {"not applicable", "n/a", "pending."}


def _has_open_defect(record: dict[str, Any]) -> bool:
    return any(
        str(note).strip().lower().startswith(OPEN_DEFECT_MARKER)
        for slice_record in record.get("slices", [])
        if isinstance(slice_record, dict)
        for note in _items(slice_record, "notes") + _items(slice_record, "completion")
    )


def _items(record: dict[str, Any], key: str) -> list[Any]:
    value = record.get(key, [])
    return value if isinstance(value, list) else []


def _integer(value: Any) -> int | None:
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _deduplicate(values: list[str]) -> list[str]:
    return list(dict.fromkeys(values))
