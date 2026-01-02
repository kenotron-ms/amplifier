# Plugin-Based Configuration (DRY)

This repository uses its own **amp plugin** for all agents, commands, and philosophies, avoiding duplication.

## How It Works

### Self-Contained Configuration
The plugin is **automatically configured** via `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "amplifier-local": {
      "source": {
        "source": "directory",
        "path": "$CLAUDE_PROJECT_DIR"
      }
    }
  },
  "enabledPlugins": {
    "amp@amplifier-local": true
  }
}
```

- **No manual setup needed** - marketplace and plugin are declared in settings
- **Fully self-contained** - Uses `$CLAUDE_PROJECT_DIR` to reference this repo
- Installed from: Local directory (`plugins/amp/` in this repo)
- Location: `~/.claude/plugins/cache/amplifier-local/amp/1.0.0/`
- Enabled: Automatically via `enabledPlugins`
- **Works offline** - No GitHub dependency for local development

### Directory Structure

```
.claude/
├── settings.json          ← Repo-specific config (permissions, hooks, MCP)
├── tools/                 ← Repo-specific hook implementations
│   ├── hook_*.py
│   ├── memory_cli.py
│   └── ...
├── logs/                  ← Runtime logs
└── *.md                   ← Repo-specific documentation

~/.claude/plugins/cache/amplifier/amp/1.0.0/  ← PLUGIN (via marketplace)
├── agents/                ← All 30 agents
├── commands/              ← All 19 commands
├── philosophies/          ← All 6 philosophies
├── tools/                 ← Bundled tools (transcript_manager.py)
└── ai_context/            ← Supporting docs
```

## What's Repo-Specific (in `.claude/`)

**Keep these** - They're specific to this repository:
- `settings.json` - Permissions, hooks, MCP servers configuration
- `tools/` - Hook implementations (session_start, post_tool_use, etc.)
- `logs/` - Runtime logs and subagent tracking
- Documentation files - README.md, AGENT_PROMPT_INCLUDE.md, etc.

## What Comes from Plugin

**These are provided by the plugin** (don't duplicate):
- All agents (30 total: core, design, knowledge)
- All commands (19 total: core workflow, advanced, DDD)
- All philosophies (6 files)
- Bundled tools (transcript_manager.py)
- Supporting context (CONTRACT_SPEC_AUTHORING_GUIDE.md)

## Benefits of This Approach

1. **DRY (Don't Repeat Yourself)** - Single source of truth for agents/commands
2. **Dogfooding** - This repo uses its own plugin
3. **Easy Updates** - Update plugin code, all users get updates
4. **Consistent** - Same behavior across all projects using the plugin
5. **Portable** - Plugin can be used in any project

## Marketplace Configuration

Local marketplace is configured at:
- Marketplace definition: `.claude-plugin/marketplace.json`
- Plugin source: `plugins/amp/` directory

To install in other projects:
```bash
# Add this repo as marketplace
claude plugin marketplace add kenotron-ms/amplifier

# Install the plugin
claude plugin install amp@amplifier --scope project
```

## Development Workflow

When updating agents or commands:
1. Edit files in `plugins/amp/`
2. Changes are automatically picked up (plugin is installed from local directory)
3. No need to touch `.claude/agents/` or `.claude/commands/` (they don't exist!)

## Verification

Check plugin is working:
```bash
# Plugin is enabled in settings
cat .claude/settings.json | grep enabledPlugins

# Plugin files are accessible
ls ~/.claude/plugins/cache/amplifier/amp/1.0.0/agents/core/
ls ~/.claude/plugins/cache/amplifier/amp/1.0.0/commands/

# Agents and commands work via /amp: prefix
/amp:prime
/amp:ultrathink-task
```

## Notes

- Commands use `/amp:` prefix (e.g., `/amp:commit`, `/amp:ultrathink-task`)
- All Python commands use `uv` for portable execution
- Tools bundled with plugin are referenced via `${CLAUDE_PLUGIN_ROOT}`
