# AmpBox API Quick Reference

Fast lookup for common API patterns and endpoints.

## Base URL

```
Local:  http://localhost:8000/api/v1
Cloud:  https://ampbox.example.com/api/v1
```

## Authentication

### Bearer Token (User Sessions)
```bash
curl -H "Authorization: Bearer eyJhbGc..." https://api/v1/resource
```

### API Key (Programmatic)
```bash
curl -H "X-API-Key: amp_live_abc123..." https://api/v1/resource
```

## Agent Runtime

### Create Session
```bash
POST /agent/sessions
{
  "agent_id": "code-analyzer",
  "workspace_id": "ws-123"
}
→ {"session_id": "sess-abc", "status": "pending"}
```

### Execute Task
```bash
POST /agent/sessions/{session_id}/tasks
{
  "task": "Analyze error patterns in logs"
}
→ {"task_id": "task-xyz", "status": "pending"}
```

### Stream Output (SSE)
```bash
GET /agent/sessions/{session_id}/stream
→ event: output
  data: {"text": "Processing..."}
  
  event: task_completed
  data: {"task_id": "task-xyz", "result": {...}}
```

### Terminate Session
```bash
DELETE /agent/sessions/{session_id}
→ 204 No Content
```

### List Sessions
```bash
GET /agent/sessions?status=running&limit=20
→ {"sessions": [...], "total": 5}
```

## Virtual Filesystem

### Read File
```bash
GET /vfs/files?path=/workspace/src/main.py
→ (file content)
```

### Write File
```bash
POST /vfs/files
{
  "path": "/workspace/config.yaml",
  "content": "database:\n  host: localhost"
}
→ {"path": "/workspace/config.yaml", "type": "file", "size": 42}
```

### List Directory
```bash
GET /vfs/directories?path=/workspace&recursive=false
→ {"path": "/workspace", "entries": [...]}
```

### Mount Layer
```bash
POST /vfs/layers
{
  "layer_id": "base-ubuntu",
  "mount_point": "/",
  "priority": 0
}
→ {"layer_id": "base-ubuntu", "mount_point": "/", "priority": 0}
```

### Resolve File (Debug)
```bash
GET /vfs/files/resolve?path=/workspace/config.yaml
→ {
    "path": "/workspace/config.yaml",
    "layer": "user-workspace",
    "layers_checked": ["user-workspace", "base-ubuntu"]
  }
```

### Watch Changes (SSE)
```bash
GET /vfs/watch?path=/workspace&recursive=true
→ event: file_modified
  data: {"path": "/workspace/src/main.py", "layer": "user-workspace"}
```

## Auth

### Login
```bash
POST /auth/login
{
  "username": "user@example.com",
  "password": "secret"
}
→ {
    "access_token": "eyJhbGc...",
    "refresh_token": "refresh_xyz",
    "token_type": "bearer",
    "expires_in": 3600
  }
```

### Refresh Token
```bash
POST /auth/refresh
{
  "refresh_token": "refresh_xyz"
}
→ {"access_token": "eyJhbGc...", "expires_in": 3600}
```

### Create API Key
```bash
POST /auth/keys
{
  "name": "CI Pipeline Key",
  "expires_at": "2025-12-31T23:59:59Z"
}
→ {
    "key_id": "key-123",
    "name": "CI Pipeline Key",
    "key": "amp_live_abc123..."  # Only shown once!
  }
```

### List API Keys
```bash
GET /auth/keys
→ {"keys": [{"key_id": "key-123", "name": "CI Pipeline Key", ...}]}
```

### Revoke API Key
```bash
DELETE /auth/keys/{key_id}
→ 204 No Content
```

## Storage

### Upload File
```bash
POST /storage/files
Content-Type: multipart/form-data

file=@/path/to/local/file.pdf
path=/documents/report.pdf
→ {"file_id": "file-123", "path": "/documents/report.pdf", "size": 1024}
```

### Download File
```bash
GET /storage/files/{file_id}
→ (file content)
```

