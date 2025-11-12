# AmpBox: Integrated Runtime for AI Agents
**Product Vision & Alignment Document**

---

## **The Core Problem**

**Infrastructure complexity robs time from building intelligence.**

You have a working Amplifier agent. Now you need:
- Database for persistence
- Auth for users
- Storage for files
- Workflow orchestration
- External service connections
- UI for interaction
- Desktop packaging for distribution

**Each piece has excellent solutions. But integrating them takes weeks.**

**The real problem:** Not the technology (it exists), but the **integration tax** - the custom glue code connecting 15+ tools.

---

## **The Landscape (What Already Exists)**

### **Agent Frameworks**
- Amplifier@next (deep agents, memory, checkpointing)
- LangChain/LangGraph (agent orchestration)
- CrewAI (multi-agent systems)

### **Workflow Tools**
- n8n, Temporal (deterministic workflows)
- Flowise, LangFlow (visual builders for simple agents)

### **UI Toolkits**
- shadcn/ui, MUI (component libraries)
- Refine.dev (admin frameworks with backend adapters)
- Vercel AI SDK (React hooks for AI)

### **Infrastructure**
- PocketBase (embedded SQLite + auth + storage)
- Supabase (cloud BaaS)
- Docker Compose (service orchestration)

### **Desktop Packaging**
- Tauri (native desktop apps)
- Ollama (local LLM serving)

**Each solves ONE piece. No one solves integration.**

---

## **The AmpBox Solution**

### **Positioning: "Rails for AI Agents"**

**Rails didn't invent databases, web servers, or MVC. It integrated them with convention over configuration.**

**AmpBox doesn't invent agent frameworks, workflows, or UI kits. It integrates them with zero-config defaults.**

---

## **What We Ruthlessly Use (90% Existing)**

### **Agent Runtime:**
- **Amplifier@next** - Deep agents, memory, checkpointing, knowledge synthesis
- Why reinvent? It's world-class.

### **Database + Auth + Storage:**
- **PocketBase** - Embedded SQLite with auth, file storage, realtime, admin UI
- Single Go binary, embeds in desktop apps perfectly
- Why reinvent? Exactly what we need for local-first.

### **Workflow Orchestration:**
- **Temporal** (programmatic) OR **n8n** (visual)
- Both mature, battle-tested
- Why reinvent? Workflow engines are solved problems.

### **Desktop Packaging:**
- **Tauri 2.0** - Rust core, web frontend, native APIs
- Smaller than Electron, better security
- Why reinvent? Perfect for AI desktop apps.

### **UI Components:**
- **Developer's choice:** shadcn/ui, MUI, Reflex, Streamlit
- **Backend adapters:** Refine.dev pattern (support multiple backends)
- Why reinvent? Hundreds of excellent component libraries exist.

### **Local LLMs:**
- **Ollama** - De facto standard for local model serving
- Why reinvent? 75k stars, proven, maintained.

### **Type Safety:**
- **tRPC** - Type-safe APIs for TypeScript
- **Zod** - Schema validation across stack
- Why reinvent? Community-standard solutions.

---

## **What We Build (10% Unique Layer)**

### **The Integration Glue**

**This is the ONLY code AmpBox writes:**

**1. Agent → Workflow Bridge**
- Amplifier agents run as Temporal/n8n workflow tasks
- Bidirectional: Agents call workflows as tools, workflows call agents as steps
- Handle checkpointing, state management, error recovery

**2. Backend → Frontend Bindings**
- Auto-generate tRPC routers from agent definitions
- Type-safe bindings: Amplifier schemas → Zod → TypeScript
- Component adapters: Works with shadcn/ui, MUI, Reflex, etc.
- AI-assisted wiring: Connect forms to agents, tables to workflows

**3. Embedded Runtime Manager**
- Start/stop PocketBase embedded instance
- Manage Ollama for local LLMs
- Health monitoring and auto-restart
- Handles local → cloud fallback

**4. Desktop Packager**
- Tauri project generator (pre-configured for AI apps)
- Bundle: Agent code + PocketBase + Ollama (optional) + UI
- Single binary output (.exe, .dmg, .AppImage)
- Auto-update mechanism

**5. The CLI/Config Layer**
```bash
ampbox init          # Scaffolds project with all integrations
ampbox dev           # Runs everything locally (PocketBase, Ollama, agents, UI)
ampbox build         # Packages as desktop app
ampbox deploy cloud  # Optional cloud deployment
```

**6. Studio Canvas (Visual Wiring)**
- Shows: Backend (agents, workflows) + Frontend (components)
- Draw connections visually
- Generates integration code
- Not a design tool - a **wiring tool**

---

## **The Unique Value Proposition**

**For agent developers who need to ship working applications:**

**AmpBox is an integrated runtime that eliminates integration work.**

**It provides:**
1. **Zero-config integration** - Amplifier + PocketBase + Temporal + Tauri work together out of box
2. **Bidirectional workflows** - Agents in workflows, workflows in agents (nested composition)
3. **Desktop-first packaging** - One command → distributable app (no Docker for users)
4. **Type-safe bindings** - Backend types propagate to frontend automatically
5. **Connector infrastructure** - MCP registry with lifecycle management

**Unlike:**
- **Amplifier alone:** No infrastructure, workflows, UI, or packaging
- **n8n/Temporal alone:** No deep agent support
- **Supabase/PocketBase alone:** No agent runtime or workflows
- **Tauri alone:** No AI-specific features or backend integration

