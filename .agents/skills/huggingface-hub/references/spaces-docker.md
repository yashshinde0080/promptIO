# Docker Spaces Reference

Complete guide for building Docker-based Spaces on Hugging Face Hub.

## Quick Start

### Minimal Structure

```
my-docker-space/
├── README.md
├── Dockerfile
└── app.py (or your application files)
```

### README.md

```yaml
---
title: My Docker Space
emoji: 🐳
colorFrom: purple
colorTo: gray
sdk: docker
app_port: 7860
---

# My Docker Space

Description of your Space...
```

### Basic Dockerfile

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 7860

# Run application
CMD ["python", "app.py"]
```

## User Permissions

Docker containers run as user ID 1000. Set up proper permissions:

```dockerfile
FROM python:3.10-slim

# Create non-root user
RUN useradd -m -u 1000 user

# Switch to user
USER user

# Set environment
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

# Set working directory
WORKDIR $HOME/app

# Install Python dependencies as user
COPY --chown=user requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files with correct ownership
COPY --chown=user . .

CMD ["python", "app.py"]
```

> **Important**: Always use `--chown=user` with COPY and ADD commands.

## Secrets Management

### Build-time Secrets

Secrets are mounted, not injected as environment variables during build:

```dockerfile
# Mount and read secret during build
RUN --mount=type=secret,id=MY_SECRET,mode=0444,required=true \
    cat /run/secrets/MY_SECRET > /app/secret.txt

# Use secret in git clone
RUN --mount=type=secret,id=GIT_TOKEN,mode=0444,required=true \
    git clone https://$(cat /run/secrets/GIT_TOKEN)@github.com/user/repo.git

# Use secret for authenticated download
RUN --mount=type=secret,id=HF_TOKEN,mode=0444,required=true \
    curl -H "Authorization: Bearer $(cat /run/secrets/HF_TOKEN)" \
    https://huggingface.co/api/models/private/model
```

### Runtime Secrets

At runtime, secrets are available as environment variables:

```python
import os

# Access secrets at runtime
hf_token = os.environ.get("HF_TOKEN")
api_key = os.environ.get("MY_API_KEY")
```

### Setting Secrets

Configure secrets in Space Settings on the Hub.

**Who can manage secrets:**
- **Space owner**: Full access to create, view, update, delete secrets
- **Organization admins**: Full access to all Spaces in the organization
- **Organization members with write access**: Can add/update secrets for Spaces they have write access to
- **Viewers/public**: Cannot see or modify secrets

**How to add secrets:**
1. Go to your Space on huggingface.co
2. Click **Settings** tab
3. Scroll to **Repository secrets** section
4. Click **New secret**
5. Enter name (e.g., `MY_API_KEY`) and value
6. Click **Add**

> **Note**: Secret values are encrypted and never displayed after saving. You can only update or delete them.

## Variables

### Build-time Variables

Variables are passed as `build-arg`:

```dockerfile
# Declare build argument
ARG MODEL_NAME=default-model

# Use in Dockerfile
RUN echo "Building for model: $MODEL_NAME"
```

### Runtime Variables

Available as environment variables:

```python
import os
model_name = os.environ.get("MODEL_NAME", "default")
```

## Common Dockerfile Patterns

### FastAPI Application

```dockerfile
FROM python:3.10-slim

RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user PATH=/home/user/.local/bin:$PATH
WORKDIR $HOME/app

COPY --chown=user requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=user . .

EXPOSE 7860

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
```

### Flask Application

```dockerfile
FROM python:3.10-slim

RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user PATH=/home/user/.local/bin:$PATH
WORKDIR $HOME/app

COPY --chown=user requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=user . .

EXPOSE 7860

CMD ["gunicorn", "-b", "0.0.0.0:7860", "app:app"]
```

### Node.js Application

```dockerfile
FROM node:18-slim

RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user
WORKDIR $HOME/app

COPY --chown=user package*.json ./
RUN npm install

COPY --chown=user . .

EXPOSE 7860

CMD ["node", "server.js"]
```

### Multi-stage Build

```dockerfile
# Build stage
FROM python:3.10-slim AS builder

WORKDIR /build
COPY requirements.txt .
RUN pip install --no-cache-dir --target=/build/deps -r requirements.txt

# Runtime stage
FROM python:3.10-slim

RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user PATH=/home/user/.local/bin:$PATH
WORKDIR $HOME/app

# Copy dependencies from builder
COPY --from=builder --chown=user /build/deps /home/user/.local/lib/python3.10/site-packages

