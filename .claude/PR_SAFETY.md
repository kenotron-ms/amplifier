# PR Safety Configuration

## ⚠️ IMPORTANT: PR Target Branch

This repository is configured with **PR safety rules** to prevent accidentally creating pull requests to the wrong branch.

### Configuration

The `.git-pr-config.json` file defines:

- **Allowed base branches**: `amplifier-claude`
- **Forbidden base branches**: `main`, `master`
- **Remote**: `origin` (kenotron-ms/amplifier)
- **Working branch**: `amplifier-claude`

### Why This Matters

This repository works exclusively on the `amplifier-claude` branch:

- **The `amplifier-claude` branch** contains Claude Code plugins and features
- **The `main` branch** is only for syncing with upstream (not for plugin work)
- **All PRs** should target `origin/amplifier-claude` (✅ CORRECT)
- **PRs to `main/master`** would disrupt the upstream sync (❌ WRONG)

### Automatic Protection

The `/git:submit-pr` command automatically checks `.git-pr-config.json` before creating PRs:

1. Detects the target base branch
2. Validates against allowed/forbidden lists
3. **Blocks PR creation** if targeting a forbidden branch
4. Shows clear error message explaining the issue

### Manual PR Creation

If creating PRs manually via `gh` CLI or GitHub UI:

```bash
# ✅ CORRECT: Target amplifier-claude branch
gh pr create --base amplifier-claude --head feature/my-changes

# ❌ WRONG: Would target main (blocked by automation)
gh pr create --base main --head feature/my-changes
```

### Working Safely

**Always ensure you're on the `amplifier-claude` branch** for plugin work:

```bash
# Check current branch
git branch --show-current

# Switch to amplifier-claude if needed
git checkout amplifier-claude

# Create feature branch from amplifier-claude
git checkout -b feature/my-plugin-work

# Make changes, commit, and use /git:submit-pr
# The PR will automatically target amplifier-claude ✅
```

### Error Message

If you see this error, it means the safety system is working:

```
❌ ERROR: Cannot create PR to branch 'main'

This repository has PR safety rules configured.

Forbidden base branches:
  - main
  - master

Allowed base branches:
  - amplifier-claude

Reason (from config):
  This repo contains Claude Code plugins on the amplifier-claude branch
  All PRs should target origin/amplifier-claude
  NEVER create PRs to main/master - those are for upstream sync only
```

**Solution**: Make sure you're working from the `amplifier-claude` branch, not `main`.

### Disabling (Not Recommended)

To disable PR safety (not recommended):

```bash
# Remove or rename the config file
mv .git-pr-config.json .git-pr-config.json.disabled
```

This removes the automatic protection - use with caution!

### Working with the Repository

All plugin development happens on `amplifier-claude`:

```bash
# Always work from amplifier-claude
git checkout amplifier-claude

# Pull latest changes
git pull origin amplifier-claude

# Create feature branch
git checkout -b feature/my-work

# Make changes, commit, and create PR
/git:submit-pr
# ✅ Will automatically target origin/amplifier-claude
```

The `main` branch is only for upstream sync and should not be used for plugin development.
