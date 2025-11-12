# AmpBox: The 10% Glue

**Don't reinvent. Use LangGraph for workflows. Build only the Amplifier integration.**

## Philosophy

**Use libraries (LangGraph), don't reinvent workflows.**

**Current dependencies:**
- LangGraph (workflow orchestration - proven, maintained)
- Amplifier@next (from /Users/ken/amplifier)
- **Total: 1 dependency**

## What This Proves

That AmpBox's value is the **integration**, not reinventing wheels.

**LangGraph provides:**
- Workflow orchestration ✅
- State management ✅
- Checkpointing ✅
- Graph visualization ✅
- Conditional branching ✅
- Parallel execution ✅

**Amplifier@next provides:**
- Deep agents ✅
- Memory system ✅
- Checkpointing ✅

**AmpBox provides:**
- The bridge (AmplifierNode) ✅
- Makes them work together ✅

**We maintain:** ~50 lines of bridge code (not 100s of lines of workflow engine)

## Usage

```bash
# Install dependencies
cd workspaces/ampbox
uv pip install -e .

# Run example workflow
python -m ampbox.examples.research_assistant
```

## How It Works

**AmplifierNode:**
- Wrapper that makes Amplifier agents work as LangGraph nodes
- ~50 lines of code
- The ONLY custom code we write

**Example workflow (using LangGraph):**
```
StateGraph(ResearchState)
  ├─ load (deterministic function)
  ├─ analyze (AmplifierNode - Amplifier agent)
  └─ format (deterministic function)
```

**LangGraph handles everything else** (execution, state, persistence, visualization)

## Files

- `ampbox/amplifier_node.py` - The 10% glue (~50 LOC)
- `ampbox/examples/research_assistant.py` - Example using LangGraph
- State managed by LangGraph (not our code)
