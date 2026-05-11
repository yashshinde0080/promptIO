# Python SDK Reference (huggingface_hub)

Complete reference for the `huggingface_hub` Python library.

## Installation

```bash
pip install huggingface_hub

# With all optional dependencies
pip install "huggingface_hub[all]"

# Specific extras
pip install "huggingface_hub[inference]"  # For InferenceClient
pip install "huggingface_hub[torch]"      # For PyTorch integration
```

## Authentication

### Interactive Login

```python
from huggingface_hub import login

# Opens browser or prompts for token
login()

# With explicit token
login(token="hf_xxx")

# Add to git credential helper
login(token="hf_xxx", add_to_git_credential=True)
```

### Environment Variable

```bash
export HF_TOKEN="hf_xxx"
```

```python
import os
# Token auto-detected from HF_TOKEN
from huggingface_hub import HfApi
api = HfApi()  # Uses HF_TOKEN automatically
```

### CLI Login

```bash
huggingface-cli login
# or
hf auth login

# Non-interactive
huggingface-cli login --token hf_xxx
```

### Token in Code (Not Recommended)

```python
from huggingface_hub import HfApi
api = HfApi(token="hf_xxx")  # Avoid hardcoding tokens
```

## Downloading Files

### Single File Download

```python
from huggingface_hub import hf_hub_download

# Basic download
file_path = hf_hub_download(
    repo_id="bert-base-uncased",
    filename="config.json"
)

# With specific revision
file_path = hf_hub_download(
    repo_id="bert-base-uncased",
    filename="config.json",
    revision="main"  # or commit hash, tag, branch
)

# From a subfolder
file_path = hf_hub_download(
    repo_id="user/model",
    filename="pytorch_model.bin",
    subfolder="checkpoints"
)

# Dataset file
file_path = hf_hub_download(
    repo_id="squad",
    filename="train-v1.1.json",
    repo_type="dataset"
)

# To specific directory
file_path = hf_hub_download(
    repo_id="bert-base-uncased",
    filename="config.json",
    local_dir="./my_model"
)

# Force re-download
file_path = hf_hub_download(
    repo_id="bert-base-uncased",
    filename="config.json",
    force_download=True
)
```

### Download Entire Repository

```python
from huggingface_hub import snapshot_download

# Download all files
local_dir = snapshot_download(repo_id="bert-base-uncased")

# To specific directory
local_dir = snapshot_download(
    repo_id="bert-base-uncased",
    local_dir="./my_model"
)

# Filter files by pattern
local_dir = snapshot_download(
    repo_id="bert-base-uncased",
    allow_patterns=["*.json", "*.txt"],
    ignore_patterns=["*.bin", "*.safetensors"]
)

# Specific revision
local_dir = snapshot_download(
    repo_id="bert-base-uncased",
    revision="v1.0"
)
```

### CLI Download

```bash
# Download entire repo
hf download bert-base-uncased

# Specific files
hf download bert-base-uncased config.json tokenizer.json

# To specific directory
hf download bert-base-uncased --local-dir ./my_model

# Dataset
hf download squad --repo-type dataset
```

### High-Performance Downloads

```bash
# Enable high-performance mode (uses all CPU cores)
HF_XET_HIGH_PERFORMANCE=1 hf download HuggingFaceH4/zephyr-7b-beta
```

## Uploading Files

### Single File Upload

```python
from huggingface_hub import upload_file

# Upload to model repo
upload_file(
    path_or_fileobj="./model.safetensors",
    path_in_repo="model.safetensors",
    repo_id="user/my-model"
)

# Upload to subfolder
upload_file(
    path_or_fileobj="./checkpoint.pt",
    path_in_repo="checkpoints/epoch_10.pt",
    repo_id="user/my-model"
)

# Upload with commit message
upload_file(
    path_or_fileobj="./model.safetensors",
    path_in_repo="model.safetensors",
    repo_id="user/my-model",
    commit_message="Add trained model weights"
)

# Upload from file object
with open("model.safetensors", "rb") as f:
    upload_file(
        path_or_fileobj=f,
        path_in_repo="model.safetensors",
        repo_id="user/my-model"
    )
```

### Folder Upload

```python
from huggingface_hub import upload_folder

# Upload entire folder
upload_folder(
    folder_path="./my_model",
    repo_id="user/my-model"
)

# With patterns
upload_folder(
    folder_path="./my_model",
    repo_id="user/my-model",
    allow_patterns=["*.json", "*.safetensors"],
    ignore_patterns=["*.pyc", "__pycache__"]
)

# To subfolder in repo
upload_folder(
    folder_path="./checkpoints",
    path_in_repo="training/checkpoints",
    repo_id="user/my-model"
)
```

## HfApi Class

### Repository Operations

```python
from huggingface_hub import HfApi

api = HfApi()

# Create repository
api.create_repo(repo_id="user/new-model", repo_type="model")
api.create_repo(repo_id="user/new-dataset", repo_type="dataset")
api.create_repo(repo_id="user/new-space", repo_type="space", space_sdk="gradio")

# Create private repo
api.create_repo(repo_id="user/private-model", private=True)

# Delete repository
api.delete_repo(repo_id="user/old-model")

# Update repo visibility
api.update_repo_visibility(repo_id="user/model", private=True)

# Get repo info
info = api.repo_info(repo_id="bert-base-uncased")
print(info.sha)  # Latest commit
print(info.siblings)  # List of files

# List files
files = api.list_repo_files(repo_id="bert-base-uncased")
```

