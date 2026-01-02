# Python Environment Guide for Project Commands & Hooks

This guide explains how to handle Python dependencies in project-specific commands and hooks that aren't included in the portable amp plugin.

## The Challenge

Project-specific commands and hooks often need to:
- Import project code (e.g., `from amplifier.memory import MemoryStore`)
- Use project dependencies
- Run in the project's Python environment

The amp plugin avoids this by only including commands that work universally without Python.

## Solutions for Your Project

### Option 1: Using `uv` (Recommended)

If your project uses `uv`, commands and hooks can use it automatically:

#### For Commands (`.claude/commands/review-changes.md`)

```markdown
# Review and test code changes

Run project checks using uv:

RUN:
uv run make check
uv run make test

# Or if you have scripts in pyproject.toml:
uv run pytest
uv run ruff check
```

#### For Hooks (`.claude/hooks/session_start.py`)

Add shebang to use uv automatically:

```python
#!/usr/bin/env -S uv run --quiet --script
# /// script
# dependencies = []
# ///

import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Now you can import project code
from amplifier.memory import MemoryStore
from amplifier.search import MemorySearcher

# ... rest of hook
```

**Settings configuration** (`.claude/settings.json`):

```json
{
  "hooks": {
    "SessionStart": [{
      "hooks": [{
        "type": "command",
        "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/session_start.py"
      }]
    }]
  }
}
```

The shebang makes it executable with uv automatically - no venv activation needed!

### Option 2: Using `uvx` for Standalone Tools

For tools that don't need project imports, use `uvx`:

#### Inline Script Dependencies

```python
#!/usr/bin/env -S uvx --quiet --with pydantic --with click --python 3.11
# transcript_manager.py - Standalone tool with inline deps

import click
from pydantic import BaseModel

@click.command()
def restore():
    # ... tool logic
    pass
```

#### Published Package

If you publish tools to PyPI:

```bash
# In command:
uvx --from amplifier-tools transcript-manager restore

# No installation or venv needed!
```

### Option 3: Traditional venv (If Not Using uv)

For projects not using `uv`, document the environment setup:

#### In Commands

```markdown
# Review changes

**Prerequisites**: Active Python environment

RUN:
# User must have activated venv manually:
# source .venv/bin/activate

make check
make test
```

#### In Hooks

Make hooks check for environment:

```python
#!/usr/bin/env python3
import sys
import os

# Check if in venv or proper environment
if not hasattr(sys, 'base_prefix') or sys.base_prefix == sys.prefix:
    print("Warning: Not in virtual environment", file=sys.stderr)
    # Either exit gracefully or continue with warning

# Continue with hook logic...
```

## Recommended Pattern: Hybrid

**For the amp plugin** (universal):
- ✅ Commands that work everywhere (commit, create-plan)
- ✅ Agents (no environment needed)
- ✅ Hook utilities (copy to projects)

**For your project** (`.claude/` directory):
- Project-specific commands using `uv run`
- Hooks with `#!/usr/bin/env -S uv run --quiet --script`
- Tools with inline dependencies via `uvx`

## Example: Project-Specific Hook with uv

**`.claude/hooks/session_start.py`**:

```python
#!/usr/bin/env -S uv run --quiet --script
# /// script
# dependencies = []
# ///
"""
Session start hook that loads Amplifier memory system.
Uses uv to run in project environment automatically.
"""

import asyncio
import json
import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Import from amp plugin utilities (copied to project)
sys.path.insert(0, str(Path(__file__).parent))
from hook_logger import HookLogger

logger = HookLogger("session_start")

# Import project code - this works because uv provides the environment
try:
    from amplifier.memory import MemoryStore
    from amplifier.search import MemorySearcher
except ImportError as e:
    logger.error(f"Failed to import amplifier modules: {e}")
    json.dump({}, sys.stdout)
    sys.exit(0)

async def main():
    """Load relevant memories for the session"""
    try:
        input_data = json.loads(sys.stdin.read())
        prompt = input_data.get("prompt", "")

        if not prompt:
            json.dump({}, sys.stdout)
            return

        # Use project code
        store = MemoryStore()
        searcher = MemorySearcher()
        results = searcher.search(prompt, store.get_all(), limit=5)

        # Format and return
        context = format_memories(results)
        json.dump({"additionalContext": context}, sys.stdout)

    except Exception as e:
        logger.exception("Error in session start hook", e)
        json.dump({}, sys.stdout)

if __name__ == "__main__":
    asyncio.run(main())
```

**Key Benefits**:
- No manual venv activation needed
- Hook runs in correct environment automatically
- Portable across machines (uv handles dependencies)
- Clear, self-documenting

## Migration Path

1. **Start**: Project-specific commands in `.claude/commands/` work locally
2. **Add uv**: Update commands to use `uv run`
3. **Update hooks**: Add `#!/usr/bin/env -S uv run --quiet --script`
4. **Test**: Verify hooks work without manual venv activation
5. **Document**: Update project README with setup instructions

## Testing Your Setup

```bash
# Test that hook works without activating venv
cd your-project
# DON'T activate venv
claude  # Start Claude Code

# Should work! The hook's shebang handles environment

# Test command
/review-changes  # Should use uv run automatically
```

## Summary

**Use the amp plugin for**: Universal agents, philosophies, simple commands

**Keep in your project for**: Commands/hooks that import project code

**Use `uv` to make project-specific code portable**: No manual venv activation needed!
