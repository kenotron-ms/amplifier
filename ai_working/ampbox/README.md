# AmpBox API Contracts

**Comprehensive API design for the AmpBox infrastructure-as-a-box platform**

## Overview

AmpBox APIs are designed following the "bricks and studs" philosophy - clear, stable connection points between system components. Each API is a well-defined contract that enables modular regeneration without breaking consumers.

## Design Philosophy

### Core Principles

1. **RESTful Pragmatism** - Follow REST when it adds clarity, but embrace RPC-style for complex operations
2. **Ruthless Simplicity** - Every endpoint must justify its existence
3. **Consistent Patterns** - Uniform error handling, pagination, filtering across all endpoints
4. **Versioned Contracts** - `/api/v1/` prefix, stay on v1 as long as possible
5. **Real-time Ready** - SSE for streaming, WebSocket when bidirectional needed

### Error Response Standard

All errors follow this format:

```json
{
  "error": {
    "code": "AGENT_SESSION_NOT_FOUND",
    "message": "Agent session abc123 not found",
    "details": {}
  }
}
```

**Benefits:**
- Machine-readable error codes for client logic
- Human-readable messages for debugging
- Optional details for additional context
- Consistent across all services

### Authentication

Two methods supported:

1. **Bearer Token** (for user sessions)
   ```
   Authorization: Bearer <jwt_token>
   ```

2. **API Key** (for programmatic access)
   ```
   X-API-Key: <api_key>
   ```

### Pagination

List endpoints follow standard pagination:

```
GET /api/v1/resource?limit=20&offset=0
```

Response includes:
```json
{
  "items": [...],
  "total": 150,
  "limit": 20,
  "offset": 0
}
```

## API Groups

### 1. Agent Runtime API

**Purpose:** Manage agent execution sessions and tasks

**Core Endpoints:**
- `POST /agent/sessions` - Create agent session
- `POST /agent/sessions/{id}/tasks` - Execute task
- `GET /agent/sessions/{id}/stream` - SSE stream for output
- `DELETE /agent/sessions/{id}` - Terminate session

**Key Design Decisions:**

**Why separate session creation from task execution?**
- Sessions represent runtime environment with state
- Tasks are discrete units of work within that environment
- Allows multiple tasks per session without overhead of session setup

**Why SSE for streaming vs WebSocket?**
- SSE is simpler (unidirectional, HTTP-based)
- Agent output is primarily server → client
- Easier to proxy, debug, and cache
- Use WebSocket only if bidirectional becomes necessary

**Session Lifecycle:**
```
pending → running → (completed | failed | terminated)
```

**Example Flow:**
```bash
# 1. Create session
curl -X POST /api/v1/agent/sessions \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"agent_id": "code-analyzer", "workspace_id": "ws-123"}'
# → {"session_id": "sess-abc", "status": "pending"}

# 2. Execute task
curl -X POST /api/v1/agent/sessions/sess-abc/tasks \
  -d '{"task": "Analyze error patterns in logs"}'
# → {"task_id": "task-xyz", "status": "pending"}

# 3. Stream output
curl -N /api/v1/agent/sessions/sess-abc/stream
# → SSE stream with events: output, tool_call, task_completed
```

### 2. Virtual Filesystem API

**Purpose:** Layer-based filesystem with memory semantics

**Core Endpoints:**
- `GET /vfs/files?path=/workspace/src/main.py` - Read file
- `POST /vfs/files` - Write file
- `GET /vfs/directories?path=/workspace` - List directory
- `POST /vfs/layers` - Mount layer
- `GET /vfs/files/resolve?path=/config/app.yaml` - Show which layer provides file

**Key Design Decisions:**

**Why query parameter for file path instead of path param?**
- Avoids URL encoding issues with `/` in paths
- Simpler to handle optional parameters
- Clear separation: resource type in path, resource identifier in query

**Why explicit layer mounting?**
- Gives users control over precedence
- Makes layer dependencies visible
- Enables debugging ("which layer provides this file?")

**Layer Priority System:**
```
Higher priority → checked first during file resolution
Example:
  Layer "workspace" (priority 100) → /workspace/config.yaml
  Layer "base"      (priority 0)   → /workspace/config.yaml
  
  resolve("/workspace/config.yaml") → returns from "workspace" layer
```

