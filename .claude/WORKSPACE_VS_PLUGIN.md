# Workspace vs Plugin Files (DRY Strategy)

## Overview

This workspace contains **both** the development environment AND the distributable plugins. To maintain DRY (Don't Repeat Yourself), we use **single source of truth** in the plugin directory.

## File Organization (Single Source of Truth)

### Source of Truth: Plugin Directory
```
/workspace/amp/plugins/amp/
├── ai_context/          # ← ONLY copy (source of truth)
├── tools/               # ← ONLY copy (source of truth)
├── AGENTS.md            # ← ONLY copy (source of truth)
├── CLAUDE.md            # ← ONLY copy (source of truth, @ refs for plugin)
├── DISCOVERIES.md       # ← ONLY copy (source of truth)
└── ...
```

### Workspace Root: Reference Files
```
/workspace/amp/
├── CLAUDE.md            # ← References @plugins/amp/CLAUDE.md
├── AGENTS.md            # ← References @plugins/amp/AGENTS.md
├── DISCOVERIES.md       # ← References @plugins/amp/DISCOVERIES.md
├── amplifier/           # ← Python package (separate)
├── scenarios/           # ← CLI tool examples (separate)
└── tests/               # ← Tests (separate)
```

## DRY Rules (Single Source of Truth)

### Development Workflow

1. **Edit plugin files directly** in `plugins/amp/` for ALL changes
2. **Workspace root files are thin references** that point to plugin files
3. **No duplication** - files only exist in plugins/amp/

### Where to Edit

**Plugin guidance, agents, philosophy:**
- ✅ Edit: `plugins/amp/CLAUDE.md`
- ✅ Edit: `plugins/amp/AGENTS.md`
- ✅ Edit: `plugins/amp/DISCOVERIES.md`
- ✅ Edit: `plugins/amp/philosophies/*.md`
- ✅ Edit: `plugins/amp/agents/**/*.md`
- ✅ Edit: `plugins/amp/tools/*.py`

**Workspace-specific:**
- Edit: `amplifier/` (Python package)
- Edit: `scenarios/` (CLI tool examples)
- Edit: `tests/` (test suites)

### No Sync Needed

Since there's only ONE copy of each file (in plugins/amp/), there's nothing to sync!

## Why Both?

### Workspace Root Files
**Purpose**: Development environment
- Used when working in this repo directly
- Can reference files freely without plugin constraints
- Easier to edit and maintain

### Plugin Files
**Purpose**: Distribution/installation
- Self-contained for users who install plugins
- All @ references work within plugin directory
- No dependencies on workspace structure

## Key Differences

### CLAUDE.md
- **Workspace version**: References `@ai_context/IMPLEMENTATION_PHILOSOPHY.md`
- **Plugin version**: References `@philosophies/IMPLEMENTATION_PHILOSOPHY.md`

These point to the same content but via different paths for each context.

## Avoiding Confusion

When working in this repo:
- You're using workspace root files by default
- @ references resolve from workspace root
- Plugin files are for distribution, not your active session

When users install plugins:
- They only get plugin directory files
- @ references resolve from plugin root
- No workspace root files exist in their environment

## Maintenance Notes

This creates intentional duplication for a good reason:
- ✅ Enables self-contained plugin distribution
- ✅ Allows development flexibility in workspace
- ✅ Both versions maintained in sync
- ⚠️ Requires manual sync before releases (until automated)

## Future Improvements

Consider:
1. Pre-commit hook to verify workspace ↔ plugin sync
2. Automated sync script
3. CI check to ensure distribution copies are current
4. Version tracking for plugin files
