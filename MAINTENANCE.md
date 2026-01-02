# Maintenance Guide

This document provides maintenance procedures and automation instructions for the Amplifier plugin repository.

## Automated Version Management

The `/git:submit-pr` command automatically handles version bumping for plugin updates using semantic versioning.

### Version Bump Rules

**CRITICAL**: The submit-pr workflow MUST bump plugin versions in `.claude-plugin/plugin.json` files before creating PRs.

#### Semantic Versioning (semver)

Versions follow the format: `MAJOR.MINOR.PATCH`

- **MAJOR** (x.0.0): Breaking changes, incompatible API changes
- **MINOR** (0.x.0): New features, backwards-compatible additions
- **PATCH** (0.0.x): Bug fixes, documentation updates, refactors

#### Automatic Version Detection

The submit-pr workflow analyzes commit messages to determine the appropriate version bump:

**MAJOR version bumps** (breaking changes):
- Commit messages containing: `BREAKING CHANGE:`, `BREAKING:`, or `!` suffix after type
- Examples:
  - `feat!: remove deprecated API`
  - `refactor!: restructure plugin directory`
  - `fix: correct behavior\n\nBREAKING CHANGE: changes default behavior`

**MINOR version bumps** (new features):
- Commit type: `feat:`, `feature:`
- Examples:
  - `feat: add new zen-architect agent`
  - `feat: add marketplace update hook`

**PATCH version bumps** (fixes, docs, refactors):
- Commit types: `fix:`, `docs:`, `refactor:`, `chore:`, `style:`, `test:`, `perf:`
- Examples:
  - `fix: correct hook path resolution`
  - `docs: update installation guide`
  - `refactor: simplify code structure`
  - `chore: update dependencies`

### Affected Plugins

Version bumps apply to all plugins with changes in their directories:

```bash
# Check which plugins have changes
git diff origin/amplifier-claude...HEAD --name-only | grep -o '^plugins/[^/]*' | sort -u
```

Plugins to check:
- `plugins/amp/.claude-plugin/plugin.json`
- `plugins/git/.claude-plugin/plugin.json`
- `plugins/dev-kit/.claude-plugin/plugin.json`

### Implementation in submit-pr Workflow

The `/git:submit-pr` command should:

1. **After commit creation, before pushing:**
   - Analyze all commits in the PR for version bump indicators
   - Determine highest version bump needed (MAJOR > MINOR > PATCH)
   - Identify which plugins have file changes
   - Update version in each affected plugin's `.claude-plugin/plugin.json`
   - Create version bump commit: `chore: bump plugin versions`

2. **Example workflow:**
   ```bash
   # Determine version bump type
   if git log origin/amplifier-claude..HEAD | grep -qE 'BREAKING CHANGE:|!:'; then
     BUMP_TYPE="major"
   elif git log origin/amplifier-claude..HEAD | grep -qE '^feat(\(.*\))?:'; then
     BUMP_TYPE="minor"
   else
     BUMP_TYPE="patch"
   fi

   # Bump version for each affected plugin
   for plugin in $(git diff origin/amplifier-claude...HEAD --name-only | grep -o '^plugins/[^/]*' | sort -u); do
     if [[ -f "$plugin/.claude-plugin/plugin.json" ]]; then
       # Use jq or python to bump version
       # Update plugin.json with new version
       # Stage the file
     fi
   done

   # Commit version bump
   git commit -m "chore: bump plugin versions for release"
   ```

3. **Version bump commit must include:**
   - Clear indication of bump type in commit body
   - List of affected plugins
   - Previous and new versions

### Marketplace Update Hook

After version bumps are pushed, the post-push hook automatically updates the local marketplace:

```bash
# Triggered by: PostPush hook
# Location: plugins/amp/hooks/marketplace_update.sh
# Command: claude plugin marketplace update --marketplace amplifier
```

This ensures users get the latest plugin versions without manual intervention.

## Manual Version Bumping

If you need to manually bump versions:

```bash
# Navigate to plugin directory
cd plugins/amp/.claude-plugin/

# Edit plugin.json manually
# Update "version" field following semver rules

# Or use jq (if available)
jq '.version = "1.1.0"' plugin.json > tmp.json && mv tmp.json plugin.json

# Commit the change
git add plugin.json
git commit -m "chore(amp): bump version to 1.1.0"
```

## Marketplace Management

### Local Marketplace Setup

The repository uses a local "amplifier" marketplace configured in `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "amplifier": {
      "source": {
        "source": "directory",
        "path": "."
      }
    }
  }
}
```

### Updating Marketplace

To manually update the marketplace:

```bash
claude plugin marketplace update --marketplace amplifier
```

This command:
1. Scans the repository for plugin updates
2. Registers new versions in Claude Code's plugin registry
3. Makes updates available via `claude plugin update` command

### Plugin Installation

Users can install/update plugins from the amplifier marketplace:

```bash
# Install a plugin
claude plugin install amp@amplifier

# Update all plugins from marketplace
claude plugin update --marketplace amplifier

# Update specific plugin
claude plugin update amp@amplifier
```

## Release Checklist

Before merging PRs that include plugin changes:

- [ ] Verify commits follow conventional commit format
- [ ] Ensure version bump commit was created by submit-pr
- [ ] Confirm all affected plugins have updated versions
- [ ] Check that changelog entries exist (if applicable)
- [ ] Verify marketplace update hook will run after merge

## Troubleshooting

### Version Not Updating

If plugin versions aren't updating:

1. Check commit messages follow conventional commits format
2. Verify submit-pr workflow included version bump step
3. Manually bump version and commit
4. Run marketplace update: `claude plugin marketplace update --marketplace amplifier`

### Marketplace Not Refreshing

If changes aren't reflected in Claude Code:

1. Manually update marketplace: `claude plugin marketplace update --marketplace amplifier`
2. Check plugin registry: `claude plugin list --marketplace amplifier`
3. Verify plugin installation: `claude plugin show amp@amplifier`

### Breaking Changes

For breaking changes:

1. Bump MAJOR version (e.g., 1.0.0 → 2.0.0)
2. Document breaking changes in commit message and PR description
3. Update CLAUDE.md or AGENTS.md if behavior changes
4. Consider migration guide for users

## Best Practices

1. **Commit message discipline**: Always use conventional commits format
2. **Atomic commits**: One logical change per commit
3. **Version bumps**: Let submit-pr handle version bumping automatically
4. **Testing**: Test plugin changes before merging
5. **Documentation**: Update docs when adding features or breaking changes
6. **Marketplace sync**: Hook handles marketplace updates automatically

## Related Documentation

- [CLAUDE.md](./CLAUDE.md) - Repository-specific instructions
- [plugins/amp/README.md](./plugins/amp/README.md) - Amp plugin documentation
- [CONTRIBUTING.md](./CONTRIBUTING.md) - Contribution guidelines (if exists)