### File Operations via API

```python
api = HfApi()

# Upload file
api.upload_file(
    path_or_fileobj="./model.safetensors",
    path_in_repo="model.safetensors",
    repo_id="user/my-model"
)

# Delete file
api.delete_file(
    path_in_repo="old_model.bin",
    repo_id="user/my-model"
)

# Get file metadata
file_info = api.get_paths_info(
    repo_id="bert-base-uncased",
    paths=["config.json"]
)
```

### User/Org Operations

```python
api = HfApi()

# Get current user info
user = api.whoami()
print(user["name"])

# List user's models
models = api.list_models(author="username")

# List organization repos
models = api.list_models(author="organization")
```

## PyTorchModelHubMixin

Add Hub integration to any PyTorch model:

```python
import torch
import torch.nn as nn
from huggingface_hub import PyTorchModelHubMixin

class MyModel(nn.Module, PyTorchModelHubMixin,
              # Optional metadata (appears in model card)
              repo_url="https://huggingface.co/user/my-model",
              pipeline_tag="text-classification",
              license="mit",
              tags=["pytorch", "classification"]):

    def __init__(self, num_classes: int, hidden_size: int = 256):
        super().__init__()
        self.config = {"num_classes": num_classes, "hidden_size": hidden_size}
        self.linear = nn.Linear(hidden_size, num_classes)

    def forward(self, x):
        return self.linear(x)

# Create and train model
model = MyModel(num_classes=10, hidden_size=512)

# Save locally (creates config.json + model.safetensors)
model.save_pretrained("./my-model")

# Push to Hub
model.push_to_hub("user/my-model")

# Load from Hub
loaded_model = MyModel.from_pretrained("user/my-model")

# Load from local
loaded_model = MyModel.from_pretrained("./my-model")
```

### With Config Class

```python
from dataclasses import dataclass
from huggingface_hub import PyTorchModelHubMixin

@dataclass
class MyConfig:
    num_classes: int = 10
    hidden_size: int = 256
    dropout: float = 0.1

class MyModel(nn.Module, PyTorchModelHubMixin):
    def __init__(self, config: MyConfig):
        super().__init__()
        self.config = config
        self.linear = nn.Linear(config.hidden_size, config.num_classes)
        self.dropout = nn.Dropout(config.dropout)

# Usage
config = MyConfig(num_classes=5)
model = MyModel(config)
model.push_to_hub("user/my-model")

# Loads with config
model = MyModel.from_pretrained("user/my-model")
```

## Repository Class

Clone and work with repos like Git:

```python
from huggingface_hub import Repository

# Clone repository
repo = Repository(
    local_dir="./my-model",
    clone_from="user/my-model"
)

# Make changes and commit
# ... modify files ...
repo.git_add()
repo.git_commit("Update model weights")
repo.git_push()

# Pull latest changes
repo.git_pull()
```

## Caching

### Cache Location

Default: `~/.cache/huggingface/hub`

```python
# Change cache location
import os
os.environ["HF_HOME"] = "/path/to/cache"
# or
os.environ["HF_HUB_CACHE"] = "/path/to/cache/hub"
```

### Cache Management

```python
from huggingface_hub import scan_cache_dir, delete_cache

# Scan cache
cache_info = scan_cache_dir()
print(f"Cache size: {cache_info.size_on_disk_str}")

for repo in cache_info.repos:
    print(f"{repo.repo_id}: {repo.size_on_disk_str}")

# Delete specific revisions
delete_strategy = cache_info.delete_revisions(
    "bert-base-uncased",
    ["abc123", "def456"]  # commit hashes
)
delete_strategy.execute()
```

### CLI Cache Commands

```bash
# View cache
huggingface-cli scan-cache

# Delete unused files
huggingface-cli delete-cache
```

## Environment Variables

| Variable | Description |
|----------|-------------|
| `HF_TOKEN` | Authentication token |
| `HF_HOME` | Root cache directory |
| `HF_HUB_CACHE` | Hub-specific cache |
| `HF_HUB_OFFLINE` | Offline mode (1 to enable) |
| `HF_HUB_DISABLE_TELEMETRY` | Disable telemetry |
| `HF_XET_HIGH_PERFORMANCE` | High-performance downloads |

## Error Handling

```python
from huggingface_hub import (
    hf_hub_download,
    HfHubHTTPError,
    RepositoryNotFoundError,
    EntryNotFoundError,
    RevisionNotFoundError,
)

try:
    hf_hub_download(repo_id="nonexistent/model", filename="config.json")
except RepositoryNotFoundError:
    print("Repository not found")
except EntryNotFoundError:
    print("File not found in repository")
except RevisionNotFoundError:
    print("Revision not found")
except HfHubHTTPError as e:
    print(f"HTTP error: {e}")
```