### Get Metadata
```bash
GET /storage/files/{file_id}/metadata
→ {
    "file_id": "file-123",
    "path": "/documents/report.pdf",
    "size": 1024,
    "content_type": "application/pdf",
    "uploaded_at": "2024-01-15T10:30:00Z"
  }
```

### List Files
```bash
GET /storage/files?path=/documents&limit=20
→ {"files": [...], "total": 5}
```

## Workspaces

### Create Workspace
```bash
POST /workspaces
{
  "name": "Project Amplifier",
  "description": "Main development workspace"
}
→ {"workspace_id": "ws-123", "name": "Project Amplifier", ...}
```

### List Workspaces
```bash
GET /workspaces?limit=20
→ {"workspaces": [...], "total": 3}
```

### Get Workspace
```bash
GET /workspaces/{workspace_id}
→ {"workspace_id": "ws-123", "name": "Project Amplifier", ...}
```

### Share Workspace
```bash
POST /workspaces/{workspace_id}/share
{
  "user_id": "user-456",
  "permissions": ["read", "write"]
}
→ 200 OK
```

### Delete Workspace
```bash
DELETE /workspaces/{workspace_id}
→ 204 No Content
```

## Agent Management

### Create Agent Config
```bash
POST /agents
{
  "name": "Code Analyzer",
  "model": "claude-3-5-sonnet-20241022",
  "system_prompt": "You are a code analysis expert...",
  "tools": ["read_file", "search_code"]
}
→ {"agent_id": "agent-123", "name": "Code Analyzer", ...}
```

### List Agent Configs
```bash
GET /agents?limit=20
→ {"agents": [...], "total": 5}
```

### Get Agent Config
```bash
GET /agents/{agent_id}
→ {"agent_id": "agent-123", "name": "Code Analyzer", ...}
```

### Update Agent Config
```bash
PUT /agents/{agent_id}
{
  "name": "Code Analyzer v2",
  "model": "claude-3-5-sonnet-20241022"
}
→ {"agent_id": "agent-123", "name": "Code Analyzer v2", ...}
```

### Delete Agent Config
```bash
DELETE /agents/{agent_id}
→ 204 No Content
```

## System & Admin

### System Status (Public)
```bash
GET /system/status
→ {
    "status": "healthy",
    "version": "1.0.0",
    "uptime": 86400,
    "services": {
      "agent_runtime": {"status": "up"},
      "vfs": {"status": "up"}
    }
  }
```

### List Users (Admin)
```bash
GET /admin/users?limit=20
→ {"users": [...], "total": 10}
```

### View Logs (Admin)
```bash
GET /admin/logs?level=error&since=2024-01-15T00:00:00Z&limit=100
→ {"logs": [...]}
```

### Get Metrics (Admin)
```bash
GET /admin/metrics
→ {
    "cpu_usage": 45.2,
    "memory_usage": 68.5,
    "active_sessions": 12,
    "requests_per_minute": 150
  }
```

## Error Responses

All errors follow this format:

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable description",
    "details": {}
  }
}
```

### Common Error Codes

| Code | Status | Meaning |
|------|--------|---------|
| `INVALID_REQUEST` | 400 | Malformed or invalid request |
| `UNAUTHORIZED` | 401 | Missing or invalid authentication |
| `FORBIDDEN` | 403 | Authenticated but insufficient permissions |
| `NOT_FOUND` | 404 | Resource doesn't exist |
| `CONFLICT` | 409 | Resource already exists |
| `VALIDATION_ERROR` | 422 | Request doesn't meet validation rules |
| `INTERNAL_ERROR` | 500 | Server error |

## Pagination

All list endpoints support pagination:

```bash
GET /resource?limit=20&offset=0
→ {
    "items": [...],
    "total": 150,
    "limit": 20,
    "offset": 0
  }
```

**Parameters:**
- `limit` - Max items per page (default: 20, max: 100)
- `offset` - Skip first N items (default: 0)

**Navigation:**
```
Page 1: ?limit=20&offset=0   (items 0-19)
Page 2: ?limit=20&offset=20  (items 20-39)
Page 3: ?limit=20&offset=40  (items 40-59)
```

## Filtering & Sorting

### Common Filters

```bash
# Filter by status
GET /agent/sessions?status=running

