#!/usr/bin/env python3
"""
Version bumping utility for Claude Code plugins.

Automatically bumps version numbers in plugin.json files based on
semantic versioning rules and git commit analysis.
"""

import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Literal

BumpType = Literal["major", "minor", "patch"]


def get_current_version(plugin_json_path: Path) -> tuple[int, int, int]:
    """Read current version from plugin.json."""
    with open(plugin_json_path) as f:
        data = json.load(f)

    version = data.get("version", "0.0.0")
    parts = version.split(".")

    return (int(parts[0]), int(parts[1]), int(parts[2]))


def bump_version(current: tuple[int, int, int], bump_type: BumpType) -> str:
    """Bump version according to semantic versioning rules."""
    major, minor, patch = current

    if bump_type == "major":
        return f"{major + 1}.0.0"
    if bump_type == "minor":
        return f"{major}.{minor + 1}.0"
    # patch
    return f"{major}.{minor}.{patch + 1}"


def update_plugin_json(plugin_json_path: Path, new_version: str) -> None:
    """Update plugin.json with new version."""
    with open(plugin_json_path) as f:
        data = json.load(f)

    data["version"] = new_version

    with open(plugin_json_path, "w") as f:
        json.dump(data, f, indent=2)
        f.write("\n")  # Add trailing newline


def detect_bump_type(base_branch: str = "origin/amplifier-claude") -> BumpType:
    """
    Analyze git commits to determine version bump type.

    Checks commit messages for:
    - MAJOR: BREAKING CHANGE, BREAKING:, or ! after type
    - MINOR: feat:, feature:
    - PATCH: fix:, docs:, refactor:, chore:, style:, test:, perf:
    """
    try:
        # Get commit messages since base branch
        result = subprocess.run(
            ["git", "log", f"{base_branch}..HEAD", "--format=%s%n%b"], capture_output=True, text=True, check=True
        )

        commit_messages = result.stdout

        # Check for breaking changes (MAJOR)
        if re.search(r"BREAKING CHANGE:|BREAKING:|!\s*:", commit_messages, re.IGNORECASE):
            return "major"

        # Check for new features (MINOR)
        if re.search(r"^(feat|feature)(\(.*?\))?:", commit_messages, re.MULTILINE):
            return "minor"

        # Default to PATCH for fixes, docs, refactors, etc.
        return "patch"

    except subprocess.CalledProcessError:
        # If git command fails, default to patch
        print("Warning: Could not analyze git commits, defaulting to patch bump", file=sys.stderr)
        return "patch"


def get_changed_plugins(base_branch: str = "origin/amplifier-claude") -> list[Path]:
    """
    Find plugins with file changes in current branch.

    Returns paths to plugin directories (e.g., plugins/amp/).
    """
    try:
        # Get changed files since base branch
        result = subprocess.run(
            ["git", "diff", f"{base_branch}...HEAD", "--name-only"], capture_output=True, text=True, check=True
        )

        changed_files = result.stdout.strip().split("\n")

        # Extract unique plugin directories
        plugin_dirs = set()
        for file_path in changed_files:
            match = re.match(r"^plugins/([^/]+)/", file_path)
            if match:
                plugin_dir = Path("plugins") / match.group(1)
                plugin_json = plugin_dir / ".claude-plugin" / "plugin.json"
                if plugin_json.exists():
                    plugin_dirs.add(plugin_dir)

        return sorted(plugin_dirs)

    except subprocess.CalledProcessError:
        print("Warning: Could not analyze changed files", file=sys.stderr)
        return []


def main() -> int:
    """Main entry point for version bumping."""
    import argparse

    parser = argparse.ArgumentParser(description="Bump plugin versions based on semantic versioning")
    parser.add_argument(
        "--base",
        default="origin/amplifier-claude",
        help="Base branch to compare against (default: origin/amplifier-claude)",
    )
    parser.add_argument(
        "--type", choices=["major", "minor", "patch"], help="Force specific bump type (auto-detect if not specified)"
    )
    parser.add_argument("--plugin", action="append", help="Specific plugin to bump (can be specified multiple times)")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done without making changes")

    args = parser.parse_args()

    # Determine bump type
    bump_type = args.type or detect_bump_type(args.base)
    print(f"Version bump type: {bump_type.upper()}")
    print()

    # Determine which plugins to bump
    if args.plugin:
        plugin_dirs = [Path(p) for p in args.plugin]
    else:
        plugin_dirs = get_changed_plugins(args.base)

    if not plugin_dirs:
        print("No plugins with changes found.")
        return 0

    # Bump version for each plugin
    bumped_plugins = []

    for plugin_dir in plugin_dirs:
        plugin_json_path = plugin_dir / ".claude-plugin" / "plugin.json"

        if not plugin_json_path.exists():
            print(f"⚠️  Skipping {plugin_dir.name} - no plugin.json found")
            continue

        # Get current and new versions
        current_version = get_current_version(plugin_json_path)
        new_version_str = bump_version(current_version, bump_type)

        print(f"📦 {plugin_dir.name}:")
        print(f"   {'.'.join(map(str, current_version))} → {new_version_str}")

        if not args.dry_run:
            update_plugin_json(plugin_json_path, new_version_str)
            bumped_plugins.append((plugin_dir.name, new_version_str))
            print(f"   ✅ Updated {plugin_json_path}")
        else:
            print("   (dry run - no changes made)")

        print()

    # Stage changed files if not dry run
    if not args.dry_run and bumped_plugins:
        print("Staging version bump changes...")
        for plugin_dir in plugin_dirs:
            plugin_json_path = plugin_dir / ".claude-plugin" / "plugin.json"
            if plugin_json_path.exists():
                subprocess.run(["git", "add", str(plugin_json_path)], check=True)

        print("\n✅ All plugin versions bumped and staged")
        print("\nCommit these changes with:")
        print('  git commit -m "chore: bump plugin versions for release"')
        print("\nBumped plugins:")
        for name, version in bumped_plugins:
            print(f"  - {name} → {version}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
