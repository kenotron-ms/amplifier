# AmpBox: Minimal POC

**Zero external dependencies. Just Amplifier@next + Python stdlib.**

## Philosophy

Start with the simplest thing that could work. Add complexity only when simplicity fails.

**Current dependencies:**
- Amplifier@next (from /Users/ken/amplifier)
- Python stdlib (json, pathlib, asyncio)
- **Total: 0 new dependencies**

## What This Proves

That we can orchestrate workflows mixing:
- Deterministic steps (Python functions)
- Agentic steps (Amplifier@next agents)

Without adding workflow engines, databases, or services.

## Usage

```bash
# From workspace root
cd workspaces/ampbox

# Run example workflow
python -m ampbox.examples.research_assistant
```

## How It Works

**SimpleWorkflow:**
- Runs async Python functions in sequence
- Passes `WorkflowState` dict between steps
- Saves JSON checkpoint after each step
- ~100 lines of code, zero dependencies

**Example workflow:**
1. Load documents (deterministic)
2. Analyze with Amplifier agent (agentic)
3. Format report (deterministic)

**State persists to:** `.ampbox_state/<workflow_name>_latest.json`

## When to Add Complexity

**Add LangGraph when:**
- Conditional branching gets messy
- Need parallel execution
- Graph visualization would help

**Add SQLite when:**
- JSON files > 1MB
- Need to query state
- Multiple workflows share data

**Add services when:**
- Libraries can't handle the complexity
- Pain is proven, not hypothetical

**Until then: Keep it simple.**

## Files

- `ampbox/workflow.py` - Core orchestrator (~100 LOC)
- `ampbox/examples/research_assistant.py` - Example usage
- `.ampbox_state/` - State checkpoints (JSON files)
