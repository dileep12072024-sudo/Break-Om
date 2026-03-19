# Hunyuan3D-2 Web API Documentation

## Base URL
```
http://localhost:8000
```

## Authentication

### JWT Token Authentication
Most endpoints require authentication. Include the token in the Authorization header:

```
Authorization: Bearer <your-jwt-token>
```

### Endpoints

#### Authentication

##### Register User
```http
POST /api/v1/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "username": "username",
  "password": "password123"
}
```

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "username",
  "is_active": true,
  "created_at": "2024-01-01T00:00:00Z"
}
```

##### Login
```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer"
}
```

##### Get Current User
```http
GET /api/v1/auth/me
Authorization: Bearer <token>
```

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "username",
  "is_active": true,
  "created_at": "2024-01-01T00:00:00Z"
}
```

#### 3D Model Generation

##### Generate from Text
```http
POST /api/v1/models/generate
Authorization: Bearer <token>
Content-Type: application/json

{
  "prompt": "a detailed dragon with metallic scales",
  "generate_texture": true,
  "format": "glb"
}
```

**Response:**
```json
{
  "success": true,
  "model_id": "model_123",
  "message": "Model generated successfully",
  "download_url": "/api/v1/models/model_123/download"
}
```

##### Generate from Image
```http
POST /api/v1/models/generate-from-image
Authorization: Bearer <token>
Content-Type: multipart/form-data

file: <image_file>
generate_texture: true
format: glb
```

**Response:**
```json
{
  "success": true,
  "model_id": "model_123",
  "message": "Model generated successfully from image",
  "download_url": "/api/v1/models/model_123/download"
}
```

##### Edit Model
```http
POST /api/v1/models/edit
Authorization: Bearer <token>
Content-Type: application/json

{
  "model_id": "model_123",
  "edit_prompt": "make the wings longer and add fire effects",
  "format": "glb"
}
```

**Response:**
```json
{
  "success": true,
  "model_id": "model_123",
  "message": "Model edited successfully",
  "download_url": "/api/v1/models/model_123/download"
}
```

#### Model Management

##### List Models
```http
GET /api/v1/models?page=1&page_size=10
Authorization: Bearer <token>
```

**Response:**
```json
{
  "models": [
    {
      "model_id": "model_123",
      "prompt": "a detailed dragon with metallic scales",
      "format": "glb",
      "file_size": 1048576,
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": null
    }
  ],
  "total": 10,
  "page": 1,
  "page_size": 10
}
```

##### Get Model Details
```http
GET /api/v1/models/{model_id}
Authorization: Bearer <token>
```

**Response:**
```json
{
  "model_id": "model_123",
  "prompt": "a detailed dragon with metallic scales",
  "format": "glb",
  "file_size": 1048576,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": null
}
```

##### Download Model
```http
GET /api/v1/models/{model_id}/download?format=glb
Authorization: Bearer <token>
```

**Response:** Binary file data

##### Delete Model
```http
DELETE /api/v1/models/{model_id}
Authorization: Bearer <token>
```

**Response:**
```json
{
  "message": "Model deleted successfully"
}
```

#### System

##### Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "Hunyuan3D-2 Web API",
  "version": "1.0.0"
}
```

##### API Root
```http
GET /
```

**Response:**
```json
{
  "message": "Hunyuan3D-2 Web API",
  "version": "1.0.0",
  "docs": "/docs",
  "health": "/health"
}
```

## Error Responses

All endpoints may return error responses in the following format:

```json
{
  "success": false,
  "error": "Error message",
  "details": "Additional error details"
}
```

### Common HTTP Status Codes

- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `422` - Validation Error
- `500` - Internal Server Error

## Rate Limiting

API endpoints are rate-limited to prevent abuse:

- **Generation endpoints**: 10 requests per hour
- **Download endpoints**: 100 requests per hour
- **Other endpoints**: 1000 requests per hour

Rate limit headers are included in responses:

```
X-RateLimit-Limit: 10
X-RateLimit-Remaining: 9
X-RateLimit-Reset: 1640995200
```

## File Upload Limits

- **Maximum file size**: 10MB
- **Supported formats**: JPEG, PNG, WebP
- **Content types**: `image/jpeg`, `image/png`, `image/webp`

## Model Formats

### Supported Export Formats

| Format | Description | Recommended Use |
|--------|-------------|-----------------|
| `glb` | GLB (Binary glTF) | Web, 3D viewers |
| `obj` | OBJ | 3D software |
| `fbx` | FBX | Unity, Unreal Engine |

### Model Generation Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `generate_texture` | boolean | true | Generate texture for the model |
| `format` | string | glb | Output format |

## WebSocket Support (Future)

Real-time updates for long-running generations:

```javascript
const ws = new WebSocket('ws://localhost:8000/ws/generation/{model_id}');

ws.onmessage = function(event) {
    const data = JSON.parse(event.data);
    console.log('Generation progress:', data.progress);
};
```

## SDK Examples

### Python

```python
import requests

# Login
response = requests.post('http://localhost:8000/api/v1/auth/login', json={
    'email': 'user@example.com',
    'password': 'password123'
})
token = response.json()['access_token']

headers = {'Authorization': f'Bearer {token}'}

# Generate model
response = requests.post(
    'http://localhost:8000/api/v1/models/generate',
    json={
        'prompt': 'a detailed dragon with metallic scales',
        'generate_texture': True,
        'format': 'glb'
    },
    headers=headers
)

model_id = response.json()['model_id']

# Download model
response = requests.get(
    f'http://localhost:8000/api/v1/models/{model_id}/download',
    headers=headers
)

with open(f'{model_id}.glb', 'wb') as f:
    f.write(response.content)
```

### JavaScript

```javascript
// Login
const loginResponse = await fetch('http://localhost:8000/api/v1/auth/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        email: 'user@example.com',
        password: 'password123'
    })
});
const { access_token } = await loginResponse.json();

// Generate model
const generateResponse = await fetch('http://localhost:8000/api/v1/models/generate', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${access_token}`
    },
    body: JSON.stringify({
        prompt: 'a detailed dragon with metallic scales',
        generate_texture: true,
        format: 'glb'
    })
});
const { model_id } = await generateResponse.json();

// Download model
const downloadResponse = await fetch(
    `http://localhost:8000/api/v1/models/${model_id}/download?format=glb`,
    { headers: { 'Authorization': `Bearer ${access_token}` } }
);
const blob = await downloadResponse.blob();
const url = URL.createObjectURL(blob);
const a = document.createElement('a');
a.href = url;
a.download = `${model_id}.glb`;
a.click();
```

## Testing

### Test with curl

```bash
# Health check
curl http://localhost:8000/health

# Generate model
curl -X POST "http://localhost:8000/api/v1/models/generate" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "prompt": "a detailed dragon with metallic scales",
    "generate_texture": true,
    "format": "glb"
  }'
```

### Interactive Documentation

Visit `http://localhost:8000/docs` for interactive API documentation with Swagger UI.
