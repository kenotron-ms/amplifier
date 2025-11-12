# AmpBox API Design Patterns

**Reusable patterns for consistent, maintainable API design**

## Pattern Catalog

### 1. Resource-Based URLs

**Pattern:** Use nouns for resources, HTTP methods for actions

```
✅ Good:
POST   /agents              (create)
GET    /agents/{id}         (read)
PUT    /agents/{id}         (update)
DELETE /agents/{id}         (delete)
GET    /agents              (list)

❌ Bad:
POST   /createAgent
GET    /getAgent?id=123
POST   /updateAgent
POST   /deleteAgent
GET    /listAgents
```

**When to break:** Complex operations that don't map to CRUD

```
✅ Acceptable:
POST   /agents/{id}/deploy        (action beyond CRUD)
POST   /workspaces/{id}/share     (operation with complex semantics)
POST   /auth/refresh              (not a resource operation)
```

---

### 2. Query Parameters vs Path Parameters

**Pattern:** 
- Path params = resource identity
- Query params = filtering, pagination, options

```
✅ Good:
GET /workspaces/{workspace_id}/files?path=/src&limit=20

❌ Bad:
GET /workspaces/{workspace_id}/files/{path}?limit=20
# Path params should be identifiers, not filtering criteria
```

**Exception:** When the secondary resource IS an identifier

```
✅ Acceptable:
GET /users/{user_id}/workspaces/{workspace_id}
# Both are resource identifiers
```

---

### 3. Pagination Pattern

**Pattern:** Use `limit` and `offset`, return totals

```python
@app.get("/resources")
async def list_resources(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    items = get_items(limit=limit, offset=offset)
    total = count_items()
    
    return {
        "items": items,
        "total": total,
        "limit": limit,
        "offset": offset
    }
```

**Client usage:**
```javascript
// Page through results
let offset = 0;
const limit = 20;

while (offset < total) {
  const response = await fetch(`/resources?limit=${limit}&offset=${offset}`);
  const data = await response.json();
  
  processItems(data.items);
  offset += limit;
}
```

**Alternative: Cursor-based** (for high-volume, real-time data)
```
GET /resources?cursor=eyJpZCI6MTIzfQ==&limit=20
→ {"items": [...], "next_cursor": "eyJpZCI6MTQzfQ=="}
```

---

### 4. Filtering Pattern

**Pattern:** Use query parameters for filters

```
GET /agent/sessions?status=running&agent_id=code-analyzer&limit=20
```

**Implementation:**
```python
@app.get("/agent/sessions")
async def list_sessions(
    status: Optional[str] = None,
    agent_id: Optional[str] = None,
    limit: int = 20
):
    filters = {}
    if status:
        filters['status'] = status
    if agent_id:
        filters['agent_id'] = agent_id
    
    return get_sessions(filters=filters, limit=limit)
```

**Complex filters** (future consideration):
```
GET /resources?filter[status]=active&filter[created_at][gt]=2024-01-01
```

---

### 5. Sorting Pattern

**Pattern:** Use `sort` parameter with `-` prefix for descending

```
GET /resources?sort=name           # Ascending
GET /resources?sort=-created_at    # Descending
GET /resources?sort=name,-priority # Multiple fields
```

**Implementation:**
```python
@app.get("/resources")
async def list_resources(sort: str = "created_at"):
    order_by = []
    for field in sort.split(','):
        if field.startswith('-'):
            order_by.append((field[1:], 'DESC'))
        else:
            order_by.append((field, 'ASC'))
    
    return get_resources(order_by=order_by)
```

---

### 6. Nested Resources Pattern

**Pattern:** Max 2 levels deep, use query params beyond that

```
✅ Good:
GET /workspaces/{workspace_id}/files?path=/src
POST /workspaces/{workspace_id}/share

❌ Too nested:
GET /workspaces/{workspace_id}/layers/{layer_id}/files/{file_id}/versions/{version_id}
# Use: GET /files/{file_id}/versions/{version_id}?workspace_id=X&layer_id=Y
```

**When nesting makes sense:**
- Parent-child relationship is strong
- Child resources don't exist independently
- Operation is specifically about the relationship

---

### 7. Error Response Pattern

