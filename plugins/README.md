# Amplifier Plugins

This directory contains modular Claude Code plugins for the Amplifier workspace. Each plugin is independently registered and can be enabled/disabled separately.

## Plugin Structure

### 🎯 amp
**Main Amplifier plugin** - Core development philosophy, universal agents, and workflows

- **Agents**: 23 specialized agents (core, design, knowledge domains)
  - Core: zen-architect, modular-builder, bug-hunter, test-coverage, etc.
  - Design: component-designer, layout-architect, art-director, etc.
  - Knowledge: concept-extractor, insight-synthesizer, knowledge-archaeologist, etc.
- **Commands**: DDD workflow, code review, planning, transcript management
- **Philosophies**: Implementation & modular design philosophy documents
- **Hooks**: Git hook utilities and templates
- **Tools**: Transcript manager and other utilities

### 🔧 git
**Git workflow plugin** - Intelligent version control helpers

- **Commands**:
  - `/git:commit` - Create well-formatted commits with standards discovery
  - `/git:pull` - Sync feature branches with intelligent conflict resolution
  - `/git:submit-pr` - Autonomous PR creation and submission workflow
- **Skills**: PR submission auto-trigger

### 🏗️ dev-kit
**SDLC toolkit plugin** - Structured feature development workflow

- **Commands**: 9-phase TDD/SDLC workflow
  - `/dev-kit:new-feature` - Complete workflow orchestrator
  - `/dev-kit:new-feature:0-discover` through `8-cleanup` - Individual phases
  - `/dev-kit:new-feature:status` - Track progress across phases

## Installation

All plugins are automatically registered in `.claude-plugin/marketplace.json` at the workspace root.

## @ Reference Resolution

All plugins can reference workspace files using @ syntax:
- `@ai_context/IMPLEMENTATION_PHILOSOPHY.md` - Resolves from workspace root
- `@AGENTS.md` - Resolves from workspace root
- `@CLAUDE.md` - Resolves from workspace root

## Plugin Independence

Each plugin:
- Has its own `.claude-plugin/plugin.json` manifest
- Can be independently enabled/disabled
- Maintains separate command namespaces
- References shared workspace context via @ syntax

## Adding New Plugins

1. Create directory in `plugins/[name]/`
2. Add `.claude-plugin/plugin.json` manifest
3. Register in workspace `.claude-plugin/marketplace.json`
4. Add commands, agents, or other assets
5. Use @ syntax for workspace file references
