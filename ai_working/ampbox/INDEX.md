# AmpBox API Contracts - Index

**Navigation guide for the complete API contract package**

## Quick Start

**New to the project?** Start here:
1. Read **[SUMMARY.md](SUMMARY.md)** - High-level overview
2. Review **[README.md](README.md)** - Design philosophy and rationale
3. Reference **[ampbox-api-contracts.yaml](ampbox-api-contracts.yaml)** - The authoritative spec

**Need quick answers?** Go to:
- **[API-QUICK-REFERENCE.md](API-QUICK-REFERENCE.md)** - Curl examples and common patterns

**Building an API?** Consult:
- **[API-DESIGN-PATTERNS.md](API-DESIGN-PATTERNS.md)** - Reusable patterns and best practices

---

## Document Guide

### 📋 [SUMMARY.md](SUMMARY.md)
**What:** Executive summary and implementation roadmap
**When to read:** 
- You're new to the project
- You need a high-level overview
- You're planning implementation phases

**Key sections:**
- What's included in this package
- API service groups overview
- Design philosophy summary
- Implementation phases (MVP → Production)
- Testing strategy
- Success metrics

**Time to read:** 10 minutes

---

### 📖 [README.md](README.md)
**What:** Comprehensive design documentation with philosophy and rationale
**When to read:**
- You're implementing an API service
- You need to understand design decisions
- You're reviewing API architecture

**Key sections:**
- Core design principles (ruthless simplicity, RESTful pragmatism)
- Detailed breakdown of all 7 API groups
- Design decision rationale ("Why X instead of Y?")
- Real-time streaming patterns (SSE)
- Security considerations
- Implementation guidelines with code examples
- Contract testing approach
- Versioning and deprecation strategy

**Time to read:** 45 minutes

---

### 📝 [ampbox-api-contracts.yaml](ampbox-api-contracts.yaml)
**What:** Complete OpenAPI 3.1 specification (source of truth)
**When to reference:**
- You're implementing an endpoint
- You're generating client SDKs
- You're writing contract tests
- You need exact request/response schemas

**Contains:**
- 50+ endpoint definitions
- Request/response schemas for all operations
- Authentication specifications
- Error response formats
- SSE streaming specifications
- Example payloads

**How to use:**
- View in Swagger UI / ReDoc for interactive docs
- Generate client SDKs in any language
- Validate implementation against spec
- Reference for exact contract details

---

### ⚡ [API-QUICK-REFERENCE.md](API-QUICK-REFERENCE.md)
**What:** Fast lookup guide with curl examples
**When to reference:**
- You need a quick example
- You're testing an endpoint
- You're writing documentation
- You want to try an API call

**Contains:**
- Curl examples for every endpoint
- Authentication patterns
- Pagination, filtering, sorting
- Error response formats
- SSE connection examples (JavaScript, Python)
- Common workflows
- SDK generation commands

**Time to find what you need:** <2 minutes

---

### 🎯 [API-DESIGN-PATTERNS.md](API-DESIGN-PATTERNS.md)
**What:** 15 reusable patterns for consistent API design
**When to reference:**
- You're designing a new endpoint
- You're deciding between design approaches
- You need implementation examples
- You're reviewing API design

**Patterns included:**
1. Resource-based URLs
2. Query vs path parameters
3. Pagination
4. Filtering
5. Sorting
6. Nested resources
7. Error responses
8. Async operations
9. Batch operations
10. Versioning
11. Idempotency
12. Conditional requests
13. Rate limiting
14. Webhooks
15. Health checks

**Plus:**
- Anti-patterns to avoid
- Testing strategies
- Code examples for each pattern

**Time to read:** 30 minutes (or reference specific patterns as needed)

---

## API Service Groups

### 🤖 Agent Runtime API
**Endpoints:** `/api/v1/agent/*`
**Purpose:** Manage agent execution sessions and tasks

