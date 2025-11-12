# AmpBox API Contracts - Summary

**Complete API design for infrastructure-as-a-box platform**

## What's Included

### 1. OpenAPI Specification (`ampbox-api-contracts.yaml`)
**The source of truth for all API contracts**

- Complete OpenAPI 3.1 specification
- 7 service groups with 50+ endpoints
- Request/response schemas for all operations
- Authentication and error handling patterns
- SSE streaming specifications
- Ready for:
  - Interactive documentation (Swagger UI, ReDoc)
  - Client SDK generation (Python, TypeScript, Go, Java, etc.)
  - Contract testing
  - Automated validation

### 2. Comprehensive Documentation (`README.md`)
**Design philosophy, patterns, and implementation guidance**

Covers:
- Core design principles (ruthless simplicity, RESTful pragmatism)
- Detailed explanation of each API group
- Design decisions with rationale
- Real-time streaming patterns (SSE)
- Security considerations
- Implementation guidelines with code examples
- Contract testing approach
- Versioning strategy

### 3. Quick Reference (`API-QUICK-REFERENCE.md`)
**Fast lookup for developers**

Includes:
- Common API calls with curl examples
- Authentication patterns
- Pagination, filtering, sorting
- Error response formats
- SSE connection examples (JavaScript, Python)
- Common workflows
- SDK generation commands

### 4. Design Patterns (`API-DESIGN-PATTERNS.md`)
**Reusable patterns for consistent APIs**

Documents 15 core patterns:
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

Plus anti-patterns to avoid and testing strategies.

## API Service Groups

### 1. Agent Runtime API (8 endpoints)
**Core agent execution capabilities**

- Session lifecycle management
- Task execution
- Real-time output streaming (SSE)
- Session termination

**Key Innovation:** Separate session (environment) from tasks (work units)

### 2. Virtual Filesystem API (9 endpoints)
**Layered filesystem with memory semantics**

- File read/write operations
- Directory listing
- Layer mounting with priority
- File resolution debugging
- Snapshot creation
- Change notifications (SSE)

**Key Innovation:** Multi-layer VFS with explicit priority control

### 3. Auth Service API (6 endpoints)
**Authentication and authorization**

- User login/logout
- Token refresh
- API key management
- Token verification

**Key Innovation:** Dual authentication (tokens for users, API keys for machines)

### 4. Storage Service API (5 endpoints)
**Object storage**

- File upload/download
- Metadata retrieval
- File listing with filtering

**Key Innovation:** Metadata endpoint for efficient browsing

### 5. Workspace Management API (5 endpoints)
**Isolated work environments**

- Workspace creation/deletion
- Workspace sharing with permissions
- Workspace listing

**Key Innovation:** Permission-based sharing model

### 6. Agent Management API (5 endpoints)
**Agent configuration**

- Create/update/delete agent configs
- List agent configs
- Get config details

**Key Innovation:** Separation of config (template) from sessions (instances)

### 7. Admin/System API (5 endpoints)
**System monitoring and administration**

- System health status
- User management
- Log viewing
- Metrics retrieval
- Multi-tenant management

**Key Innovation:** Public health endpoint + authenticated admin endpoints

## Design Philosophy

### Core Principles

1. **Ruthless Simplicity**
   - Every endpoint must justify its existence
   - Minimal but complete
   - No unnecessary abstractions

2. **RESTful Pragmatism**
   - Follow REST when it adds clarity
   - Action endpoints (POST /resource/{id}/action) when clearer than pure REST
   - HTTP methods used appropriately

3. **Consistent Patterns**
   - Standard error format across all endpoints
   - Uniform pagination (limit/offset)
   - Consistent authentication
   - Clear naming conventions

4. **Versioned Contracts**
   - URL path versioning (/api/v1/)
   - Stay on v1 as long as possible
   - Add optional fields rather than new versions
   - Version entire API modules, not individual endpoints

5. **Real-time Ready**
   - SSE for server-to-client streaming
   - WebSocket only when bidirectional needed
   - Clear event types and data structures

### Error Response Standard

**Every error follows this format:**

```json
{
  "error": {
    "code": "MACHINE_READABLE_CODE",
    "message": "Human-readable description",
    "details": {}
  }
}
```

**Benefits:**
- Client can branch on error codes
- Humans get useful messages
- Optional details for context
- Consistent across entire platform

### Authentication

**Two methods supported:**

1. **Bearer Token** (user sessions, short-lived)
   ```
   Authorization: Bearer <jwt_token>
   ```

2. **API Key** (programmatic access, long-lived)
   ```
   X-API-Key: <api_key>
   ```

Both validated by API Gateway before routing to services.

## Key Design Decisions

### Why SSE Instead of WebSocket?

**For agent output streaming:**
- Unidirectional (server → client)
- HTTP-based (easier to proxy, debug, cache)
- Automatic reconnection
- Simpler than WebSocket
- Good enough for current needs

**When to use WebSocket:**
- Bidirectional communication needed
- Very low latency required
- Binary protocols

### Why Separate Session from Task?

**Agent Runtime API has two resources:**
- **Session:** Runtime environment with state
- **Task:** Discrete work unit within session

**Benefits:**
- Multiple tasks per session without setup overhead
- Clear lifecycle management
- Can terminate session (kills all tasks)
- Can check task status independently

### Why Query Params for File Paths?

```
GET /vfs/files?path=/workspace/config.yaml
```

**Instead of:**
```
GET /vfs/files/workspace/config.yaml
```

**Reasons:**
- Avoids URL encoding issues
- Clearer separation (resource type vs identifier)
- Simpler to handle optional parameters
- Easier to debug

### Why Layer Priority in VFS?

