# Amp Plugin

Amplifier development philosophy, universal agents, and workflows for AI-assisted development.

## What's Included

### Core Agents (`/agents/core/`)
Universal development agents that work across any project:
- `zen-architect` - Planning and architecture design with ruthless simplicity
- `modular-builder` - Implementation following "bricks and studs" philosophy
- `bug-hunter` - Systematic debugging and issue resolution
- `test-coverage` - Test strategy and coverage analysis
- `security-guardian` - Security reviews and vulnerability assessment
- `performance-optimizer` - Performance analysis and optimization
- `integration-specialist` - External service and API integration
- `database-architect` - Database design and optimization
- `api-contract-designer` - API design and contracts
- `post-task-cleanup` - Codebase hygiene after task completion
- `subagent-architect` - Creating new specialized agents
- `amplifier-cli-architect` - Expert guidance for Amplifier CLI tools
- `contract-spec-author` - Create contract and implementation specifications
- `module-intent-architect` - Translate natural language to module specifications

### Design Agents (`/agents/design/`)
Specialized agents for design systems and UI/UX:
- `animation-choreographer` - Motion design and animation
- `art-director` - Visual direction and aesthetics
- `component-designer` - UI component design
- `design-system-architect` - Design system architecture
- `layout-architect` - Layout and spacing systems
- `responsive-strategist` - Responsive design strategies
- `voice-strategist` - Brand voice and tone

### Knowledge Agents (`/agents/knowledge/`)
Agents for knowledge synthesis and management:
- `concept-extractor` - Extract concepts from documents
- `insight-synthesizer` - Synthesize insights from multiple sources
- `pattern-emergence` - Detect emergent patterns
- `ambiguity-guardian` - Preserve productive ambiguity
- `knowledge-archaeologist` - Trace evolution of ideas
- `visualization-architect` - Create knowledge visualizations
- `graph-builder` - Build knowledge graphs
- `content-researcher` - Research and analyze content
- `analysis-engine` - Multi-mode analysis

### Commands (`/commands/`)
Universal workflow commands (portable via `uv`):

**Core Workflow Commands:**
- `/amp:commit` - Create well-formatted git commits with conventional commit messages
- `/amp:create-plan` - Create implementation plans from current context
- `/amp:execute-plan` - Execute implementation plans (uses `uv sync` for dependencies)
- `/amp:review-changes` - Review and test code changes (uses `uv run` for checks/tests)
- `/amp:review-code-at-path` - Review code at specific paths (uses `uv run` for checks/tests)
- `/amp:prime` - Setup and verify project environment (uses `uv sync` and `uv run`)

**Advanced Workflows:**
- `/amp:ultrathink-task` - Task orchestration with specialized sub-agents (zero-shot planning)
- `/amp:designer` - Transform design ideas through collaborative intelligence with design agents
- `/amp:modular-build` - Generate modules from natural language (Contract → Spec → Plan → Code)
- `/amp:test-webapp-ui` - Test web applications using browser automation (Playwright MCP)
- `/amp:transcripts` - Manage conversation transcripts (restore, search, export)

**Document-Driven Development (DDD):**
- `/amp:ddd:0-help` - Complete DDD workflow guide and help
- `/amp:ddd:1-plan` - Planning and design phase
- `/amp:ddd:2-docs` - Update all non-code files (docs, configs, READMEs)
- `/amp:ddd:3-code-plan` - Plan code implementation changes
- `/amp:ddd:4-code` - Implement and verify code
- `/amp:ddd:5-finish` - Cleanup and finalize
- `/amp:ddd:prime` - Load complete DDD context
- `/amp:ddd:status` - Check current progress and next steps

### Philosophies (`/philosophies/`)
Core development philosophies and principles:
- `IMPLEMENTATION_PHILOSOPHY.md` - Ruthless simplicity, architectural integrity
- `MODULAR_DESIGN_PHILOSOPHY.md` - "Bricks and studs" approach
- `DESIGN-PHILOSOPHY.md` - Design system philosophy
- `DESIGN-PRINCIPLES.md` - Actionable design principles
- `DESIGN-FRAMEWORK.md` - Design sensibility framework
- `DESIGN-VISION.md` - Design vision and values

### Tools and Context (`/tools/` and `/ai_context/`)
Portable CLI tools and supporting documentation:
- `tools/transcript_manager.py` - Manage conversation transcripts (restore, search, export)
- `ai_context/module_generator/CONTRACT_SPEC_AUTHORING_GUIDE.md` - Module specification authoring guide (for `/amp:modular-build`)

