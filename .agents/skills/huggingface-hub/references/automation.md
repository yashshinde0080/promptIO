# Automation Reference

Webhooks, Jobs, and GitHub Actions for automating Hub workflows.

## Webhooks

Webhooks notify your server when events happen on Hub repositories.

### Creating Webhooks

Configure in Settings: https://huggingface.co/settings/webhooks

**Settings:**
- **Target URL:** Your HTTPS endpoint
- **Secret:** Optional verification token (sent as `X-Webhook-Secret` header)
- **Watched repos:** Specific repos or all repos for users/orgs

### Webhook Events

| Scope | Action | Description |
|-------|--------|-------------|
| `repo` | `create`, `delete`, `update`, `move` | Repository lifecycle |
| `repo.content` | `update` | New commits, tags, or PR refs |
| `repo.config` | `update` | Settings changes (private, etc.) |
| `discussion` | `create`, `delete`, `update` | Discussions/PRs |
| `discussion.comment` | `create`, `update` | Comments |

### Payload Structure

```json
{
  "event": {
    "action": "update",
    "scope": "repo.content"
  },
  "repo": {
    "type": "model",
    "name": "user/model-name",
    "id": "621ffdc036468d709f17434d",
    "private": false,
    "url": {
      "web": "https://huggingface.co/user/model-name",
      "api": "https://huggingface.co/api/models/user/model-name"
    },
    "headSha": "abc123...",
    "owner": {"id": "..."}
  },
  "updatedRefs": [
    {
      "ref": "refs/heads/main",
      "oldSha": "abc123...",
      "newSha": "def456..."
    }
  ],
  "webhook": {
    "id": "...",
    "version": 3
  }
}
```

### Webhook Handler Example (Python/Flask)

```python
from flask import Flask, request, jsonify
import hmac
import hashlib

app = Flask(__name__)
WEBHOOK_SECRET = "your-secret"

def verify_signature(payload, signature):
    expected = hmac.new(
        WEBHOOK_SECRET.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(signature, expected)

@app.route("/webhook", methods=["POST"])
def handle_webhook():
    # Verify secret (if configured)
    secret = request.headers.get("X-Webhook-Secret")
    if secret != WEBHOOK_SECRET:
        return jsonify({"error": "Invalid secret"}), 401

    data = request.json
    event = data["event"]
    repo = data["repo"]

    print(f"Event: {event['scope']}.{event['action']}")
    print(f"Repo: {repo['name']}")

    # Handle specific events
    if event["scope"] == "repo.content" and event["action"] == "update":
        # New commit pushed
        handle_new_commit(data)

    return jsonify({"status": "ok"})

def handle_new_commit(data):
    repo_name = data["repo"]["name"]
    refs = data.get("updatedRefs", [])
    for ref in refs:
        if ref["ref"] == "refs/heads/main":
            print(f"Main branch updated: {ref['newSha']}")
            # Trigger your automation here

if __name__ == "__main__":
    app.run(port=8000)
```

### Rate Limits

- **1,000 triggers per 24 hours** per webhook
- Upgrade to PRO/Enterprise for higher limits

## Jobs

Run compute tasks on Hugging Face infrastructure.

### CLI Usage

```bash
# Install/update huggingface-cli
pip install -U huggingface_hub

# Run a Python script
hf jobs uv run script.py

# Run with specific hardware
hf jobs uv run script.py --hardware a10g-small

# Run a Docker image
hf jobs run python:3.10 python script.py

# List running jobs
hf jobs ps

# View job logs
hf jobs logs <job-id>

# Cancel a job
hf jobs cancel <job-id>
```

### Python API

```python
from huggingface_hub import HfApi

api = HfApi()

# Run a job
job = api.run_job(
    command="python train.py",
    hardware="a10g-small",
    env={"HF_TOKEN": "..."}
)

print(f"Job ID: {job.id}")
print(f"Status: {job.status}")

# List jobs
jobs = api.list_jobs()
for job in jobs:
    print(f"{job.id}: {job.status}")

# Get job logs
logs = api.get_job_logs(job_id="...")
print(logs)
```

### Hardware Options

