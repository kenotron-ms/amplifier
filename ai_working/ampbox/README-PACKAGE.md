# AmpBox API Contracts Package

**Complete API design for infrastructure-as-a-box platform**

## What You're Looking At

This is a complete, production-ready API contract specification for the AmpBox platform. It includes:

✅ **Complete OpenAPI 3.1 Specification** (1,826 lines)
✅ **Comprehensive Design Documentation** (4,653 total lines)
✅ **Quick Reference Guide** for developers
✅ **Reusable Design Patterns** library
✅ **Implementation Roadmap** with phasing

## Quick Navigation

**Start here:**
→ **[INDEX.md](INDEX.md)** - Navigation guide for the entire package

**Then read:**
1. **[SUMMARY.md](SUMMARY.md)** - Executive overview (10 min)
2. **[README.md](README.md)** - Full design documentation (45 min)

**Reference as needed:**
- **[API-QUICK-REFERENCE.md](API-QUICK-REFERENCE.md)** - Curl examples
- **[API-DESIGN-PATTERNS.md](API-DESIGN-PATTERNS.md)** - Pattern library
- **[ampbox-api-contracts.yaml](ampbox-api-contracts.yaml)** - OpenAPI spec

## What's Included

### 1. OpenAPI Specification (ampbox-api-contracts.yaml)
**The source of truth**

- Complete OpenAPI 3.1 specification
- 7 service groups, 50+ endpoints
- All request/response schemas
- Authentication patterns
- Error response formats
- SSE streaming specifications

**Use for:**
- SDK generation (Python, TypeScript, Go, Java, etc.)
- Contract testing
- Interactive documentation (Swagger UI, ReDoc)
- API validation

### 2. Design Documentation (README.md)
**Philosophy and rationale**

- Core design principles
- Detailed API group explanations
- Design decision rationale
- Real-time streaming patterns
- Security considerations
- Implementation guidelines
- Testing strategies
- Versioning approach

### 3. Quick Reference (API-QUICK-REFERENCE.md)
**Fast lookup for developers**

- Curl examples for every endpoint
- Authentication patterns
- Common workflows
- SSE connection examples
- SDK generation commands

### 4. Design Patterns (API-DESIGN-PATTERNS.md)
**Reusable patterns**

15 core patterns:
- Resource-based URLs
- Pagination, filtering, sorting
- Error responses
- Async operations
- Versioning
- Rate limiting
- And more...

### 5. Summary & Roadmap (SUMMARY.md)
**Overview and implementation path**

- High-level summary
- API service groups overview
- Implementation phases (MVP → Production)
- Testing strategy
- Success metrics

### 6. Navigation Guide (INDEX.md)
**How to use this package**

- Quick start guide
- Document overview
- Common tasks
- Maintenance guidelines

## API Service Groups

### 🤖 Agent Runtime API (8 endpoints)
Manage agent execution sessions and tasks
- Create/terminate sessions
- Execute tasks
- Stream output (SSE)

### 📁 Virtual Filesystem API (9 endpoints)
Layer-based filesystem with memory semantics
- Read/write files
- Mount/unmount layers
- Resolve paths across layers

### 🔐 Auth Service API (6 endpoints)
Authentication and authorization
- User login/logout
- Token management
- API key management

### 💾 Storage Service API (5 endpoints)
Object storage
- Upload/download files
- Metadata retrieval

### 📦 Workspace Management API (5 endpoints)
Isolated work environments
- Create/delete workspaces
- Share with permissions

### ⚙️ Agent Management API (5 endpoints)
Agent configuration
- Create/update/delete configs
- List configurations

### 🔧 Admin/System API (5 endpoints)
System monitoring and administration
- Health checks
- User management
- Logs and metrics

## Design Philosophy

### Core Principles

**Ruthless Simplicity**
- Every endpoint must justify its existence
- Minimal but complete
- No unnecessary abstractions

**RESTful Pragmatism**
- Follow REST when it adds clarity
- Action endpoints when clearer
- HTTP methods used appropriately

**Consistent Patterns**
- Standard error format
- Uniform pagination
- Consistent authentication

**Versioned Contracts**
- URL path versioning (/api/v1/)
- Stay on v1 as long as possible
- Add optional fields vs new versions

**Real-time Ready**
- SSE for streaming
- WebSocket only when needed

### Error Response Standard

Every error follows this format:

