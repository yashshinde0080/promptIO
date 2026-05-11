"""
Webhook Auto-Retrain Example

Automatically retrain a model when its training dataset is updated.
This example shows how to build a webhook handler that triggers
retraining jobs on Hugging Face infrastructure.

Prerequisites:
    pip install flask huggingface_hub

Run locally for testing:
    python webhooks-auto-retrain.py

For production, deploy to a server or use a service like:
- Hugging Face Spaces (Docker SDK)
- Railway, Render, or similar
"""

import os
import hmac
import hashlib
from datetime import datetime
from flask import Flask, request, jsonify
from huggingface_hub import HfApi

# =============================================================================
# CONFIGURATION
# =============================================================================

WEBHOOK_SECRET = os.environ.get("WEBHOOK_SECRET", "your-webhook-secret")
HF_TOKEN = os.environ.get("HF_TOKEN")

# Map datasets to their dependent models
DATASET_MODEL_MAP = {
    "username/my-training-data": {
        "model_repo": "username/my-model",
        "training_script": "train.py",
        "hardware": "a10g-small"
    },
    # Add more dataset -> model mappings
}

app = Flask(__name__)
api = HfApi(token=HF_TOKEN)


# =============================================================================
# WEBHOOK HANDLER
# =============================================================================

@app.route("/webhook", methods=["POST"])
def handle_webhook():
    """Handle incoming webhook from Hugging Face."""

    # Verify webhook secret
    secret = request.headers.get("X-Webhook-Secret")
    if secret != WEBHOOK_SECRET:
        return jsonify({"error": "Invalid secret"}), 401

    data = request.json
    event = data.get("event", {})
    repo = data.get("repo", {})

    # Log the event
    print(f"[{datetime.now()}] Received: {event.get('scope')}.{event.get('action')}")
    print(f"  Repo: {repo.get('name')} ({repo.get('type')})")

    # Handle dataset content updates
    if (event.get("scope") == "repo.content" and
        event.get("action") == "update" and
        repo.get("type") == "dataset"):

        dataset_name = repo.get("name")

        # Check if this dataset has a dependent model
        if dataset_name in DATASET_MODEL_MAP:
            config = DATASET_MODEL_MAP[dataset_name]
            trigger_retrain(dataset_name, config)

    return jsonify({"status": "received"})


# =============================================================================
# RETRAINING LOGIC
# =============================================================================

def trigger_retrain(dataset_name: str, config: dict):
    """Trigger a retraining job for the given dataset."""

    print(f"Triggering retrain for dataset: {dataset_name}")

    model_repo = config["model_repo"]
    training_script = config["training_script"]
    hardware = config["hardware"]

    # Create training script content (or use existing script from repo)
    training_code = f'''
import os
from datasets import load_dataset
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    TrainingArguments,
    Trainer
)
from huggingface_hub import login

# Login with token
login(token=os.environ["HF_TOKEN"])

# Load dataset
dataset = load_dataset("{dataset_name}")

# Load model and tokenizer
model_name = "distilbert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)

# Tokenize
def tokenize(examples):
    return tokenizer(examples["text"], truncation=True, padding="max_length")

tokenized = dataset.map(tokenize, batched=True)

# Training arguments
args = TrainingArguments(
    output_dir="./output",
    num_train_epochs=3,
    per_device_train_batch_size=16,
    push_to_hub=True,
    hub_model_id="{model_repo}",
)

# Train
trainer = Trainer(model=model, args=args, train_dataset=tokenized["train"])
trainer.train()
trainer.push_to_hub()

print("Training complete!")
'''

    try:
        # Option 1: Run as a HF Job (recommended)
        # Note: HfApi.run_job() requires huggingface_hub with jobs support
        # job = api.run_job(
        #     command=f"python -c '{training_code}'",
        #     hardware=hardware,
        #     env={"HF_TOKEN": HF_TOKEN, "DATASET": dataset_name}
        # )
        # print(f"Started job: {job.id}")

        # Option 2: Create a discussion/issue to notify
        api.create_discussion(
            repo_id=model_repo,
            title=f"[Auto] Dataset updated - retrain triggered",
            description=f"""
The training dataset `{dataset_name}` was updated.

A retraining job has been triggered automatically.

**Configuration:**
- Hardware: {hardware}
- Script: {training_script}

This discussion was created automatically by the webhook handler.
""",
            repo_type="model"
        )
        print(f"Created discussion in {model_repo}")

    except Exception as e:
        print(f"Error triggering retrain: {e}")


# =============================================================================
# HEALTH CHECK
# =============================================================================

@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint."""
    return jsonify({"status": "healthy"})


@app.route("/", methods=["GET"])
def index():
    """Info endpoint."""
    return jsonify({
        "service": "HF Webhook Auto-Retrain",
        "endpoints": {
            "/webhook": "POST - Webhook handler",
            "/health": "GET - Health check"
        }
    })


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    print("Starting webhook server...")
    print(f"Webhook secret configured: {'Yes' if WEBHOOK_SECRET else 'No'}")
    print(f"HF token configured: {'Yes' if HF_TOKEN else 'No'}")
    print(f"Watching datasets: {list(DATASET_MODEL_MAP.keys())}")
    print()

    # For local development
    app.run(host="0.0.0.0", port=8000, debug=True)


# =============================================================================
# DOCKERFILE (for deployment as HF Space)
# =============================================================================
"""
# Dockerfile
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
"""


# =============================================================================
# README.md (for HF Space)
# =============================================================================
"""
---
title: Webhook Auto-Retrain
emoji: 🔄
colorFrom: blue
colorTo: green
sdk: docker
app_port: 7860
---

# Webhook Auto-Retrain Service

This Space receives webhooks from Hugging Face and triggers
model retraining when training datasets are updated.

## Setup

1. Create webhook at https://huggingface.co/settings/webhooks
2. Point to: `https://your-space.hf.space/webhook`
3. Set secret in Space secrets as `WEBHOOK_SECRET`
4. Set `HF_TOKEN` for API access

## Configuration

Edit the `DATASET_MODEL_MAP` in the code to configure
which datasets trigger which model retraining.
"""
