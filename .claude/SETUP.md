# Setting Up This Repository

This repository uses its own **amp plugin** for all agents, commands, and philosophies.

## For Team Members (Automatic Setup!)

When you clone this repository, the marketplace and plugin are **automatically configured**:

✅ Marketplace is declared in `.claude/settings.json` via `extraKnownMarketplaces`
✅ Plugin is enabled in `.claude/settings.json` via `enabledPlugins`

When you first open the project:
1. Claude Code will detect the marketplace configuration
2. You'll be prompted to trust and install the marketplace
3. The plugin will be automatically available

### Prerequisites

Install `uv` (Python package manager) for portable command execution:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

That's it! No manual plugin installation needed.

### Verify Installation (Optional)

```bash
# Check plugin is enabled (should see "amp@amplifier": true)
cat .claude/settings.json | grep enabledPlugins

# Check marketplace is configured
cat .claude/settings.json | grep extraKnownMarketplaces -A 7
```

## What You Get

Automatically available via the plugin:
- **30 agents** (core, design, knowledge)
- **19 commands** (core workflow, advanced, DDD)
- **6 philosophies** (implementation, design, modular)
- **Bundled tools** (transcript_manager.py)

All available via `/amp:` prefix, e.g.:
```bash
/amp:prime
/amp:ultrathink-task
/amp:designer
/amp:commit
/amp:ddd:0-help
```

## How It Works

The self-contained setup uses two key settings in `.claude/settings.json`:

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

- **`extraKnownMarketplaces`**: Points to this repo directory using `$CLAUDE_PROJECT_DIR`
- **`enabledPlugins`**: Activates the amp plugin automatically
- **Fully self-contained**: No external dependencies, works offline

This means **no manual marketplace/plugin installation** - it's all committed to the repo!

## For Repository Developers

If you're working on the plugin itself:

1. Edit files in `plugins/amp/` directory
2. Commit and push changes
3. Team members get updates on next `git pull` and Claude Code restart
4. Test commands with `/amp:` prefix

**Local Development**: For immediate testing without pushing:
```bash
# Temporarily use local plugin instead of GitHub
claude plugin marketplace add .
claude plugin install amp@amplifier --scope project
# Now your local plugins/amp/ is used
```

## Troubleshooting

### Commands failing with "not found"?
Ensure `uv` is installed and in PATH:
```bash
uv --version
```

### Want to use local plugin for development?
```bash
# Override the GitHub marketplace with local directory
claude plugin marketplace add .
# Reinstall plugin (will use local plugins/amp/)
claude plugin install amp@amplifier --scope project
```

### Need to force plugin update?
```bash
# Uninstall and reinstall
claude plugin uninstall amp@amplifier
claude plugin install amp@amplifier --scope project
```
