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
