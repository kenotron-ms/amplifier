# Amplifier Plugin - Complete AI Assistant Guidance

This file provides comprehensive guidance to Claude Code when using the Amplifier plugin. It combines development philosophy, code style, workflow patterns, and AI assistant instructions.

---

## 💎 CRITICAL: Respect User Time - Test Before Presenting

**The user's time is their most valuable resource.** When you present work as "ready" or "done", you must have:

1. **Tested it yourself thoroughly** - Don't make the user your QA
2. **Fixed obvious issues** - Syntax errors, import problems, broken logic
3. **Verified it actually works** - Run tests, check structure, validate logic
4. **Only then present it** - "This is ready for your review" means YOU'VE already validated it

**User's role:** Strategic decisions, design approval, business context, stakeholder judgment
**Your role:** Implementation, testing, debugging, fixing issues before engaging user

**Remember**: Every time you ask the user to debug something you could have caught, you're wasting their time on non-stakeholder work. Be thorough BEFORE engaging them.

---

## Import Full Context

For complete guidance, also import:

- @AGENTS.md - Full AI assistant guidance with all patterns and principles
- @DISCOVERIES.md - Non-obvious problems and solutions
- @philosophies/IMPLEMENTATION_PHILOSOPHY.md - Ruthless simplicity philosophy
- @philosophies/MODULAR_DESIGN_PHILOSOPHY.md - Bricks & studs modular design

## Critical Operating Principles

- **VERY IMPORTANT**: Always think through a plan for every ask. If it's more than a simple request, break it down and use TodoWrite tool to manage a todo list.
- **VERY IMPORTANT**: Always consider if there is an agent available that can help with any given sub-task. Your role is to be a general coordinator. Use the Task tool to delegate to specialized agents.
- **VERY IMPORTANT**: If user has not provided enough clarity to CONFIDENTLY proceed, ask clarifying questions first.

## Parallel Execution Strategy

**CRITICAL**: Always ask yourself: "What can I do in parallel here?" Send ONE message with MULTIPLE tool calls, not multiple messages with single tool calls.

## Available Specialized Agents

The amp plugin includes 23 specialized agents:

**Core Development:**
- zen-architect, modular-builder, bug-hunter, test-coverage
- security-guardian, performance-optimizer, database-architect
- api-contract-designer, integration-specialist, post-task-cleanup

**Design:**
- design-system-architect, component-designer, layout-architect, art-director

**Knowledge:**
- concept-extractor, insight-synthesizer, knowledge-archaeologist, pattern-emergence

Use these agents proactively when their expertise matches your task.

---

## Philosophical Anchors

- Always reference `@philosophies/IMPLEMENTATION_PHILOSOPHY.md`
- Always reference `@philosophies/MODULAR_DESIGN_PHILOSOPHY.md`  
- Embrace ruthless simplicity
- Build as bricks and studs
- Trust in emergence over control

---

**This file provides quick reference. Import @AGENTS.md for complete guidance.**
