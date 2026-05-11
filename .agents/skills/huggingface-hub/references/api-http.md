# HTTP API Reference

Complete curl/HTTP examples for interacting with Hugging Face APIs directly.

## Authentication

All authenticated requests require an HF token:

```bash
# Set your token
export HF_TOKEN="hf_your_token_here"

# Use in requests
curl -H "Authorization: Bearer $HF_TOKEN" ...
```

Get tokens at: https://huggingface.co/settings/tokens

## Inference Providers API

The Inference Providers API is OpenAI-compatible and routes to multiple providers.

**Base URL:** `https://router.huggingface.co/v1`

### Chat Completion

```bash
curl https://router.huggingface.co/v1/chat/completions \
  -H "Authorization: Bearer $HF_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "meta-llama/Llama-3.1-8B-Instruct",
    "messages": [
      {"role": "user", "content": "Hello!"}
    ],
    "stream": false
  }'
```

**Streaming:**

```bash
curl https://router.huggingface.co/v1/chat/completions \
  -H "Authorization: Bearer $HF_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "meta-llama/Llama-3.1-8B-Instruct",
    "messages": [{"role": "user", "content": "Tell me a story"}],
    "stream": true
  }'
```

### Provider Selection

Append suffix to model name:

```bash
# Fastest provider (highest throughput)
"model": "meta-llama/Llama-3.1-8B-Instruct:fastest"

# Cheapest provider (lowest cost per token)
"model": "meta-llama/Llama-3.1-8B-Instruct:cheapest"

# Specific provider
"model": "meta-llama/Llama-3.1-8B-Instruct:together"
"model": "meta-llama/Llama-3.1-8B-Instruct:sambanova"
```

### Vision Models (VLM)

```bash
curl https://router.huggingface.co/v1/chat/completions \
  -H "Authorization: Bearer $HF_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "meta-llama/Llama-3.2-11B-Vision-Instruct",
    "messages": [
      {
        "role": "user",
        "content": [
          {"type": "text", "text": "What is in this image?"},
          {"type": "image_url", "image_url": {"url": "https://example.com/image.jpg"}}
        ]
      }
    ]
  }'
```

### List Available Models

```bash
curl https://router.huggingface.co/v1/models \
  -H "Authorization: Bearer $HF_TOKEN"
```

## Hub API

**Base URL:** `https://huggingface.co/api`

### Models API

```bash
# List models
curl "https://huggingface.co/api/models?limit=10"

# Search models
curl "https://huggingface.co/api/models?search=llama"

# Filter by task
curl "https://huggingface.co/api/models?pipeline_tag=text-generation"

# Filter by inference provider
curl "https://huggingface.co/api/models?inference_provider=together"

# Get model info
curl "https://huggingface.co/api/models/meta-llama/Llama-3.1-8B-Instruct"

# Get model with inference status
curl "https://huggingface.co/api/models/meta-llama/Llama-3.1-8B-Instruct?expand[]=inference"

# Get model providers
curl "https://huggingface.co/api/models/meta-llama/Llama-3.1-8B-Instruct?expand[]=inferenceProviderMapping"
```

### Datasets API

```bash
# List datasets
curl "https://huggingface.co/api/datasets?limit=10"

# Search datasets
curl "https://huggingface.co/api/datasets?search=imdb"

# Get dataset info
curl "https://huggingface.co/api/datasets/stanfordnlp/imdb"
```

### Spaces API

```bash
# List Spaces
curl "https://huggingface.co/api/spaces?limit=10"

# Get Space info
curl "https://huggingface.co/api/spaces/gradio/text-generation"
```

## File Operations

### Download Files

```bash
# Download single file (public repo)
curl -L "https://huggingface.co/bert-base-uncased/resolve/main/config.json" \
  -o config.json

# Download file from private/gated repo
curl -L "https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct/resolve/main/config.json" \
  -H "Authorization: Bearer $HF_TOKEN" \
  -o config.json

# Download specific revision
curl -L "https://huggingface.co/bert-base-uncased/resolve/v1.0/config.json" \
  -o config.json
```

### Upload Files

```bash
# Upload single file
curl -X POST "https://huggingface.co/api/models/username/my-model/upload/main/model.safetensors" \
  -H "Authorization: Bearer $HF_TOKEN" \
  -H "Content-Type: application/octet-stream" \
  --data-binary @model.safetensors
```

### Create Repository

```bash
# Create model repo
curl -X POST "https://huggingface.co/api/repos/create" \
  -H "Authorization: Bearer $HF_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "model",
    "name": "my-new-model",
    "private": false
  }'

# Create dataset repo
curl -X POST "https://huggingface.co/api/repos/create" \
  -H "Authorization: Bearer $HF_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "dataset",
    "name": "my-new-dataset"
  }'

# Create Space
curl -X POST "https://huggingface.co/api/repos/create" \
  -H "Authorization: Bearer $HF_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "space",
    "name": "my-new-space",
    "sdk": "gradio"
  }'
```

### Delete Repository

```bash
curl -X DELETE "https://huggingface.co/api/repos/delete" \
  -H "Authorization: Bearer $HF_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "model",
    "name": "username/my-model"
  }'
```

## Gated Model Access

### List Access Requests

```bash
# Pending requests
curl "https://huggingface.co/api/models/username/gated-model/user-access-request/pending" \
  -H "Authorization: Bearer $HF_TOKEN"

# Accepted requests
curl "https://huggingface.co/api/models/username/gated-model/user-access-request/accepted" \
  -H "Authorization: Bearer $HF_TOKEN"
```

### Manage Access

```bash
# Accept user
curl -X POST "https://huggingface.co/api/models/username/gated-model/user-access-request/handle" \
  -H "Authorization: Bearer $HF_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"status": "accepted", "user": "requesting-user"}'

# Reject user
curl -X POST "https://huggingface.co/api/models/username/gated-model/user-access-request/handle" \
  -H "Authorization: Bearer $HF_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"status": "rejected", "user": "requesting-user"}'

# Grant access directly
curl -X POST "https://huggingface.co/api/models/username/gated-model/user-access-request/grant" \
  -H "Authorization: Bearer $HF_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"user": "some-user"}'
```

## Webhooks

### Test Webhook Endpoint

```bash
# Simulate webhook payload
curl -X POST "https://your-webhook-url.com/webhook" \
  -H "Content-Type: application/json" \
  -H "X-Webhook-Secret: your-secret" \
  -d '{
    "event": {"action": "update", "scope": "repo.content"},
    "repo": {
      "type": "model",
      "name": "user/model",
      "private": false
    }
  }'
```

## Rate Limits

All API calls are subject to rate limits. If you exceed limits, you'll receive a 429 status code.

Headers returned with each request:
- `X-RateLimit-Limit`: Total requests allowed
- `X-RateLimit-Remaining`: Requests remaining
- `X-RateLimit-Reset`: Time when limit resets

## Error Handling

Common HTTP status codes:

| Code | Meaning |
|------|---------|
| 200 | Success |
| 400 | Bad request (invalid parameters) |
| 401 | Unauthorized (missing/invalid token) |
| 403 | Forbidden (no access to resource) |
| 404 | Not found |
| 429 | Rate limited |
| 500 | Server error |

## OpenAPI Specification

Full API documentation: https://huggingface.co/spaces/huggingface/openapi

OpenAPI spec: https://huggingface.co/.well-known/openapi.json
