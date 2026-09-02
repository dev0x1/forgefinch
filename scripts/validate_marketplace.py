#!/usr/bin/env python3
"""Validate the Forgefinch marketplaces and public skill inventory."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CODEX_MARKETPLACE = ROOT / ".agents/plugins/marketplace.json"
CLAUDE_MARKETPLACE = ROOT / ".claude-plugin/marketplace.json"
EXPECTED = [
    ("forgefinch-core", 7, "0.1.0"),
    ("forgefinch-client", 21, "0.1.0"),
    ("forgefinch-backend", 66, "0.1.0"),
]
FORBIDDEN_COMPONENT_KEYS = {"apps", "hooks", "mcpServers"}
FORBIDDEN_PUBLIC_TEXT = re.compile(
    r"\x73\x6f\x66\x74\x77\x6f\x72\x6b\x65\x72"
    r"|\x73\x6f\x66\x74\x77\x6f\x72\x6b\x65\x72\x64"
    r"|\b\x73\x77-[a-z0-9]|\b\x73\x77\x63\x74\x6c\b"
    r"|apps/\x64\x65\x73\x6b"
    r"|apps/\x61\x64\x6d\x69\x6e-\x63\x65\x6e\x74\x65\x72",
    re.IGNORECASE,
)
SKILL_NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
MARKDOWN_LINK = re.compile(r"\[[^]]*]\(([^)]+)\)")


def load_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_relative_links(skill_root: Path, text: str) -> None:
    for raw_target in MARKDOWN_LINK.findall(text):
        target = raw_target.split("#", 1)[0].strip()
        if not target or "://" in target or target.startswith(("#", "mailto:")):
            continue
        if Path(target).suffix.lower() not in {
            ".md",
            ".yaml",
            ".yml",
            ".json",
            ".png",
            ".svg",
            ".py",
            ".sh",
        }:
            continue
        resolved = (skill_root / target).resolve()
        assert resolved.is_relative_to(skill_root.resolve()), (skill_root, target)
        assert resolved.is_file(), (skill_root, target)


def validate_public_tree() -> None:
    for path in ROOT.rglob("*"):
        if ".git" in path.parts or not path.is_file():
            continue
        relative = path.relative_to(ROOT)
        assert not FORBIDDEN_PUBLIC_TEXT.search(relative.as_posix()), relative
        if path.suffix.lower() in {".md", ".json", ".yaml", ".yml", ".py", ".sh", ".toml"}:
            text = path.read_text(encoding="utf-8")
            assert not FORBIDDEN_PUBLIC_TEXT.search(text), relative
            assert "[TO" "DO:" not in text, relative


def main() -> int:
    codex_catalog = load_json(CODEX_MARKETPLACE)
    claude_catalog = load_json(CLAUDE_MARKETPLACE)
    assert codex_catalog["name"] == claude_catalog["name"] == "forgefinch"
    assert codex_catalog["interface"]["displayName"] == "Forgefinch"
    assert claude_catalog["owner"] == {
        "name": "Forgefinch",
        "url": "https://github.com/dev0x1",
    }
    assert claude_catalog["version"] == "0.1.0"

    codex_entries = codex_catalog["plugins"]
    claude_entries = claude_catalog["plugins"]
    expected_names = [name for name, _, _ in EXPECTED]
    assert [entry["name"] for entry in codex_entries] == expected_names
    assert [entry["name"] for entry in claude_entries] == expected_names

    all_skill_names: set[str] = set()
    total_skills = 0
    for codex_entry, claude_entry, expected in zip(
        codex_entries, claude_entries, EXPECTED, strict=True
    ):
        plugin_name, expected_skill_count, version = expected
        expected_path = f"./plugins/{plugin_name}"
        assert codex_entry["source"] == {"source": "local", "path": expected_path}
        assert codex_entry["policy"] == {
            "installation": "AVAILABLE",
            "authentication": "ON_INSTALL",
        }
        assert codex_entry["category"] == "Developer Tools"
        assert claude_entry["source"] == expected_path
        assert claude_entry["version"] == version
        assert claude_entry["author"]["name"] == "Forgefinch"
        assert claude_entry["strict"] is True

        plugin_root = ROOT / "plugins" / plugin_name
        codex_manifest = load_json(plugin_root / ".codex-plugin/plugin.json")
        claude_manifest = load_json(plugin_root / ".claude-plugin/plugin.json")
        for manifest in (codex_manifest, claude_manifest):
            assert manifest["name"] == plugin_name
            assert manifest["version"] == version
            assert manifest["author"] == {
                "name": "Forgefinch",
                "url": "https://github.com/dev0x1",
            }
            assert manifest["repository"] == "https://github.com/dev0x1/forgefinch"
            assert manifest["license"] == "Apache-2.0"
        assert not FORBIDDEN_COMPONENT_KEYS.intersection(codex_manifest)
        assert {
            key: codex_manifest[key] for key in ("name", "version", "author")
        } == {
            key: claude_manifest[key] for key in ("name", "version", "author")
        }
        for asset_key in ("composerIcon", "logo", "logoDark"):
            asset_path = codex_manifest["interface"][asset_key]
            assert asset_path.startswith("./assets/")
            assert (plugin_root / asset_path.removeprefix("./")).is_file()

        skill_roots = sorted(
            path for path in (plugin_root / "skills").iterdir() if path.is_dir()
        )
        assert len(skill_roots) == expected_skill_count, (
            plugin_name,
            len(skill_roots),
            expected_skill_count,
        )
        for skill_root in skill_roots:
            skill_file = skill_root / "SKILL.md"
            assert skill_file.is_file(), skill_root
            skill_text = skill_file.read_text(encoding="utf-8")
            match = re.search(r"^name:\s*[\"']?([^\"'\n]+)", skill_text, re.MULTILINE)
            assert match is not None, skill_file
            declared_name = match.group(1).strip()
            assert declared_name == skill_root.name
            assert SKILL_NAME.fullmatch(declared_name)
            assert len(declared_name) < 64
            assert declared_name not in all_skill_names, declared_name
            all_skill_names.add(declared_name)
            validate_relative_links(skill_root, skill_text)

            metadata = skill_root / "agents/openai.yaml"
            if metadata.exists():
                metadata_text = metadata.read_text(encoding="utf-8")
                assert f"${declared_name}" in metadata_text, metadata
        total_skills += len(skill_roots)

    assert total_skills == 94
    assert not (ROOT / "plugins/forgefinch-client/skills/react-best-practices").exists()
    assert not (ROOT / "docs/workpackages").exists()
    validate_public_tree()

    print(
        "Forgefinch marketplace parity, public naming, unique skills, links, "
        "assets, and all 94 skills passed."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