**Pattern:** Consistent error structure with machine-readable codes

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid request parameters",
    "details": {
      "field": "agent_id",
      "reason": "Agent ID is required"
    }
  }
}
```

**Implementation:**
```python
class APIError(Exception):
    def __init__(self, code: str, message: str, status_code: int = 400, details: dict = None):
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details or {}

# Common errors
NOT_FOUND = lambda resource, id: APIError(
    code=f"{resource.upper()}_NOT_FOUND",
    message=f"{resource} {id} not found",
    status_code=404
)

VALIDATION_ERROR = lambda field, reason: APIError(
    code="VALIDATION_ERROR",
    message=f"Invalid {field}: {reason}",
    status_code=422,
    details={"field": field, "reason": reason}
)
```

---

### 8. Async Operation Pattern

**Pattern:** Return 202 Accepted with task ID, poll for status

```bash
# 1. Initiate async operation
POST /agent/sessions/{id}/tasks
→ 202 Accepted
  {"task_id": "task-123", "status": "pending"}

# 2. Poll for completion
GET /agent/sessions/{id}/tasks/task-123
→ 200 OK
  {"task_id": "task-123", "status": "running"}

# 3. Eventually completes
GET /agent/sessions/{id}/tasks/task-123
→ 200 OK
  {"task_id": "task-123", "status": "completed", "result": {...}}
```

**Alternative: SSE for real-time updates** (preferred for AmpBox)
```bash
POST /agent/sessions/{id}/tasks
→ 202 Accepted
  {"task_id": "task-123", "stream_url": "/agent/sessions/{id}/stream"}

# Stream events
GET /agent/sessions/{id}/stream
→ event: task_started
  event: output
  event: task_completed
```

---

### 9. Batch Operations Pattern

**Pattern:** Accept array of items, return array of results

```bash
POST /resources/batch
{
  "operations": [
    {"action": "create", "data": {...}},
    {"action": "update", "id": "123", "data": {...}},
    {"action": "delete", "id": "456"}
  ]
}
→ {
    "results": [
      {"status": "success", "id": "789"},
      {"status": "success", "id": "123"},
      {"status": "error", "code": "NOT_FOUND", "message": "..."}
    ]
  }
```

**Partial success handling:**
```python
@app.post("/resources/batch")
async def batch_operations(operations: List[Operation]):
    results = []
    for op in operations:
        try:
            result = await process_operation(op)
            results.append({"status": "success", "result": result})
        except Exception as e:
            results.append({
                "status": "error",
                "code": e.code,
                "message": str(e)
            })
    
    # Return 200 even if some failed (partial success)
    return {"results": results}
```

---

### 10. Versioning Pattern

**Pattern:** Version in URL path, maintain compatibility within version

```
/api/v1/resources
/api/v2/resources
```

**When to version:**
- Breaking changes to request/response schemas
- Removing endpoints
- Changing authentication mechanism

**How to maintain compatibility:**
```python
# Add optional fields (backward compatible)
class ResourceV1(BaseModel):
    name: str
    description: Optional[str] = None  # New optional field

# Deprecation header
@app.get("/api/v1/old-endpoint")
async def old_endpoint():
    headers = {
        "Deprecation": "true",
        "Sunset": "Sat, 31 Dec 2025 23:59:59 GMT",
        "Link": '<https://api/v2/new-endpoint>; rel="successor-version"'
    }
    return Response(content=data, headers=headers)
```

---

### 11. Idempotency Pattern

**Pattern:** Use idempotency keys for POST/PUT to prevent duplicates

```bash
POST /resources
Idempotency-Key: unique-client-key-123
{...}
→ 201 Created

# Retry with same key
POST /resources
Idempotency-Key: unique-client-key-123
{...}
→ 200 OK (returns same result, no duplicate created)
```

**Implementation:**
```python
@app.post("/resources")
async def create_resource(
    data: ResourceCreate,
    idempotency_key: str = Header(None)
):
    if idempotency_key:
        # Check if already processed
        cached = get_cached_result(idempotency_key)
        if cached:
            return cached
    
    # Process request
    result = create_new_resource(data)
    
    if idempotency_key:
        # Cache result for 24 hours
        cache_result(idempotency_key, result, ttl=86400)
    
    return result