| Hardware | vCPU | RAM | GPU | Price |
|----------|------|-----|-----|-------|
| `cpu-basic` | 2 | 16GB | - | $ |
| `cpu-upgrade` | 8 | 32GB | - | $$ |
| `t4-small` | 4 | 15GB | T4 16GB | $$ |
| `a10g-small` | 4 | 15GB | A10G 24GB | $$$ |
| `a10g-large` | 12 | 46GB | A10G 24GB | $$$$ |
| `a100-large` | 12 | 142GB | A100 80GB | $$$$$ |

### Scheduled Jobs

```bash
# Run every hour
hf jobs uv run script.py --schedule "@hourly"

# Run daily at midnight
hf jobs uv run script.py --schedule "@daily"

# Custom cron schedule (every 5 minutes)
hf jobs uv run script.py --schedule "*/5 * * * *"
```

### Webhook-Triggered Jobs

Jobs can be triggered by webhooks for automated pipelines.

## GitHub Actions

### Deploy Space on Push

```yaml
# .github/workflows/deploy-space.yml
name: Deploy to HF Space

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Push to HF Space
        env:
          HF_TOKEN: ${{ secrets.HF_TOKEN }}
        run: |
          git remote add space https://huggingface.co/spaces/${{ secrets.HF_USERNAME }}/my-space
          git push space main --force
```

### Sync Model on Release

```yaml
# .github/workflows/sync-model.yml
name: Sync Model to Hub

on:
  release:
    types: [published]

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: pip install huggingface_hub

      - name: Upload to Hub
        env:
          HF_TOKEN: ${{ secrets.HF_TOKEN }}
        run: |
          python -c "
          from huggingface_hub import HfApi
          api = HfApi()
          api.upload_folder(
              folder_path='./model',
              repo_id='${{ secrets.HF_USERNAME }}/my-model',
              repo_type='model'
          )
          "
```

### Run Tests with Hub Models

```yaml
# .github/workflows/test.yml
name: Test with HF Models

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: |
          pip install transformers torch pytest
          pip install -e .

      - name: Run tests
        env:
          HF_TOKEN: ${{ secrets.HF_TOKEN }}
        run: pytest tests/
```

### Auto-Convert Model Formats

```yaml
# .github/workflows/convert.yml
name: Convert to GGUF

on:
  workflow_dispatch:
    inputs:
      model_id:
        description: 'Model ID to convert'
        required: true

jobs:
  convert:
    runs-on: ubuntu-latest
    steps:
      - name: Convert model
        env:
          HF_TOKEN: ${{ secrets.HF_TOKEN }}
        run: |
          pip install huggingface_hub
          # Use llama.cpp conversion or similar
          # Upload converted model to Hub
```

## Automation Patterns

### Auto-Retrain on Dataset Update

```python
# webhook_handler.py
from flask import Flask, request
from huggingface_hub import HfApi

app = Flask(__name__)
api = HfApi()

@app.route("/webhook", methods=["POST"])
def handle():
    data = request.json

    # Check if dataset was updated
    if (data["event"]["scope"] == "repo.content" and
        data["repo"]["type"] == "dataset"):

        # Trigger training job
        api.run_job(
            command="python train.py",
            hardware="a10g-small",
            env={
                "DATASET": data["repo"]["name"],
                "HF_TOKEN": "..."
            }
        )

    return {"status": "ok"}
```

### Auto-Deploy on Model Update

```python
# Webhook triggers Space rebuild when model is updated
@app.route("/webhook", methods=["POST"])
def handle():
    data = request.json

    if data["repo"]["type"] == "model":
        model_name = data["repo"]["name"]

        # Restart dependent Space
        api.restart_space(repo_id="user/my-space")

    return {"status": "ok"}
```

### CI/CD Pipeline

1. **Push code** → GitHub Actions runs tests
2. **Merge to main** → Deploy to HF Space
3. **Create release** → Upload model to Hub
4. **Model updated** → Webhook triggers downstream jobs

## Resources

- Webhooks guide: https://huggingface.co/docs/hub/webhooks
- Jobs docs: https://huggingface.co/docs/hub/jobs-overview
- HfApi reference: https://huggingface.co/docs/huggingface_hub/package_reference/hf_api
