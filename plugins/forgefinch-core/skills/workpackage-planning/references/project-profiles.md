# Project Command Profiles

Select commands from the repository being changed. Read `AGENTS.md`, the root
task runner, package scripts, and CI configuration; never copy a command from
an unrelated example.

Record three roles in the workpackage:

- Workpackage validation: the repository-owned schema or metadata check.
- Quality review: the repository's findings-first review or quality command.
- Final verification: the broadest relevant build, lint, test, and integration
  commands that can run in the current environment.

Examples include `just quality`, `npm test`, `pnpm lint`, `cargo test`, or a
project-specific script, but examples are not defaults. If a required command
does not exist or cannot run, mark the check blocked and state what is needed.