**Example Flow:**
```bash
# Mount base layer
curl -X POST /api/v1/vfs/layers \
  -d '{"layer_id": "base-ubuntu", "mount_point": "/", "priority": 0}'

# Mount workspace layer
curl -X POST /api/v1/vfs/layers \
  -d '{"layer_id": "user-workspace", "mount_point": "/workspace", "priority": 100}'

# Read file (checks workspace first, falls back to base)
curl /api/v1/vfs/files?path=/workspace/config.yaml

# Debug file resolution
curl /api/v1/vfs/files/resolve?path=/workspace/config.yaml
# → {"path": "/workspace/config.yaml", "layer": "user-workspace", 
#     "layers_checked": ["user-workspace", "base-ubuntu"]}
```

### 3. Auth Service API

**Purpose:** Authentication and API key management

**Core Endpoints:**
- `POST /auth/login` - User login (no auth required)
- `POST /auth/refresh` - Refresh access token
- `POST /auth/keys` - Create API key
- `DELETE /auth/keys/{key_id}` - Revoke API key

**Key Design Decisions:**

**Why separate access and refresh tokens?**
- Access tokens short-lived (15-60 min) → less risk if stolen
- Refresh tokens long-lived → better UX, stored securely
- Enables token rotation without re-authentication

**Why separate API keys from user tokens?**
- API keys for machines, tokens for humans
- Different security models (long-lived vs short-lived)
- Different rotation strategies

**API Key Best Practices:**
- Key value shown only once on creation
- Support optional expiration dates
- Track last_used_at for auditing
- Allow multiple keys per user (for key rotation)

### 4. Storage Service API

**Purpose:** Simple object storage

**Core Endpoints:**
- `POST /storage/files` - Upload file
- `GET /storage/files/{file_id}` - Download file
- `DELETE /storage/files/{file_id}` - Delete file
- `GET /storage/files/{file_id}/metadata` - Get metadata without downloading

**Key Design Decisions:**

**Why separate metadata endpoint?**
- Avoid downloading large files just to check properties
- Enables efficient file browsing
- Supports conditional downloads based on metadata

**Why multipart/form-data for upload?**
- Standard browser file upload format
- Supports large files
- Can include metadata in same request

**File Organization:**
```
No enforced hierarchy - flat namespace with paths
Users organize via path prefixes:
  /user-123/projects/amplifier/data.json
  /user-123/projects/ampbox/config.yaml
```

### 5. Workspace Management API

**Purpose:** Manage isolated work environments

**Core Endpoints:**
- `POST /workspaces` - Create workspace
- `GET /workspaces` - List workspaces
- `POST /workspaces/{id}/share` - Share with user
- `DELETE /workspaces/{id}` - Delete workspace

**Key Design Decisions:**

**Why separate workspaces from VFS layers?**
- Workspaces are logical groupings (project, user, team)
- VFS layers are technical (OS, dependencies, user files)
- Workspaces can have multiple VFS layers
- Enables sharing at workspace level without exposing layer details

**Sharing Model:**
```json
{
  "user_id": "user-456",
  "permissions": ["read", "write", "execute", "admin"]
}
```

Permissions:
- `read` - View workspace and files
- `write` - Modify files
- `execute` - Run agent sessions in workspace
- `admin` - Share workspace, delete workspace

### 6. Agent Management API

**Purpose:** Configure and manage agent definitions

**Core Endpoints:**
- `POST /agents` - Create agent config
- `PUT /agents/{agent_id}` - Update config
- `GET /agents` - List configs
- `DELETE /agents/{agent_id}` - Delete config

**Key Design Decisions:**

**Agent Config Structure:**
```json
{
  "name": "Code Analyzer",
  "model": "claude-3-5-sonnet-20241022",
  "system_prompt": "You are a code analysis expert...",
  "tools": ["read_file", "search_code", "run_linter"],
  "config": {
    "temperature": 0.7,
    "max_tokens": 4096
  }
}
```