**AmpBox is the glue layer that makes them work together.**

---

## **What Becomes Unnecessary**

When AmpBox exists, developers **no longer write:**

❌ Database migration scripts (generated from agent schemas)
❌ API layer boilerplate (tRPC auto-generated)
❌ Auth integration code (PocketBase handles it)
❌ Workflow task definitions (agent → task adapter)
❌ UI state management (workflow engine provides state)
❌ Desktop packaging scripts (ampbox build)
❌ Update mechanisms (built-in)

**The simplification cascade:**
Solve "integrated agent runtime" → Eliminates 30-40% of typical project code (the custom glue).

---

## **What Becomes Possible**

### **New Possibility 1: Weekend AI Apps**
Go from agent idea → distributable desktop app in 48 hours
- Saturday: Build agent with Amplifier, define workflow
- Sunday: Generate UI bindings, package with ampbox build
- Ship to users Monday

### **New Possibility 2: Personal AI Stack**
Sophisticated agents without cloud dependencies:
- Run entirely on your machine
- No SaaS subscriptions, no API costs
- Your data never leaves your computer
- Optionally sync to cloud when YOU choose

### **New Possibility 3: Team Tools Without IT**
Share AI tools as easily as sharing a document:
- Send .exe/.dmg to colleague
- They double-click, it works
- No infrastructure provisioning, no IT approval
- Self-contained, sandboxed, safe

### **New Possibility 4: Agent Marketplace**
Distribute agents as standalone apps:
- "npm install" for AI agents
- One-click install, includes runtime
- Like Electron apps (Slack, VS Code) but for AI

### **New Possibility 5: Graduated Complexity**
Start simple, go deep when needed:
- Day 1: Use templates (zero code)
- Week 1: Customize agents (agent code)
- Month 1: Custom workflows (orchestration)
- Month 3: Fork runtime (full control)

---

## **The Non-Technical Value**

**Beyond faster development:**

**1. Risk Reduction**
- Use battle-tested integrations (not custom glue)
- Security updates handled (update AmpBox, get all fixes)
- Compliance easier (fewer moving parts)

**2. Team Scaling**
- New developers understand "it's AmpBox" (not your custom stack)
- Onboarding is learning AmpBox (not 15 tools)
- Knowledge transfers across AmpBox projects

**3. Focus Preservation**
- Spend time on agent intelligence (your unique value)
- Not on integration debugging (undifferentiated work)
- Cognitive energy on problems that matter

**4. Economic Model Shift**
- Local-first = no per-seat SaaS costs
- Use cloud when YOU choose (not forced)
- Users own their tools (not rent them)

---

## **Honest Assessment**

### **Is this "just integration"?**
**Yes.** But that's the point.

Rails is "just integration" of database + web server + MVC.
Next.js is "just integration" of React + routing + server actions.
**Both created massive value by solving integration once.**

### **Can developers do this themselves?**
**Yes.** But they choose not to.

They could integrate Amplifier + PocketBase + Temporal + Tauri themselves. But:
- Takes 2-4 weeks per project
- Custom solutions (not reusable)
- Maintenance burden (15+ dependencies to update)

**AmpBox's value:** Do it once, perfectly, so no one else has to.

### **Will this actually save time?**
**Hypothesis to validate.**

Need to build proof of concept and measure:
- Time from agent code → working app
- Developer satisfaction (does it actually help?)
- Adoption (do people use it over DIY?)

---

## **Success Metrics**

### **Technical:**
- Integration works: Amplifier agents run in Temporal/n8n workflows
- Packaging works: One command → distributable desktop app
- Type safety works: Backend changes propagate to frontend automatically
- Offline works: App runs without internet, syncs when online

### **Developer Experience:**
- Time to first app: < 1 day (vs. 2-4 weeks)
- Custom integration code: < 10% of project (vs. 30-40%)
- Setup complexity: One config file (vs. dozens)

### **Product:**
- 10+ apps built with AmpBox (validate real usage)
- Developers choose AmpBox over DIY (preference validation)
- Community contributions (agents, workflows, templates)

---

## **The Thesis**

**"Infrastructure integration is undifferentiated work. Solve it once, so developers can focus on intelligence."**

**AmpBox = The 10% glue that makes 90% existing tools work together.**

**Three pillars:**
1. **Workflow orchestration** (deterministic + agentic, bidirectionally nested)
2. **Connector infrastructure** (MCP registry + lifecycle)
3. **Zero-config packaging** (desktop or cloud, no Docker for users)

**Built on:** Amplifier@next + PocketBase + Temporal/n8n + Tauri + shadcn/Reflex

**If thesis is correct:** AmpBox becomes how you deploy Amplifier agents (like Vercel is how you deploy Next.js).

**If thesis is wrong:** We learn what developers actually need and build that instead.

---

## **Alignment Check**

Before building features, ask:

1. ✅ **Does this reduce integration work?** (save developer time)
2. ✅ **Can this use existing tools?** (leverage ecosystem)
3. ✅ **Is this glue, not reinvention?** (10% unique, 90% existing)
4. ✅ **Does this enable deep agents in workflows?** (bidirectional nesting)
5. ✅ **Does this make deployment easier?** (no Docker for users)

**If all yes → Aligned with vision, build it**
**If any no → Not aligned, reconsider**

---

_This document defines AmpBox as integration layer, not technology platform. Update as we learn._
