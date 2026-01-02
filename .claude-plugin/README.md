# Amplifier Claude Code Plugins

Three powerful plugins for Claude Code that provide specialized agents, workflows, and tools.

## 🚀 Quick Start

### Installation

**One-line install (recommended):**

**macOS / Linux:**
```bash
curl -fsSL https://raw.githubusercontent.com/kenotron-ms/amplifier/refs/heads/amplifier-claude/install.sh | bash
```

**Windows PowerShell:**
```powershell
irm https://raw.githubusercontent.com/kenotron-ms/amplifier/refs/heads/amplifier-claude/install.ps1 | iex
```

**Manual installation:**
```bash
# Add marketplace (amplifier-claude branch)
claude plugin marketplace add https://github.com/kenotron-ms/amplifier#amplifier-claude

# Install plugins (project scope)
claude plugin install amp@amplifier --scope project
claude plugin install git@amplifier --scope project
claude plugin install dev-kit@amplifier --scope project
```

## 📦 Available Plugins

### 1. amp - Core Amplifier
**Core development philosophy, specialized agents, and universal workflows**

**23 Specialized Agents:**
- **Core**: zen-architect, modular-builder, bug-hunter, test-coverage, security-guardian, performance-optimizer, database-architect, api-contract-designer, integration-specialist, etc.
- **Design**: component-designer, layout-architect, art-director, animation-choreographer, etc.
- **Knowledge**: concept-extractor, insight-synthesizer, knowledge-archaeologist, pattern-emergence, etc.

**Key Commands:**
- `/amp:commit` - Create conventional commits with philosophy alignment
- `/amp:ddd:*` - Domain-driven design workflow (8 phases)
- `/amp:prime` - Load complete context for session
- `/amp:review-changes` - Review code changes
- `/amp:ultrathink-task` - Complex task orchestration with sub-agents

**Philosophy:**
- Ruthless simplicity
- Modular design ("bricks & studs")
- Analysis-first, don't code blindly
- Trust in emergence over control

### 2. git - Git Workflow Helpers
**Intelligent version control with standards discovery and autonomous PR workflows**

**Commands:**
- `/git:commit` - Smart commit with repository standards discovery
- `/git:pull` - Intelligent branch syncing with conflict resolution
- `/git:submit-pr` - Complete autonomous PR workflow:
  - Auto-creates branch if on main/master
  - Ensures documentation compliance
  - Monitors CI/CD checks in real-time
  - Fixes failures automatically (up to 3 attempts)
  - Auto-merges when approved and checks pass
  - Cleans up branches after merge

**Skills:**
- `pr-submission` - Auto-triggers on PR-related requests

### 3. dev-kit - SDLC Toolkit
**Structured test-driven development lifecycle with 9-phase workflow**

**Commands:**
- `/dev-kit:new-feature` - Complete TDD workflow orchestrator
- `/dev-kit:new-feature:0-discover` - Explore and understand codebase
- `/dev-kit:new-feature:1-requirements` - Define requirements and acceptance criteria
- `/dev-kit:new-feature:2-design` - Design architecture and approach
- `/dev-kit:new-feature:3-tests` - Write tests FIRST (TDD RED phase)
- `/dev-kit:new-feature:4-implement` - Implement to make tests pass (TDD GREEN)
- `/dev-kit:new-feature:5-refactor` - Refactor and improve (TDD REFACTOR)
- `/dev-kit:new-feature:6-verify` - Comprehensive testing and verification
- `/dev-kit:new-feature:7-document` - Update all relevant documentation
- `/dev-kit:new-feature:8-cleanup` - Archive working documents
- `/dev-kit:new-feature:status` - Check feature development progress

**Workflow Approach:**
- Test-Driven Development (TDD)
- Complete coverage: requirements → tests → implementation → docs
- Progress tracking across phases
- Integrates with amp philosophy and agents

## 💡 Usage Examples

### Using amp Agents

Agents are automatically available through the Task tool:

```markdown
Task zen-architect: "Analyze this architecture and suggest improvements following @philosophies/IMPLEMENTATION_PHILOSOPHY.md"

Task bug-hunter: "Find and fix the authentication bug in the login flow"

Task modular-builder: "Implement the user profile module from specs"
```

### Git Workflow

```bash
# Make changes to code...

# Smart commit with standards discovery
/git:commit

# Complete PR workflow (fully autonomous)
/git:submit-pr
# - Creates branch if needed
# - Commits changes
# - Ensures docs compliance
# - Creates PR
# - Monitors checks
# - Fixes failures
# - Auto-merges when ready
```

### Feature Development

```bash
# Start new feature with complete workflow
/dev-kit:new-feature

# Or run individual phases
/dev-kit:new-feature:0-discover
/dev-kit:new-feature:1-requirements
# ...

# Check progress
/dev-kit:new-feature:status
```

## 🎯 Key Features

### Self-Contained
Each plugin includes ALL necessary files:
- Philosophy documents
- Reference materials
- Agent definitions
- Command workflows

### @ Reference Resolution
All `@` file references resolve within each plugin:
- `@philosophies/IMPLEMENTATION_PHILOSOPHY.md`
- `@AGENTS.md`
- `@CLAUDE.md`
- `@DISCOVERIES.md`

### Independent Installation
Install only what you need:
```bash
# Just core amp
claude plugin install amp@amplifier --scope project

# Just git workflows
claude plugin install git@amplifier --scope project

# Just dev-kit
claude plugin install dev-kit@amplifier --scope project
```

## 📚 Documentation

- **Plugin architecture**: See [../plugins/README.md](../plugins/README.md)
- **Philosophy**: See plugins/amp/philosophies/
- **Git workflows**: See plugins/git/README.md
- **Dev-kit workflows**: See plugins/dev-kit/commands/

## 🔧 Configuration

All plugins work with project-scope installation by default. They read philosophy and standards from their own directories, so they work consistently across any project.

## 🤝 Contributing

See main repository documentation for contribution guidelines.

## 📄 License

MIT License - see LICENSE file in repository root.
