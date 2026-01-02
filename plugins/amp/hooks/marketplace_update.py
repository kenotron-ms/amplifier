#!/usr/bin/env python3
"""
Claude Code Marketplace Update Hook (Cross-platform)

Runs at session start to check for and install plugin updates from
the amplifier marketplace. Ensures users always have the latest versions.
"""

import contextlib
import json
import subprocess
import sys
from pathlib import Path


def main() -> int:
    """Main hook entry point."""
    try:
        # Read JSON input from stdin
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        # Silently fail to not disrupt session start
        return 0

    # Determine project directory
    import os

    project_dir = Path(os.environ.get("CLAUDE_PROJECT_DIR", data.get("cwd", ".")))

    # Silently update marketplace and plugins in the background
    try:
        # Step 1: Update marketplace registry
        subprocess.run(
            ["claude", "plugin", "marketplace", "update", "--marketplace", "amplifier"],
            cwd=project_dir,
            capture_output=True,
            text=True,
            timeout=15,  # Quick timeout to not block session start
        )

        # Step 2: Update installed plugins
        plugins_to_update = ["amp@amplifier", "git@amplifier", "dev-kit@amplifier"]

        for plugin in plugins_to_update:
            with contextlib.suppress(subprocess.CalledProcessError, subprocess.TimeoutExpired):
                subprocess.run(
                    ["claude", "plugin", "update", plugin],
                    cwd=project_dir,
                    capture_output=True,
                    text=True,
                    timeout=10,  # Quick timeout per plugin
                )

    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
        # Silently fail - don't disrupt session start
        # User can manually update if needed
        pass

    # Always return success to not block session start
    return 0


if __name__ == "__main__":
    sys.exit(main())
