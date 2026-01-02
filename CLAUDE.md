# CLAUDE.md

# Amplifier Plugin Guidance
@plugins/amp/AMP_GUIDANCE.md

# Repository-Specific Instructions

This workspace contains the Amplifier plugin development environment.

## Structure

- **plugins/** - Claude Code plugins (source of truth for agents, commands, tools)
  - **amp/** - Core Amplifier plugin (23 agents, 12 commands, 18 tools, philosophies)
  - **git/** - Git workflow helpers
  - **dev-kit/** - SDLC toolkit
- **amplifier/** - Python package for amplifier CLI tools
- **tests/** - Test suites
- **docs/** - Documentation

## Development Notes

When working in this repository:
- Plugin files in `plugins/amp/` are the source of truth
- All @ references in plugins resolve within their directory
- Use `/amp:`, `/git:`, or `/dev-kit:` prefixed commands

## Git Safety Configuration

**IMPORTANT: This is a detached fork - never create PRs to the upstream repository.**

This repository has git safety measures configured in `.git-pr-config.json`:

- **Working branch**: `amplifier-claude` (all work happens here)
- **Target repository**: `kenotron-ms/amplifier` (this fork only)
- **Forbidden branches**: `main`, `master` (these are for merging from upstream only)

### Safety Measures in Place

1. **No upstream remote**: The `microsoft/amplifier` remote has been removed to prevent accidental pushes
2. **PR target enforcement**: The `/git:submit-pr` command reads `.git-pr-config.json` and:
   - Uses `--repo kenotron-ms/amplifier` for all `gh pr` commands
   - Uses `--base amplifier-claude` when creating PRs
   - Blocks PRs to `main` or `master` branches

### Working on This Repository

Always work on the `amplifier-claude` branch:
```bash
git checkout amplifier-claude
# Make changes
git commit -m "your changes"
git push origin amplifier-claude
```

To create a PR (which will automatically target `amplifier-claude` base):
```bash
/git:submit-pr
```
