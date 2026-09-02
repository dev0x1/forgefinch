# Forgefinch

Forgefinch is an open-source software-engineering skill marketplace for Codex
and Claude Code. Both hosts consume the same skill implementations.

## Choose your plugins

| Plugin | Purpose | Skills |
| --- | --- | ---: |
| `forgefinch-core` | General planning, acceptance criteria, implementation, review, verification, and schema-v4 workpackages | 7 |
| `forgefinch-client` | Optional Electron, React, Next.js, TypeScript, accessibility, testing, and desktop local-runtime guidance | 21 |
| `forgefinch-backend` | Optional Rust services, APIs, persistence, security, infrastructure, testing, and agentic-system guidance | 66 |

Install Core plus the optional pack that matches the repository. The packs do
not copy project instructions into a checkout: repository-specific rules and
commands remain in that project's `AGENTS.md`.

Vercel's `react-best-practices` skill is intentionally not vendored. Install
its current upstream version separately from `vercel-labs/agent-skills` when
you want that supplemental guidance.

## Install from GitHub

### Codex

```bash
codex plugin marketplace add dev0x1/forgefinch@v0.1.0
codex plugin add forgefinch-core@forgefinch
codex plugin add forgefinch-client@forgefinch   # optional client pack
codex plugin add forgefinch-backend@forgefinch  # optional backend pack
```

The `owner/repository@tag` form pins the marketplace to a published release.
Confirm that `forgefinch` appears in `codex plugin marketplace list` before
installing plugins; a failed marketplace registration leaves no plugin
inventory for the subsequent `plugin add` commands.

Start a fresh Codex task after installation or an upgrade so newly installed
skills are discovered.

### Claude Code

```bash
claude plugin marketplace add dev0x1/forgefinch
claude plugin install forgefinch-core@forgefinch --scope user
claude plugin install forgefinch-client@forgefinch --scope user   # optional
claude plugin install forgefinch-backend@forgefinch --scope user  # optional
```

Restart Claude Code after installation or an update. If activation is pending,
run `/reload-plugins`; use `/reload-plugins --force` when Claude warns that it
will reread the conversation.

## Invoke skills

Codex can select installed skills from their descriptions or accept an explicit
generic skill name:

```text
Use $workpackage-planning to plan this change.
Use $electron-dev to review this desktop boundary.
Use $service-integration to plan this backend dependency.
```

Claude uses the plugin namespace for explicit slash commands:

```text
/forgefinch-core:workpackage-planning
/forgefinch-client:electron-dev
/forgefinch-backend:service-integration
```

## Optional React guidance

```bash
npx skills add vercel-labs/agent-skills --skill react-best-practices -g \
  -a claude-code -a codex -y
```

## Local development

From the repository root, register the unpublished checkout:

```bash
codex plugin marketplace add "$PWD"
codex plugin add forgefinch-core@forgefinch
codex plugin add forgefinch-client@forgefinch
codex plugin add forgefinch-backend@forgefinch

claude plugin marketplace add "$PWD"
claude plugin install forgefinch-core@forgefinch --scope user
claude plugin install forgefinch-client@forgefinch --scope user
claude plugin install forgefinch-backend@forgefinch --scope user
```

Validate the complete marketplace:

```bash
./scripts/validate.sh
CLAUDE_BIN="$(command -v claude)" ./scripts/validate-claude.sh
```

Claude can also load an unpublished plugin directly:

```bash
claude --plugin-dir ./plugins/forgefinch-core \
  --plugin-dir ./plugins/forgefinch-backend
```

## Workpackages

Core includes reusable schema-v4 templates, semantic validation, and workflow
guidance. Adopt the shared `AGENTS.md` template explicitly, then keep actual
workpackage records, specifications, commands, and product rules in the
project repository.

## License

Copyright 2026 Forgefinch. Licensed under Apache-2.0; see `LICENSE`.