**Why separate agent configs from sessions?**
- Config is template (reusable definition)
- Session is instance (runtime state)
- Enables versioning configs without affecting running sessions
- Multiple sessions can use same config

### 7. Admin/System API

**Purpose:** System monitoring and administration

**Core Endpoints:**
- `GET /system/status` - Health check (public)
- `GET /admin/users` - List users (admin only)
- `GET /admin/logs` - View logs (admin only)
- `GET /admin/metrics` - System metrics (admin only)

**Key Design Decisions:**

**Why public health check?**
- Load balancers need unauthenticated endpoint
- Monitoring systems need quick status check
- No sensitive information exposed

**Admin Authorization:**
- Requires valid auth token
- Additional permission check for admin role
- Returns 403 if authenticated but not admin

## Real-Time Streaming

### Server-Sent Events (SSE)

Used for:
- Agent output streaming (`/agent/sessions/{id}/stream`)
- File change notifications (`/vfs/watch`)

**Why SSE?**
- Simple unidirectional streaming
- Built on HTTP (works with existing infrastructure)
- Automatic reconnection
- Event types for structured data

**Event Format:**
```
event: output
data: {"text": "Processing file...", "timestamp": "2024-01-15T10:30:00Z"}

event: tool_call
data: {"tool": "read_file", "args": {"path": "/src/main.py"}}

event: task_completed
data: {"task_id": "task-123", "result": {...}}
```

**Client Example:**
```javascript
const eventSource = new EventSource('/api/v1/agent/sessions/sess-abc/stream', {
  headers: { 'Authorization': `Bearer ${token}` }
});

eventSource.addEventListener('output', (e) => {
  const data = JSON.parse(e.data);
  console.log(data.text);
});

eventSource.addEventListener('task_completed', (e) => {
  const data = JSON.parse(e.data);
  console.log('Task completed:', data.result);
  eventSource.close();
});
```

## Versioning Strategy

**Current:** `/api/v1/`

**When to create v2:**
- Breaking changes to request/response schemas
- Removing endpoints
- Changing authentication mechanism