COPY --chown=user . .

CMD ["python", "app.py"]
```

### GPU-enabled Container

```dockerfile
FROM nvidia/cuda:12.1.0-runtime-ubuntu22.04

# Install Python
RUN apt-get update && apt-get install -y python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user PATH=/home/user/.local/bin:$PATH
WORKDIR $HOME/app

COPY --chown=user requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=user . .

CMD ["python3", "app.py"]
```

> **Note**: GPU is not available during build. Don't run GPU commands in Dockerfile.

## Data Persistence

### Persistent Storage

Data in `/data` persists across restarts (requires persistent storage upgrade):

```dockerfile
# Create data directory
RUN mkdir -p /data && chmod 777 /data
```

```python
import os

DATA_DIR = "/data"
os.makedirs(DATA_DIR, exist_ok=True)

# Save persistent data
with open(f"{DATA_DIR}/state.json", "w") as f:
    json.dump(state, f)
```

> **Note**: `/data` is only available at runtime, not during build.

### Using Hub as Storage

```python
from huggingface_hub import upload_file, hf_hub_download
import os

def save_to_hub(data, filename):
    upload_file(
        path_or_fileobj=data,
        path_in_repo=filename,
        repo_id="user/data-repo",
        repo_type="dataset",
        token=os.environ.get("HF_TOKEN")
    )

def load_from_hub(filename):
    return hf_hub_download(
        repo_id="user/data-repo",
        filename=filename,
        repo_type="dataset",
        token=os.environ.get("HF_TOKEN")
    )
```

## Health Checks

```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:7860/health || exit 1
```

```python
# In your app
@app.get("/health")
def health_check():
    return {"status": "healthy"}
```

## Multiple Ports

Internal ports can be any number. Only `app_port` is exposed externally.

For multiple services, use a reverse proxy:

```dockerfile
FROM nginx:alpine

# Custom nginx config
COPY nginx.conf /etc/nginx/nginx.conf

# Copy your apps
COPY --chown=user app1 /app1
COPY --chown=user app2 /app2

EXPOSE 7860
```

```nginx
# nginx.conf
events {}
http {
    server {
        listen 7860;

        location /api {
            proxy_pass http://localhost:8000;
        }

        location / {
            proxy_pass http://localhost:3000;
        }
    }
}
```

## Preloading Models

Speed up startup by preloading during build:

```yaml
---
preload_from_hub:
  - bert-base-uncased config.json,pytorch_model.bin
  - user/private-model
---
```

Or in Dockerfile:

```dockerfile
RUN --mount=type=secret,id=HF_TOKEN,mode=0444,required=true \
    python -c "from huggingface_hub import snapshot_download; \
    snapshot_download('bert-base-uncased', token=open('/run/secrets/HF_TOKEN').read().strip())"
```

## Startup Timeout

```yaml
---
startup_duration_timeout: 1h
---
```

Default is 30 minutes. Useful for large model downloads.

## Debugging

### View Build Logs

Build logs are available in the Space's "Logs" tab.

### Interactive Debugging

```dockerfile
# Add debugging tools
RUN apt-get update && apt-get install -y curl wget vim

# Keep container running for debugging
# CMD ["tail", "-f", "/dev/null"]
```

### Common Issues

**Permission denied errors:**
```dockerfile
# Ensure user owns all files
COPY --chown=user . .
# Or fix permissions
RUN chmod -R 755 /app
```

**Port not accessible:**
```yaml
# Verify app_port matches your application
app_port: 7860
```

**Secret not found:**
```dockerfile
# Check secret is mounted correctly
RUN --mount=type=secret,id=MY_SECRET,mode=0444,required=true \
    test -f /run/secrets/MY_SECRET
```

## Example: Full FastAPI + ML Model

```dockerfile
FROM python:3.10-slim

# System dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create user
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user PATH=/home/user/.local/bin:$PATH
WORKDIR $HOME/app

# Install Python dependencies
COPY --chown=user requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download model at build time (public model)
RUN python -c "from transformers import AutoModel; AutoModel.from_pretrained('bert-base-uncased')"

# Copy application
COPY --chown=user . .

EXPOSE 7860

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
```

**main.py:**
```python
from fastapi import FastAPI
from transformers import pipeline

app = FastAPI()
classifier = pipeline("sentiment-analysis")

@app.get("/")
def read_root():
    return {"status": "running"}

@app.post("/predict")
def predict(text: str):
    return classifier(text)

@app.get("/health")
def health():
    return {"status": "healthy"}
```
