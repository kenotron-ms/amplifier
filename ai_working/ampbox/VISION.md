# AmpBox: Integrated Runtime for AI Agents
**Product Vision & Alignment Document**

---

## **The Core Problem**

**Infrastructure complexity robs time from building intelligence.**

You have a working Amplifier agent. Getting it to production requires integrating many pieces, and **every integration is code you maintain forever.**

**The trap:** Adding dependencies "just in case" creates maintenance burden before proving value.

---

## **The Library-First Philosophy**

### **Start with Absolute Minimum:**

**Phase 1: Prove the concept**
- Amplifier@next agents (already exists)
- JSON files for state (Python stdlib)
- Python functions for workflows (no library needed yet)
- CLI for interface (print statements)
- **Dependencies added: 0**

**Phase 2: Add only when simple breaks**
- SQLite if JSON becomes unwieldy (stdlib, not a dependency)
- LangGraph if workflow functions become complex
- FastAPI if CLI isn't sufficient
- **Add only what pain demands**

**Phase 3: Services only when libraries can't scale**
- PocketBase if SQLite + auth libraries are too much work
- Temporal if LangGraph doesn't handle distributed workflows
- **Wait for real need, not hypothetical**

**Every dependency must justify itself through pain relief.**

---

## **The Minimal First Slice**

### **What we can build with ZERO external services:**

**The Flow:**
```
1. Amplifier agent does work
   ↓
2. Saves results to JSON file (or SQLite if needed)
   ↓
3. Simple Python script reads results
   ↓
4. Displays via CLI (or simple FastAPI endpoint)
```

**Dependencies:**
- Amplifier@next (already have)
- Python stdlib (json, pathlib, sqlite3)
- Maybe: FastAPI (if web needed)
- Maybe: LangGraph (if workflows get complex)
- **That's it. Start here.**

---

## **Evolutionary Dependency Model**

### **When to Add Complexity:**

**Add LangGraph when:**
- ✅ Workflow functions become spaghetti (too many if/else)
- ✅ Need state persistence across runs
- ✅ Want visual workflow representation
- ❌ "Might need it later" - NO

**Add SQLite when:**
- ✅ JSON files become too large (>1MB)
- ✅ Need queries beyond simple reads
- ✅ Multiple processes accessing same data
- ❌ "Databases are professional" - NO

**Add FastAPI when:**
- ✅ CLI is insufficient (need web UI)
- ✅ Multiple users need access
- ✅ Browser-based interaction required
- ❌ "Web apps are modern" - NO

**Add PocketBase when:**
- ✅ Auth libraries are too much work
- ✅ Need realtime subscriptions
- ✅ Admin UI would save time
- ❌ "Integrated solutions are better" - NO

**Add Temporal when:**
- ✅ LangGraph can't handle distributed workflows
- ✅ Need industrial-grade scheduling
- ✅ Have actual distributed systems requirements
- ❌ "We'll scale eventually" - NO

**Add Tauri when:**
- ✅ Desktop distribution is validated need
- ✅ Have paying users wanting desktop app
- ✅ Python script + installer isn't sufficient
- ❌ "Desktop apps are cool" - NO

---

## **The Dependency Conscious Stack**

### **Tier 1: Always (Already Have)**
- Amplifier@next (the reason AmpBox exists)
- Python stdlib (free, always available)

### **Tier 2: Add When Simple Breaks (Libraries)**
- LangGraph - When workflow functions get complex
- SQLAlchemy - When direct SQLite is too verbose
- FastAPI - When CLI isn't sufficient
- **Cost:** Integration code + maintenance

### **Tier 3: Add When Libraries Can't Scale (Services)**
- PocketBase - When auth+DB libraries are too much work
- Temporal - When LangGraph can't handle distribution
- **Cost:** Service lifecycle + configuration + updates

### **Tier 4: Add When Validated by Users (Packaging)**
- Tauri - When users want desktop apps
- Cloudflare Workers - When users need cloud hosting
- **Cost:** Build pipeline + distribution + support

**Rule: Move down tiers ONLY when pain at current tier is proven.**

---

## **What We Build (The 10% Glue)**

### **The ONLY code AmpBox writes:**

**1. Convention-Over-Configuration Layer**
- Project structure templates
- Config file schema (ampbox.yaml)
- Sensible defaults for each tier

**2. Integration Adapters (Added As Needed)**
- Amplifier → LangGraph bridge (when LangGraph added)
- LangGraph → Database adapter (when DB added)
- Backend → Frontend bindings (when FastAPI added)
- **Write adapters only when both sides exist**

**3. CLI (Simple from Day 1)**
```bash
ampbox init          # Create project structure
ampbox dev           # Run locally (whatever tier you're at)
ampbox add <thing>   # Add dependency when needed
```

**4. Documentation**
- When to add each dependency
- How to stay at current tier as long as possible
- Migration paths between tiers

---

## **The Honest Value Proposition**

### **AmpBox doesn't make things faster by adding tools.**
### **AmpBox makes things faster by NOT adding tools until necessary.**

**For agent developers:**

**Without AmpBox:**
- "I should use PocketBase" → 2 days integrating
- "I should use Temporal" → 3 days learning + integrating
- "I should use Tauri" → 2 days setting up
- **Result:** Week of integration, maybe didn't need any of it

**With AmpBox:**
- Start: Amplifier + JSON files + Python functions
- Validate: Does this actually work for users?
- Add: Only when proven necessary
- **Result:** Days of building, not integrating

---

## **Revised Success Metrics**

### **Technical:**
- ✅ Phase 1 works with <5 dependencies (Amplifier + minimal libs)
- ✅ Each dependency addition is documented with "why we needed this"
- ✅ Can remove dependencies if they don't prove valuable

### **Developer Experience:**
- ✅ Time to first working slice: Hours (not days)
- ✅ Dependency count: <10 (not 50+)
- ✅ Maintenance burden: Minimal (fewer integrations)

### **Philosophy:**
- ✅ Every dependency justified by pain
- ✅ Start simple, grow as proven
- ✅ Can always remove complexity

---

## **The Thesis (Revised)**

**"Start with the simplest thing that could work. Add complexity only when simplicity fails."**

**AmpBox provides:**
1. **Convention over configuration** (sensible defaults, clear structure)
2. **Evolutionary path** (start minimal, add complexity when needed)
3. **Integration adapters** (only for dependencies we actually use)
4. **Clear guidance** (when to add, when to wait)

**NOT:**
- ❌ A pre-integrated stack (too much too soon)
- ❌ Mandatory services (PocketBase, Temporal, etc.)
- ❌ Complex architecture (YAGNI)

**Built on:** Amplifier@next + Whatever proves necessary + Nothing more

---

## **Alignment Check (Revised)**

Before adding ANY dependency, ask:

1. ✅ **Have we tried the simple way?** (stdlib, functions, files)
2. ✅ **Did the simple way fail?** (proven inadequate, not hypothetical)
3. ✅ **Will this dependency reduce code we maintain?** (not just shift it)
4. ✅ **Can we remove it later if wrong?** (no lock-in)
5. ✅ **Is this the minimal solution?** (not gold-plating)

**If all yes → Add the dependency**
**If any no → Stay simpler**

---

_AmpBox as "least complexity first" - add only what pain demands._