### Hook Utilities (`/hooks/utils/`)
Shared utilities for creating project-specific hooks:
- `hook_logger.py` - Logging utility for hooks

## Installation

### Add the Marketplace

```bash
claude plugin marketplace add kenotron-ms/amplifier
```

### Install the Plugin

```bash
# Install for all your projects (recommended)
claude plugin install amp@amplifier --scope user

# Or install for current project only
claude plugin install amp@amplifier --scope project
```

## Usage

### Using Agents

Agents are automatically available to Claude Code. The system will delegate to them as appropriate:

```bash
# In your conversation with Claude Code, agents are invoked automatically
# when their expertise is needed. For example:

"Review this code for security issues"
# → security-guardian agent may be invoked

"Help me plan this feature"
# → zen-architect agent may be invoked
```

### Using Commands

Commands are invoked with the `/amp:` prefix:

```bash
# Core Workflow
/amp:commit                # Create git commit with conventional message
/amp:create-plan           # Generate implementation plan
/amp:execute-plan          # Execute an implementation plan
/amp:review-changes        # Review and test code changes
/amp:review-code-at-path   # Review specific code paths
/amp:prime                 # Setup and verify project environment

# Advanced Workflows
/amp:ultrathink-task       # Orchestrate task with specialized agents
/amp:designer              # Transform design ideas with AI
/amp:modular-build         # Generate modules from natural language
/amp:test-webapp-ui        # Test web apps with browser automation
/amp:transcripts           # Manage conversation transcripts

# Document-Driven Development
/amp:ddd:0-help            # Get complete DDD guide
/amp:ddd:1-plan            # Start DDD planning phase
/amp:ddd:status            # Check DDD progress
# ... (see full list in Commands section above)
```

**Python Environment**: All commands use `uv` for Python dependencies, so no manual venv activation is needed! Just ensure your project has:
- `pyproject.toml` with dependencies
- `uv` installed (`curl -LsSf https://astral.sh/uv/install.sh | sh`)

Commands will run `uv sync` and `uv run` automatically.

**Included Tools**: Commands can reference tools bundled with the plugin using `${CLAUDE_PLUGIN_ROOT}`:
```bash
# Example: transcript_manager.py is at
${CLAUDE_PLUGIN_ROOT}/tools/transcript_manager.py

# ✅ CORRECT - Invoke from project directory using absolute path:
uv run python ${CLAUDE_PLUGIN_ROOT}/tools/transcript_manager.py restore

# 🔴 NEVER use cd to change into plugin cache:
# WRONG: cd ${CLAUDE_PLUGIN_ROOT} && uv run python tools/transcript_manager.py
# This breaks relative paths and prevents tools from finding project files
```

### Referencing Philosophies

Philosophy documents are available in the plugin cache:

```bash
# On macOS/Linux:
~/.claude/plugins/cache/amp/philosophies/

# Reference in your project's CLAUDE.md:
# "This project follows Amplifier philosophy. See:"
# "~/.claude/plugins/cache/amp/philosophies/IMPLEMENTATION_PHILOSOPHY.md"
```

### Creating Project-Specific Hooks

Copy utilities from the plugin and create portable hooks with `uv`:

```bash
# Copy logger utility
cp ~/.claude/plugins/cache/amp/hooks/utils/hook_logger.py .claude/hooks/

# Create your hook with uv shebang (no venv activation needed!)
```

**Example hook** (`.claude/hooks/session_start.py`):
```python
#!/usr/bin/env -S uv run --quiet --script
# /// script
# dependencies = []
# ///

# Import project code - uv handles the environment!
from amplifier.memory import MemoryStore
# ... hook logic
```

See [PYTHON_ENV_GUIDE.md](./PYTHON_ENV_GUIDE.md) for detailed patterns.

## Philosophy

This plugin embodies the Amplifier development philosophy:

1. **Ruthless Simplicity** - Keep everything as simple as possible, but no simpler
2. **Modular Design** - "Bricks and studs" approach for AI-regeneratable code
3. **Architectural Integrity** - Preserve key patterns with minimal implementation
4. **Trust in Emergence** - Complex systems from simple, well-defined components
5. **Design for Humans** - Real people with diverse abilities and contexts

## License

MIT

## Contributing

See the main [Amplifier repository](https://github.com/kenotron-ms/amplifier) for contribution guidelines.