**Quick links:**
- [Full documentation](README.md#1-agent-runtime-api)
- [OpenAPI spec](ampbox-api-contracts.yaml) (search "Agent Runtime")
- [Quick reference examples](API-QUICK-REFERENCE.md#agent-runtime)

**Key endpoints:**
- `POST /agent/sessions` - Create session
- `POST /agent/sessions/{id}/tasks` - Execute task
- `GET /agent/sessions/{id}/stream` - Stream output (SSE)

---

### 📁 Virtual Filesystem API
**Endpoints:** `/api/v1/vfs/*`
**Purpose:** Layer-based filesystem with memory semantics

**Quick links:**
- [Full documentation](README.md#2-virtual-filesystem-api)
- [OpenAPI spec](ampbox-api-contracts.yaml) (search "VFS")
- [Quick reference examples](API-QUICK-REFERENCE.md#virtual-filesystem)

**Key endpoints:**
- `GET /vfs/files?path=...` - Read file
- `POST /vfs/files` - Write file
- `POST /vfs/layers` - Mount layer

---

### 🔐 Auth Service API
**Endpoints:** `/api/v1/auth/*`
**Purpose:** Authentication and authorization

**Quick links:**
- [Full documentation](README.md#3-auth-service-api)
- [OpenAPI spec](ampbox-api-contracts.yaml) (search "Auth")
- [Quick reference examples](API-QUICK-REFERENCE.md#auth)

**Key endpoints:**
- `POST /auth/login` - User login
- `POST /auth/refresh` - Refresh token
- `POST /auth/keys` - Create API key

---

### 💾 Storage Service API
**Endpoints:** `/api/v1/storage/*`
**Purpose:** Object storage

**Quick links:**
- [Full documentation](README.md#4-storage-service-api)
- [OpenAPI spec](ampbox-api-contracts.yaml) (search "Storage")
- [Quick reference examples](API-QUICK-REFERENCE.md#storage)

**Key endpoints:**
- `POST /storage/files` - Upload file
- `GET /storage/files/{id}` - Download file

---

### 📦 Workspace Management API
**Endpoints:** `/api/v1/workspaces/*`
**Purpose:** Manage isolated work environments

**Quick links:**
- [Full documentation](README.md#5-workspace-management-api)
- [OpenAPI spec](ampbox-api-contracts.yaml) (search "Workspaces")
- [Quick reference examples](API-QUICK-REFERENCE.md#workspaces)

**Key endpoints:**
- `POST /workspaces` - Create workspace
- `POST /workspaces/{id}/share` - Share workspace

---

### ⚙️ Agent Management API
**Endpoints:** `/api/v1/agents/*`
**Purpose:** Configure and manage agent definitions

**Quick links:**
- [Full documentation](README.md#6-agent-management-api)
- [OpenAPI spec](ampbox-api-contracts.yaml) (search "Agent Management")
- [Quick reference examples](API-QUICK-REFERENCE.md#agent-management)

**Key endpoints:**
- `POST /agents` - Create agent config
- `PUT /agents/{id}` - Update config

---

### 🔧 Admin/System API
**Endpoints:** `/api/v1/system/*`, `/api/v1/admin/*`
**Purpose:** System monitoring and administration

**Quick links:**
- [Full documentation](README.md#7-adminsystem-api)
- [OpenAPI spec](ampbox-api-contracts.yaml) (search "System" or "Admin")
- [Quick reference examples](API-QUICK-REFERENCE.md#system--admin)

**Key endpoints:**
- `GET /system/status` - System health (public)
- `GET /admin/users` - List users (admin only)

---

## Common Tasks

### I want to...

#### Understand the API design philosophy
→ Read **[README.md](README.md)** sections:
- Core Philosophy
- Core Design Principles
- Design Philosophy (summary)

#### Create a new endpoint
1. Review **[API-DESIGN-PATTERNS.md](API-DESIGN-PATTERNS.md)** for relevant patterns
2. Update **[ampbox-api-contracts.yaml](ampbox-api-contracts.yaml)** with new endpoint
3. Follow implementation guidelines in **[README.md](README.md)**
4. Add examples to **[API-QUICK-REFERENCE.md](API-QUICK-REFERENCE.md)**

#### Test an existing endpoint
1. Find curl example in **[API-QUICK-REFERENCE.md](API-QUICK-REFERENCE.md)**
2. Reference exact schema in **[ampbox-api-contracts.yaml](ampbox-api-contracts.yaml)**
3. Write contract test following patterns in **[API-DESIGN-PATTERNS.md](API-DESIGN-PATTERNS.md#testing-patterns)**

#### Generate a client SDK
1. Use OpenAPI generator with **[ampbox-api-contracts.yaml](ampbox-api-contracts.yaml)**
2. See commands in **[API-QUICK-REFERENCE.md](API-QUICK-REFERENCE.md#sdk-generation)**

#### Understand a design decision
→ Check **[README.md](README.md)** "Key Design Decisions" section

#### Find a quick example
→ Go directly to **[API-QUICK-REFERENCE.md](API-QUICK-REFERENCE.md)**

#### Review implementation strategy
→ Read **[SUMMARY.md](SUMMARY.md)** "Implementation Path" section

---

## Design Principles (Quick Reference)

### ✅ Do
- Follow RESTful conventions where they add clarity
- Use standard error format across all endpoints
- Provide clear, descriptive error messages
- Document design decisions and rationale
- Test against OpenAPI contract
- Keep endpoints focused and minimal
- Use SSE for server-to-client streaming
- Version APIs in URL path (/api/v1/)

### ❌ Don't
- Create endpoints without clear purpose
- Mix error response formats
- Use POST for everything
- Expose internal implementation details
- Add complexity without justification
- Create new versions unnecessarily
- Use WebSocket unless bidirectional needed
- Break backward compatibility within a version

---

## Getting Help

### Design Questions
Consult **[README.md](README.md)** for:
- Design philosophy
- Rationale for decisions
- Implementation guidelines

### Pattern Questions
Consult **[API-DESIGN-PATTERNS.md](API-DESIGN-PATTERNS.md)** for:
- Reusable patterns
- Anti-patterns to avoid
- Code examples

### Quick Answers
Consult **[API-QUICK-REFERENCE.md](API-QUICK-REFERENCE.md)** for:
- Curl examples
- Common workflows
- SDK generation

### Exact Specifications
Consult **[ampbox-api-contracts.yaml](ampbox-api-contracts.yaml)** for:
- Request/response schemas
- Authentication details
- Error codes
- Endpoint paths

---

## Visual Overview

```
AmpBox API Contracts
│
├── SUMMARY.md                    ← START HERE (overview)
│   └── High-level summary
│   └── Implementation phases
│   └── Testing strategy
│
├── README.md                     ← DESIGN REFERENCE
│   └── Design philosophy
│   └── All 7 API groups in detail
│   └── Implementation guidelines
│   └── Contract testing
│
├── ampbox-api-contracts.yaml     ← SOURCE OF TRUTH
│   └── Complete OpenAPI spec
│   └── All endpoints defined
│   └── Request/response schemas
│   └── Use for: SDK generation, contract tests
│
├── API-QUICK-REFERENCE.md        ← QUICK LOOKUP
│   └── Curl examples
│   └── Common patterns
│   └── Workflows
│
└── API-DESIGN-PATTERNS.md        ← PATTERN LIBRARY
    └── 15 reusable patterns
    └── Anti-patterns
    └── Code examples
```

---

## Maintenance

### When Adding a New Endpoint

1. **Design:** Review patterns in `API-DESIGN-PATTERNS.md`
2. **Specify:** Add to `ampbox-api-contracts.yaml`
3. **Document:** Update `README.md` with rationale
4. **Example:** Add curl example to `API-QUICK-REFERENCE.md`
5. **Test:** Write contract test validating spec compliance

### When Changing an Endpoint

1. **Check:** Is this a breaking change?
2. **If breaking:** Consider deprecation path, version bump
3. **If compatible:** Add optional fields, maintain backward compatibility
4. **Update:** All relevant documentation
5. **Test:** Verify existing tests still pass

### When Deprecating an Endpoint

1. **Add deprecation headers** to endpoint response
2. **Document migration path** in `README.md`
3. **Update** `ampbox-api-contracts.yaml` with deprecation notice
4. **Maintain** for 6+ months
5. **Remove** only in new major version

---

## Package Contents Summary

**5 files, complete API contract package:**

| File | Purpose | Size | Read Time |
|------|---------|------|-----------|
| `INDEX.md` | Navigation (this file) | ~8 KB | 5 min |
| `SUMMARY.md` | Executive overview | ~15 KB | 10 min |
| `README.md` | Comprehensive docs | ~40 KB | 45 min |
| `ampbox-api-contracts.yaml` | OpenAPI spec | ~60 KB | Reference |
| `API-QUICK-REFERENCE.md` | Quick examples | ~20 KB | <2 min (search) |
| `API-DESIGN-PATTERNS.md` | Pattern library | ~35 KB | 30 min |

**Total:** ~178 KB of documentation
**Time investment:** ~2 hours to read everything (or reference as needed)

---

## Remember

**The contracts are the "studs" - the connection points between system bricks.**

- Clear and stable
- Well-documented
- Regeneratable
- Testable
- Complete but minimal

**Every endpoint has a clear purpose. Every response follows a pattern. Every error is understandable.**

**Good APIs are boring APIs - they work predictably, every time.**

---

**Ready to build? Start with [SUMMARY.md](SUMMARY.md) → [README.md](README.md) → [ampbox-api-contracts.yaml](ampbox-api-contracts.yaml)**