```json
{
  "error": {
    "code": "MACHINE_READABLE_CODE",
    "message": "Human-readable description",
    "details": {}
  }
}
```

## Generate Client SDKs

```bash
# Python
openapi-python-client generate --path ampbox-api-contracts.yaml

# TypeScript
npx openapi-typescript ampbox-api-contracts.yaml --output ampbox-api.ts

# Go
oapi-codegen -generate types,client ampbox-api-contracts.yaml > client.go

# Java
openapi-generator-cli generate -i ampbox-api-contracts.yaml -g java
```

## Generate Interactive Docs

```bash
# Swagger UI
docker run -p 8080:8080 \
  -e SWAGGER_JSON=/api/ampbox-api-contracts.yaml \
  -v $(pwd):/api swaggerapi/swagger-ui

# ReDoc
docker run -p 8080:80 \
  -e SPEC_URL=/api/ampbox-api-contracts.yaml \
  -v $(pwd):/api redocly/redoc

# Open http://localhost:8080
```

## Implementation Phases

### Phase 1: Core APIs (MVP)
- Auth Service
- Agent Runtime
- Basic VFS
- Workspaces

**Goal:** Create workspace, run agent task, stream output

### Phase 2: Enhanced Functionality
- Storage Service
- VFS layers
- Agent Management
- Workspace sharing

**Goal:** Full workflow with shared workspace

### Phase 3: Operations & Admin
- System API
- Admin API
- Rate limiting
- Monitoring

**Goal:** Production-ready deployment

## Package Statistics

| File | Lines | Size | Purpose |
|------|-------|------|---------|
| ampbox-api-contracts.yaml | 1,826 | 46 KB | OpenAPI spec |
| README.md | 615 | 17 KB | Design docs |
| API-QUICK-REFERENCE.md | 556 | 10 KB | Quick examples |
| API-DESIGN-PATTERNS.md | 737 | 16 KB | Pattern library |
| SUMMARY.md | 482 | 12 KB | Overview |
| INDEX.md | 437 | 12 KB | Navigation |
| **Total** | **4,653** | **113 KB** | Complete package |

## Key Design Decisions

### Why SSE for Streaming?
- Unidirectional (server → client)
- HTTP-based (easier to proxy, debug)
- Automatic reconnection
- Simpler than WebSocket

### Why Separate Session from Task?
- Session = runtime environment
- Task = work unit
- Multiple tasks per session
- Clear lifecycle management

### Why Query Params for File Paths?
- Avoids URL encoding issues
- Clear separation of concerns
- Simpler parameter handling

### Why Layer Priority in VFS?
- User controls file resolution
- Makes dependencies visible
- Enables debugging

## Quality Standards

This API design follows AmpBox's implementation philosophy:

✅ **Ruthless simplicity** - Every endpoint justified
✅ **Architectural integrity** - Clean patterns throughout
✅ **Clear contracts** - Well-documented, testable
✅ **Modular design** - Independent, regeneratable services
✅ **Real-time ready** - SSE for streaming where needed

## Testing Strategy

### Contract Tests
Verify implementation matches OpenAPI spec

### Integration Tests
Verify end-to-end workflows

### Load Tests
Verify performance under load

**See:** [API-DESIGN-PATTERNS.md](API-DESIGN-PATTERNS.md#testing-patterns) for examples

## Next Steps

### For Architects
1. Review [SUMMARY.md](SUMMARY.md) for overview
2. Read [README.md](README.md) for detailed design
3. Validate against requirements

### For Developers
1. Review [ampbox-api-contracts.yaml](ampbox-api-contracts.yaml)
2. Reference [API-QUICK-REFERENCE.md](API-QUICK-REFERENCE.md)
3. Follow patterns in [API-DESIGN-PATTERNS.md](API-DESIGN-PATTERNS.md)

### For Testers
1. Generate contract tests from OpenAPI spec
2. Implement integration tests
3. Add load tests

### For Documentation
1. Generate interactive docs (Swagger UI / ReDoc)
2. Create SDK examples
3. Write integration guides

## Remember

**APIs are the "studs" - the connection points between system bricks.**

- Clear and stable
- Well-documented
- Regeneratable
- Testable
- Complete but minimal

**Every endpoint has a clear purpose.**
**Every response follows a pattern.**
**Every error is understandable.**

**Good APIs are boring APIs - they work predictably, every time.**

---

**Ready to dive in? Start with [INDEX.md](INDEX.md) for navigation guidance.**