**Explicit priority control:**
```
Layer "workspace" (priority 100) → checked first
Layer "base"      (priority 0)   → fallback
```

**Benefits:**
- User controls file resolution order
- Makes layer dependencies visible
- Enables debugging (which layer provides this file?)
- Supports complex overlay scenarios

## Implementation Path

### Phase 1: Core APIs (MVP)
1. **Auth Service** - Login, tokens, API keys
2. **Agent Runtime** - Sessions, tasks, streaming
3. **VFS** - Basic file ops, single layer
4. **Workspaces** - Create, list, delete

**Validate:** Can create workspace, run agent task, stream output

### Phase 2: Enhanced Functionality
5. **Storage Service** - File upload/download
6. **VFS Layers** - Multi-layer mounting, resolution
7. **Agent Management** - Config CRUD
8. **Workspace Sharing** - Permissions

**Validate:** Full workflow with shared workspace

### Phase 3: Operations & Admin
9. **System API** - Health checks, metrics
10. **Admin API** - User management, logs
11. **Rate Limiting** - Per-user quotas
12. **Monitoring** - Observability

**Validate:** Production-ready deployment

## Testing Strategy

### Contract Tests
**Verify API matches OpenAPI spec**

```python
def test_create_session_contract():
    response = client.post('/api/v1/agent/sessions',
                          json={'agent_id': 'test'})
    assert response.status_code == 201
    assert_matches_schema(response.json(), 'AgentSession')
```

### Integration Tests
**Verify end-to-end workflows**

```python
@pytest.mark.integration
async def test_agent_execution_flow():
    session = await create_session()
    task = await execute_task(session.id, "test")
    result = await wait_for_completion(task.id)
    assert result.status == 'completed'
```

### Load Tests
**Verify performance under load**

```python
async def test_concurrent_sessions():
    sessions = await asyncio.gather(*[
        create_session() for _ in range(100)
    ])
    assert len(sessions) == 100
```

## SDK Generation

Generate client SDKs from OpenAPI spec:

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

**Benefits:**
- Type-safe clients
- Automatic serialization/deserialization
- Built-in error handling
- Always in sync with API spec

## Documentation Generation

Generate interactive API docs:

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

## Next Steps

### For Implementation
1. **Read `README.md`** - Understand design philosophy and rationale
2. **Review `ampbox-api-contracts.yaml`** - The authoritative spec
3. **Reference `API-DESIGN-PATTERNS.md`** - Follow established patterns
4. **Use `API-QUICK-REFERENCE.md`** - Quick lookup during development

### For Testing
1. Generate contract tests from OpenAPI spec
2. Implement integration tests for workflows
3. Add load tests for performance validation

### For Documentation
1. Generate interactive docs (Swagger UI / ReDoc)
2. Create client SDK examples
3. Write integration guides for common workflows

### For Evolution
1. Monitor API usage patterns
2. Collect feedback from consumers
3. Identify pain points
4. Consider breaking changes only when necessary
5. Maintain v1 as long as possible

## Principles for Evolution

### Add, Don't Break

**Prefer:**
- Adding optional fields
- Adding new endpoints
- Expanding enum values (with backward compatibility)

**Avoid:**
- Removing fields
- Changing field types
- Removing endpoints
- Breaking authentication

### Deprecate Gracefully

**When breaking changes are unavoidable:**
1. Add deprecation headers to old endpoints
2. Document migration path
3. Maintain old version for 6+ months
4. Provide clear sunset timeline
5. Create v2 only after v1 deprecation period

### Version Carefully

**Create new version only when:**
- Breaking changes truly necessary
- Can't maintain backward compatibility
- Benefits outweigh migration costs

**Remember:** Every new version fragments the ecosystem.

## Key Metrics for Success

### API Health
- ✅ All endpoints documented in OpenAPI
- ✅ Consistent error responses
- ✅ Standard authentication
- ✅ Contract tests passing
- ✅ Integration tests covering workflows

### Developer Experience
- ✅ Generated SDKs available
- ✅ Interactive documentation live
- ✅ Quick reference for common tasks
- ✅ Clear examples in all languages
- ✅ Fast response times (<100ms for simple requests)

### System Quality
- ✅ Follows AmpBox philosophy (ruthless simplicity)
- ✅ RESTful where it makes sense
- ✅ Real-time streaming where needed
- ✅ Secure by default
- ✅ Observable and debuggable

## Summary

AmpBox APIs are designed as **clear, stable connection points** between system components. Following the "bricks and studs" philosophy, each API is a well-defined contract that enables:

- **Modular regeneration** - Rebuild any service without breaking consumers
- **Independent scaling** - Scale services based on load patterns
- **Clear ownership** - Each API group has focused responsibility
- **Easy testing** - Contract tests verify compliance
- **SDK generation** - Clients in any language
- **Interactive docs** - Self-service documentation

The design embodies **ruthless simplicity**:
- Every endpoint justified
- Consistent patterns throughout
- Minimal but complete
- RESTful pragmatism
- Standard error handling
- Clear authentication

**The contracts are ready. Build with confidence.**

---

## Files in This Package

1. **`ampbox-api-contracts.yaml`** - Complete OpenAPI 3.1 specification (source of truth)
2. **`README.md`** - Comprehensive design documentation with philosophy and rationale
3. **`API-QUICK-REFERENCE.md`** - Fast lookup guide with curl examples
4. **`API-DESIGN-PATTERNS.md`** - 15 reusable patterns for consistent API design
5. **`SUMMARY.md`** - This file: overview and implementation roadmap

**Start with `README.md` → Reference `ampbox-api-contracts.yaml` → Use patterns from `API-DESIGN-PATTERNS.md`**