# Filter by date range
GET /admin/logs?since=2024-01-01T00:00:00Z&until=2024-01-31T23:59:59Z

# Filter by user
GET /workspaces?owner_id=user-123

# Multiple filters
GET /storage/files?path=/documents&content_type=application/pdf
```

### Sorting (Future)
```bash
# Sort by created date (descending)
GET /resource?sort=-created_at

# Sort by name (ascending)
GET /resource?sort=name
```

## Rate Limiting

Headers in response:
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1642262400
```

When rate limited:
```
HTTP 429 Too Many Requests
Retry-After: 60

{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Rate limit exceeded. Try again in 60 seconds."
  }
}
```

## SSE Connection Example

JavaScript:
```javascript
const eventSource = new EventSource(
  'https://api/v1/agent/sessions/sess-abc/stream',
  { headers: { 'Authorization': `Bearer ${token}` }}
);

eventSource.addEventListener('output', (e) => {
  const data = JSON.parse(e.data);
  console.log(data.text);
});

eventSource.addEventListener('task_completed', (e) => {
  eventSource.close();
});

eventSource.onerror = (e) => {
  console.error('SSE error:', e);
};
```

Python:
```python
import sseclient
import requests

response = requests.get(
    'https://api/v1/agent/sessions/sess-abc/stream',
    headers={'Authorization': f'Bearer {token}'},
    stream=True
)

client = sseclient.SSEClient(response)
for event in client.events():
    if event.event == 'output':
        data = json.loads(event.data)
        print(data['text'])
    elif event.event == 'task_completed':
        break
```

## Common Workflows

### Run Agent Task

```bash
# 1. Create session
SESSION=$(curl -X POST https://api/v1/agent/sessions \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"agent_id":"code-analyzer"}' | jq -r .session_id)

# 2. Execute task
TASK=$(curl -X POST https://api/v1/agent/sessions/$SESSION/tasks \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"task":"Analyze codebase"}' | jq -r .task_id)

# 3. Stream output
curl -N https://api/v1/agent/sessions/$SESSION/stream \
  -H "Authorization: Bearer $TOKEN"

# 4. Clean up
curl -X DELETE https://api/v1/agent/sessions/$SESSION \
  -H "Authorization: Bearer $TOKEN"
```

### Setup Workspace with VFS

```bash
# 1. Create workspace
WS=$(curl -X POST https://api/v1/workspaces \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"name":"My Project"}' | jq -r .workspace_id)

# 2. Mount base layer
curl -X POST https://api/v1/vfs/layers \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"layer_id":"base-ubuntu","mount_point":"/","priority":0}'

# 3. Mount workspace layer
curl -X POST https://api/v1/vfs/layers \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"layer_id":"'$WS'","mount_point":"/workspace","priority":100}'

# 4. Write config file
curl -X POST https://api/v1/vfs/files \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"path":"/workspace/config.yaml","content":"app:\n  name: MyApp"}'
```

## SDK Generation

Generate client SDK from OpenAPI spec:

```bash
# Python
openapi-python-client generate --path ampbox-api-contracts.yaml

# TypeScript
npx openapi-typescript ampbox-api-contracts.yaml --output ampbox-api.ts

# Go
oapi-codegen -generate types,client ampbox-api-contracts.yaml > ampbox_client.go

# Java
openapi-generator-cli generate -i ampbox-api-contracts.yaml -g java
```

## Testing

```bash
# Health check
curl https://api/v1/system/status

# Test auth
curl -X POST https://api/v1/auth/login \
  -d '{"username":"test","password":"test"}'

# Verify token
curl https://api/v1/auth/verify \
  -H "Authorization: Bearer $TOKEN"
```

## Support

- Full API Spec: `ampbox-api-contracts.yaml`
- Documentation: `README.md`
- Issues: https://github.com/your-org/ampbox/issues