**Prefer instead:**
- Adding optional fields (backward compatible)
- Adding new endpoints (doesn't break existing clients)
- Deprecation warnings before removal

**Deprecation Process:**
1. Add deprecation header: `Deprecation: true`
2. Document sunset date: `Sunset: Sat, 31 Dec 2025 23:59:59 GMT`
3. Maintain for at least 6 months
4. Create v2 with breaking changes
5. Run both versions in parallel during migration

## Contract Testing

Each API endpoint should have contract tests verifying:

1. **Request validation** - Rejects invalid requests
2. **Response format** - Returns correct schema
3. **Error handling** - Standard error format
4. **Authentication** - Requires proper auth
5. **Authorization** - Enforces permissions

**Example Test Structure:**
```python
def test_create_agent_session():
    # Happy path
    response = client.post('/api/v1/agent/sessions', 
                          json={'agent_id': 'test-agent'},
                          headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 201
    assert 'session_id' in response.json()
    
    # Missing required field
    response = client.post('/api/v1/agent/sessions',
                          json={},
                          headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 400
    assert response.json()['error']['code'] == 'MISSING_REQUIRED_FIELD'
    
    # Missing auth
    response = client.post('/api/v1/agent/sessions',
                          json={'agent_id': 'test-agent'})
    assert response.status_code == 401
```

## Implementation Guidelines

### Minimal Implementation First

Start with simplest working version:

```python
# Good: Simple, focused endpoint
@app.post("/api/v1/agent/sessions")
async def create_session(request: CreateSessionRequest, user = Depends(get_current_user)):
    session = agent_runtime.create_session(
        agent_id=request.agent_id,
        user_id=user.id
    )
    return session

# Avoid: Over-engineered with unnecessary abstractions
@app.post("/api/v1/agent/sessions")
async def create_session(
    request: CreateSessionRequest,
    user = Depends(get_current_user),
    session_factory = Depends(get_session_factory),
    validator = Depends(get_request_validator),
    metrics = Depends(get_metrics_collector)
):
    await validator.validate(request)
    await metrics.record_request("create_session")
    session = await session_factory.create(
        agent_id=request.agent_id,
        user_id=user.id,
        context=await request.get_context()
    )
    await metrics.record_creation(session.id)
    return session
```

### Error Handling

```python
# Standard error responses
class APIError(Exception):
    def __init__(self, code: str, message: str, status_code: int = 400, details: dict = None):
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details or {}

# Usage
if not session:
    raise APIError(
        code="AGENT_SESSION_NOT_FOUND",
        message=f"Agent session {session_id} not found",
        status_code=404
    )

# Error handler
@app.exception_handler(APIError)
async def api_error_handler(request: Request, exc: APIError):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.code,
                "message": exc.message,
                "details": exc.details
            }
        }
    )
```

### Response Models

Use Pydantic for automatic validation and documentation:

```python
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class AgentSessionResponse(BaseModel):
    session_id: str = Field(description="Unique session identifier")
    agent_id: str = Field(description="Agent configuration ID")
    status: str = Field(description="Session status")
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "session_id": "sess-abc123",
                "agent_id": "code-analyzer",
                "status": "running",
                "created_at": "2024-01-15T10:30:00Z"
            }
        }
```

## API Gateway Pattern

**Stateless Gateway:**
```
Client Request
    ↓
API Gateway (stateless routing)
    ↓
┌─────────────┬──────────────┬──────────────┐
│   Agent     │     VFS      │    Auth      │
│   Runtime   │   Service    │   Service    │
└─────────────┴──────────────┴──────────────┘
```

**Gateway Responsibilities:**
- Route requests to services
- Authenticate tokens/API keys
- Rate limiting
- Request/response logging
- CORS handling

**Gateway Does NOT:**
- Store session state
- Make business logic decisions
- Cache responses (initially)
- Transform data (pass through)

## Security Considerations

### Authentication
- JWT tokens with short expiration (15-60 min)
- Refresh tokens stored securely (HTTP-only cookies or secure storage)
- API keys for programmatic access only

### Authorization
- Every endpoint checks permissions
- Resource-level ACLs for fine-grained control
- Admin endpoints require explicit admin role

### Input Validation
- All inputs validated via Pydantic models
- Path traversal prevention in file paths
- SQL injection prevention (use parameterized queries)
- Size limits on uploads

### Rate Limiting
- Per-user limits on API calls
- Per-IP limits on unauthenticated endpoints
- Separate limits for expensive operations (agent sessions)

## Future Considerations

**Not implemented yet, add when needed:**

1. **GraphQL API** - If clients need flexible querying
2. **Webhooks** - For external service notifications
3. **Bulk Operations** - For batch processing
4. **API Versioning in Headers** - Alternative to URL versioning
5. **Content Negotiation** - Supporting XML, Protobuf, etc.
6. **Caching** - ETags, Cache-Control headers
7. **Conditional Requests** - If-Modified-Since, If-None-Match

**Remember:** Add complexity only when actual need arises.

## Documentation

The OpenAPI specification (`ampbox-api-contracts.yaml`) serves as:
1. **API Reference** - Complete endpoint documentation
2. **Client Generation** - Generate SDKs in any language
3. **Contract Tests** - Validate implementation matches spec
4. **Interactive Docs** - Swagger UI, ReDoc

**View Interactive Docs:**
```bash
# Using Swagger UI
docker run -p 8080:8080 -e SWAGGER_JSON=/api/ampbox-api-contracts.yaml \
  -v $(pwd):/api swaggerapi/swagger-ui

# Open http://localhost:8080
```

## Contract Evolution

As system evolves:

1. **Update OpenAPI spec first** - Design before implementing
2. **Generate/update tests** - Verify contract compliance
3. **Implement service** - Build to match spec
4. **Document decisions** - Explain "why" in this README

**The contract is the source of truth.**

## Summary

AmpBox APIs embody ruthless simplicity:
- Clear resource naming
- Consistent patterns
- Standard error handling
- Minimal but complete
- RESTful where it helps
- Real-time where needed
- Documented as code (OpenAPI)

Every endpoint has a clear purpose. Every response follows a pattern. Every error is understandable.

**Good APIs are boring APIs - they work predictably, every time.**
