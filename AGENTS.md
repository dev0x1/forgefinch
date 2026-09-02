# Forgefinch Plugin Repository

This repository publishes one Codex and Claude Code marketplace backed by the
same three skill trees.

## Repository rules

- Keep plugin folders, identifiers, manifest names, authors, and versions in
  parity across both hosts.
- Use strict semantic versions and change only the plugin whose public behavior
  changes.
- Keep skill folder and frontmatter names identical, lowercase, hyphenated,
  unique across the marketplace, and shorter than 64 characters.
- Keep descriptions concise and useful for routing. Put conditional procedures
  in linked references.
- Keep skills repository-neutral. Discover project layout and commands from
  `AGENTS.md`, nearby code, and project-owned documentation instead of assuming
  a fixed checkout.
- Never add secrets, credentials, private endpoints, generated caches, personal
  agent configuration, or project-owned workpackage records.
- Core owns reusable workflow and schema-v4 workpackage behavior. Optional packs
  must not duplicate those skills.
- Installing a plugin never copies or merges project instructions.

## Required validation

Run `./scripts/validate.sh` before a release. When Claude Code is installed,
also run `CLAUDE_BIN=/path/to/claude ./scripts/validate-claude.sh`. Repository
validation must not register or install personal marketplaces.