```

---

### 12. Conditional Requests Pattern

**Pattern:** Use ETags for caching and optimistic locking

```bash
# Get resource with ETag
GET /resources/123
→ 200 OK
  ETag: "abc123"
  {...}

# Conditional GET (only if changed)
GET /resources/123
If-None-Match: "abc123"
→ 304 Not Modified (content not returned)

# Conditional update (prevent conflicts)
PUT /resources/123
If-Match: "abc123"
{...}
→ 412 Precondition Failed (if ETag doesn't match)
```

**Implementation:**
```python
@app.get("/resources/{id}")
async def get_resource(id: str, if_none_match: str = Header(None)):
    resource = get_resource_by_id(id)
    etag = generate_etag(resource)
    
    if if_none_match == etag:
        return Response(status_code=304)
    
    return Response(
        content=resource.json(),
        headers={"ETag": etag}
    )

@app.put("/resources/{id}")
async def update_resource(
    id: str,
    data: ResourceUpdate,
    if_match: str = Header(None)
):
    resource = get_resource_by_id(id)
    current_etag = generate_etag(resource)
    
    if if_match and if_match != current_etag:
        raise APIError(
            code="PRECONDITION_FAILED",
            message="Resource has been modified",
            status_code=412
        )
    
    updated = update_resource_data(id, data)
    return Response(
        content=updated.json(),
        headers={"ETag": generate_etag(updated)}
    )
```

---

### 13. Rate Limiting Pattern

**Pattern:** Return rate limit info in headers

```bash
GET /resources
→ 200 OK
  X-RateLimit-Limit: 1000
  X-RateLimit-Remaining: 999
  X-RateLimit-Reset: 1642262400

# When limited
GET /resources
→ 429 Too Many Requests
  Retry-After: 60
  X-RateLimit-Limit: 1000
  X-RateLimit-Remaining: 0
  X-RateLimit-Reset: 1642262400
```

**Implementation:**
```python
from time import time

class RateLimiter:
    def __init__(self, limit: int, window: int):
        self.limit = limit
        self.window = window
        self.requests = {}
    
    def check_limit(self, key: str) -> tuple[bool, dict]:
        now = int(time())
        window_start = now - self.window
        
        # Clean old requests
        self.requests[key] = [t for t in self.requests.get(key, []) if t > window_start]
        
        count = len(self.requests[key])
        remaining = max(0, self.limit - count)
        reset = window_start + self.window
        
        if count >= self.limit:
            return False, {"limit": self.limit, "remaining": 0, "reset": reset}
        
        self.requests[key].append(now)
        return True, {"limit": self.limit, "remaining": remaining - 1, "reset": reset}

# Middleware
@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    key = get_user_id(request) or request.client.host
    allowed, info = rate_limiter.check_limit(key)
    
    if not allowed:
        return JSONResponse(
            status_code=429,
            content={"error": {"code": "RATE_LIMIT_EXCEEDED", "message": "..."}},
            headers={
                "X-RateLimit-Limit": str(info["limit"]),
                "X-RateLimit-Remaining": "0",
                "X-RateLimit-Reset": str(info["reset"]),
                "Retry-After": str(info["reset"] - int(time()))
            }
        )
    
    response = await call_next(request)
    response.headers.update({
        "X-RateLimit-Limit": str(info["limit"]),
        "X-RateLimit-Remaining": str(info["remaining"]),
        "X-RateLimit-Reset": str(info["reset"])
    })
    return response
```

---

### 14. Webhook Pattern

**Pattern:** Allow clients to register URLs for event notifications

```bash
# Register webhook
POST /webhooks
{
  "url": "https://client.example.com/webhooks/ampbox",
  "events": ["session.completed", "task.failed"],
  "secret": "webhook_secret_xyz"
}
→ {"webhook_id": "wh-123", ...}

# Webhook payload
POST https://client.example.com/webhooks/ampbox
X-Webhook-Signature: sha256=abc123...
{
  "event": "session.completed",
  "timestamp": "2024-01-15T10:30:00Z",
  "data": {
    "session_id": "sess-abc",
    "result": {...}
  }
}
```

**Security:**
```python
import hmac
import hashlib

def sign_webhook(payload: str, secret: str) -> str:
    signature = hmac.new(
        secret.encode(),
        payload.encode(),
        hashlib.sha256
    ).hexdigest()
    return f"sha256={signature}"

def verify_webhook(payload: str, signature: str, secret: str) -> bool:
    expected = sign_webhook(payload, secret)
    return hmac.compare_digest(signature, expected)
```

---

### 15. Health Check Pattern

**Pattern:** Multiple levels of health endpoints

```bash
# Liveness (is service running?)
GET /health
→ 200 OK
  {"status": "ok"}

# Readiness (can service handle traffic?)
GET /health/ready
→ 200 OK (ready) or 503 Service Unavailable (not ready)
  {"status": "ready", "checks": {"db": "ok", "cache": "ok"}}

# Detailed status (authenticated)
GET /system/status
→ 200 OK
  {
    "status": "healthy",
    "version": "1.0.0",
    "uptime": 86400,
    "services": {
      "database": {"status": "up", "latency_ms": 5},
      "cache": {"status": "up", "hit_rate": 0.85},
      "queue": {"status": "degraded", "message": "High backlog"}
    }
  }
```

**Implementation:**
```python
@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/health/ready")
async def ready():
    checks = {}
    all_ok = True
    
    # Check dependencies
    checks["db"] = await check_database()
    checks["cache"] = await check_cache()
    
    all_ok = all(c == "ok" for c in checks.values())
    
    status_code = 200 if all_ok else 503
    return JSONResponse(
        status_code=status_code,
        content={"status": "ready" if all_ok else "not_ready", "checks": checks}
    )
```

---

## Anti-Patterns to Avoid

### ❌ Mixing Verbs and Nouns in URLs

```
Bad:  GET /getUser?id=123
Good: GET /users/123

Bad:  POST /createSession
Good: POST /sessions
```

### ❌ Using POST for Everything

```
Bad:  POST /getResources
Bad:  POST /deleteResource
Good: GET /resources
Good: DELETE /resources/{id}
```

### ❌ Inconsistent Response Formats

```
Bad:
  POST /resources → {"data": {...}}
  GET /resources → [{...}, {...}]

Good:
  POST /resources → {...}
  GET /resources → {"items": [...], "total": 10}
```

### ❌ Exposing Internal Details

```
Bad:  {"db_table": "users", "sql_query": "SELECT..."}
Good: {"user_id": "123", "username": "alice"}
```

### ❌ No Error Context

```
Bad:  {"error": "Invalid input"}
Good: {
        "error": {
          "code": "VALIDATION_ERROR",
          "message": "Invalid agent_id: must be non-empty string",
          "details": {"field": "agent_id"}
        }
      }
```

---

## Testing Patterns

### Contract Tests

```python
def test_agent_session_contract():
    # Test happy path
    response = client.post('/api/v1/agent/sessions', json={
        'agent_id': 'test-agent'
    })
    assert response.status_code == 201
    assert 'session_id' in response.json()
    assert response.json()['status'] == 'pending'
    
    # Test validation
    response = client.post('/api/v1/agent/sessions', json={})
    assert response.status_code == 400
    assert response.json()['error']['code'] == 'VALIDATION_ERROR'
    
    # Test auth
    response = client.post('/api/v1/agent/sessions',
                          json={'agent_id': 'test'},
                          headers={})  # No auth
    assert response.status_code == 401
```

### Integration Tests

```python
@pytest.mark.integration
async def test_agent_workflow():
    # Create session
    session = await create_session(agent_id='test-agent')
    
    # Execute task
    task = await execute_task(session.id, task='test')
    
    # Wait for completion
    result = await wait_for_completion(session.id, task.id)
    
    assert result.status == 'completed'
    assert 'output' in result
```

---

## Summary

Good API design is:
- **Consistent** - Same patterns everywhere
- **Predictable** - Follows REST/HTTP conventions
- **Simple** - Minimal but complete
- **Documented** - Self-explanatory with examples
- **Testable** - Easy to verify behavior

Use these patterns as starting points, not rigid rules. Break them when you have good reason, but document why.
