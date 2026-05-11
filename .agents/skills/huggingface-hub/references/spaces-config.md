# Spaces Configuration Reference

Complete YAML configuration reference for Hugging Face Spaces.

## Basic Configuration

```yaml
---
title: My Space
emoji: 🚀
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: 5.0.0
app_file: app.py
---
```

## All Configuration Options

### Display Settings

| Parameter | Type | Description |
|-----------|------|-------------|
| `title` | string | Display title for the Space |
| `emoji` | string | Space emoji (emoji character only) |
| `colorFrom` | string | Gradient start color: `red`, `yellow`, `green`, `blue`, `indigo`, `purple`, `pink`, `gray` |
| `colorTo` | string | Gradient end color (same options as colorFrom) |
| `thumbnail` | string | URL for custom social sharing thumbnail |
| `short_description` | string | Brief description shown in Space card |

### SDK Settings

| Parameter | Type | Description |
|-----------|------|-------------|
| `sdk` | string | **Required.** `gradio`, `docker`, or `static` |
| `sdk_version` | string | Gradio version (e.g., `5.0.0`). All versions supported. |
| `python_version` | string | Python version: `3.x` or `3.x.x`. Default: `3.10` |
| `app_file` | string | Path to main application file (relative to repo root) |
| `app_port` | int | Port for Docker Spaces. Default: `7860` |
| `base_path` | string | Initial URL to render (must start with `/`). Non-static Spaces only. |

### Static Space Settings

| Parameter | Type | Description |
|-----------|------|-------------|
| `app_build_command` | string | Build command (e.g., `npm run build`) |
| `app_file` | string | Path to built HTML (e.g., `dist/index.html`) |

### Hardware Settings

| Parameter | Type | Description |
|-----------|------|-------------|
| `suggested_hardware` | string | Recommended hardware tier |
| `suggested_storage` | string | **Deprecated** - Persistent storage is no longer available |
| `startup_duration_timeout` | string | Max startup time (e.g., `30m`, `1h`). Default: `30m` |

**Hardware Options:**

| Category | Options |
|----------|---------|
| CPU | `cpu-basic`, `cpu-upgrade` |
| GPU | `t4-small`, `t4-medium`, `l4x1`, `l4x4`, `a10g-small`, `a10g-large`, `a10g-largex2`, `a10g-largex4`, `a100-large`, `a100x4`, `a100x8` |
| TPU | `v5e-1x1`, `v5e-2x2`, `v5e-2x4` |

**Requesting Hardware:**

1. **Via YAML** (recommended): Set `suggested_hardware` in README.md frontmatter
2. **Via Settings UI**: Space Settings > Hardware > Select tier
3. **Via API**:
   ```python
   from huggingface_hub import HfApi
   api = HfApi()
   api.request_space_hardware(repo_id="user/my-space", hardware="a10g-small")
   ```

**Access Requirements:**
- CPU tiers: Available to all users
- T4/L4 GPUs: Available to Pro subscribers and organization members
- A10G/A100 GPUs: Requires Pro subscription or organization with compute quota
- Hardware changes take effect on next Space restart

### Layout Settings

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `fullWidth` | boolean | `true` | Render full-width vs fixed-width container |
| `header` | string | `default` | Header style: `default` or `mini` (floating mini header) |

### Metadata

| Parameter | Type | Description |
|-----------|------|-------------|
| `models` | List[string] | Model IDs used (e.g., `openai-community/gpt2`) |
| `datasets` | List[string] | Dataset IDs used |
| `tags` | List[string] | Descriptive tags |
| `pinned` | boolean | Pin to top of profile |

### Authentication

| Parameter | Type | Description |
|-----------|------|-------------|
| `hf_oauth` | boolean | Enable HF OAuth sign-in |
| `hf_oauth_scopes` | List[string] | OAuth scopes (e.g., `read-repos`, `write-repos`) |
| `hf_oauth_expiration_minutes` | int | Token duration. Default: `480` (8 hours). Max: `43200` (30 days) |
| `hf_oauth_authorized_org` | string or List[string] | Restrict to organization members |

### Security Settings

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `disable_embedding` | boolean | `false` | Prevent embedding in iframes |

### Custom Headers

```yaml
custom_headers:
  cross-origin-embedder-policy: require-corp
  cross-origin-opener-policy: same-origin
  cross-origin-resource-policy: cross-origin
```

Enables `SharedArrayBuffer` and other cross-origin isolated features.

### Preloading

```yaml
preload_from_hub:
  # Entire repository
  - coqui/XTTS-v1

  # Specific files
  - warp-ai/wuerstchen-prior text_encoder/model.safetensors,prior/diffusion_pytorch_model.safetensors

  # Specific revision
  - openai-community/gpt2 config.json abc123def456
```

Files are cached to `~/.cache/huggingface/hub` during build.

> **Note**: Private repo preloading is not yet supported.

## Complete Example

```yaml
---
title: Image Classifier Demo
emoji: 🖼️
colorFrom: green
colorTo: blue
sdk: gradio
sdk_version: 5.0.0
python_version: "3.11"
app_file: app.py

# Hardware
suggested_hardware: t4-small
startup_duration_timeout: 45m

# Display
fullWidth: true
header: mini
pinned: true
short_description: Classify images using ViT

# Metadata
models:
  - google/vit-base-patch16-224
datasets:
  - imagenet-1k
tags:
  - image-classification
  - computer-vision
  - demo

# Preload model for faster startup
preload_from_hub:
  - google/vit-base-patch16-224

# OAuth (optional)
hf_oauth: true
hf_oauth_scopes:
  - read-repos
---

# Image Classifier

Upload an image to classify it using Vision Transformer (ViT).

## Features
- Fast inference with GPU acceleration
- Top-5 predictions with confidence scores
- Example images included
```

## Docker Space Example

```yaml
---
title: FastAPI Backend
emoji: 🐳
colorFrom: purple
colorTo: gray
sdk: docker
app_port: 8000

suggested_hardware: cpu-upgrade
startup_duration_timeout: 1h

models:
  - bert-base-uncased
tags:
  - api
  - nlp
---
```

## Static Space Example

```yaml
---
title: React App
emoji: ⚛️
colorFrom: blue
colorTo: cyan
sdk: static
app_file: dist/index.html
app_build_command: npm run build
---
```

## Environment Variables

Set via Space Settings, not in YAML.

Access in code:
```python
import os
token = os.environ.get("HF_TOKEN")
api_key = os.environ.get("MY_API_KEY")
```

## Validation

The Hub validates YAML configuration on push. Common errors:

- Missing required `sdk` field
- Invalid hardware tier name
- Invalid color names
- Malformed YAML syntax

## Programmatic Configuration

Update Space config via API:

```python
from huggingface_hub import HfApi

api = HfApi()

# Update Space hardware
api.request_space_hardware(
    repo_id="user/my-space",
    hardware="t4-small"
)

# Pause/restart Space
api.pause_space(repo_id="user/my-space")
api.restart_space(repo_id="user/my-space")
```
