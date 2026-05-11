# Security Reference

Security features, tokens, scanning, and gated model access.

## Access Tokens

Tokens authenticate your applications to Hugging Face services.

### Token Types

| Type | Use Case | Permissions |
|------|----------|-------------|
| `fine-grained` | Production apps | Specific resources only |
| `read` | Download models/datasets | Read access to your repos |
| `write` | Upload and modify | Read + write to your repos |

### Creating Tokens

1. Go to https://huggingface.co/settings/tokens
2. Click **New token**
3. Select role and permissions
4. Name your token descriptively

### Fine-Grained Tokens (Recommended)

Create tokens with minimal permissions:

- Access to specific models/datasets only
- Specific organizations
- Time-limited validity

### Using Tokens

```python
# Environment variable (recommended)
import os
os.environ["HF_TOKEN"] = "hf_xxx"

# In code
from huggingface_hub import login
login(token="hf_xxx")

# CLI
huggingface-cli login --token hf_xxx

# In transformers
from transformers import AutoModel
model = AutoModel.from_pretrained("private/model", token="hf_xxx")
```

### Best Practices

1. **One token per application** - Easy to revoke if compromised
2. **Use fine-grained tokens** - Minimize scope
3. **Never commit tokens** - Use environment variables
4. **Rotate regularly** - Especially after team changes

## Gated Models

Control access to your models with approval workflows.

### Enabling Gating

In model settings, enable "Access requests" with:

- **Automatic approval**: Users get access after agreeing to terms
- **Manual approval**: You review each request

### Custom Access Form

```yaml
---
extra_gated_prompt: "You agree to not use this model for harmful purposes."
extra_gated_fields:
  Company: text
  Country: country
  Use case:
    type: select
    options:
      - Research
      - Commercial
      - Personal
  I agree to the license: checkbox
---
```

### Field Types

| Type | Description |
|------|-------------|
| `text` | Single-line text input |
| `checkbox` | Boolean checkbox |
| `date_picker` | Date selection |
| `country` | Country dropdown (ISO 3166-1) |
| `select` | Dropdown with custom options |

### Managing Access via API

```python
from huggingface_hub import HfApi

api = HfApi()

# List pending requests
pending = api.list_pending_access_requests("username/gated-model")

# Accept a user
api.accept_access_request("username/gated-model", user="requesting-user")

# Reject a user
api.reject_access_request("username/gated-model", user="requesting-user")

# Grant access directly
api.grant_access("username/gated-model", user="some-user")
```

### Restrict EU Users

```yaml
---
gated: true
extra_gated_eu_disallowed: true
---
```

## Security Scanning

Hugging Face automatically scans repositories for security issues.

### Malware Scanning

All files are scanned with ClamAV on every commit.

- ✅ Safe files show green checkmark
- ⚠️ Infected files show warning
- Files pending scan show no badge

If infected files are detected, users see a warning banner.

### Pickle Scanning

Python pickle files (`.pkl`, `.bin`) are scanned for:

- Arbitrary code execution
- Suspicious imports
- Known malicious patterns

**Recommendation:** Use `.safetensors` instead of pickle-based formats.

### Secrets Scanning

Repositories are scanned for accidentally committed secrets:

- API keys
- Access tokens
- Passwords
- Private keys

If detected, you'll be notified to rotate and remove them.

## SafeTensors

SafeTensors is the recommended format for model weights.

### Why SafeTensors?

| Feature | SafeTensors | PyTorch .bin |
|---------|-------------|--------------|
| Security | ✅ No code execution | ⚠️ Pickle can run code |
| Load speed | ✅ Fast (mmap) | Slower |
| Memory | ✅ Efficient | Higher peak |
| Format | Simple binary | Python pickle |

### Converting to SafeTensors

```python
from safetensors.torch import save_file
import torch

# Save model in safetensors format
state_dict = model.state_dict()
save_file(state_dict, "model.safetensors")

# Push to Hub
from huggingface_hub import upload_file
upload_file(
    path_or_fileobj="model.safetensors",
    path_in_repo="model.safetensors",
    repo_id="username/my-model"
)
```

## Two-Factor Authentication (2FA)

Enable 2FA for your account:

1. Go to https://huggingface.co/settings/security
2. Click "Enable 2FA"
3. Scan QR code with authenticator app
4. Save backup codes

## SSH Keys

Use SSH for git operations:

```bash
# Generate key
ssh-keygen -t ed25519 -C "your-email@example.com"

# Add to SSH agent
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# Add public key to HF
# Copy contents of ~/.ssh/id_ed25519.pub to:
# https://huggingface.co/settings/keys

# Clone with SSH
git clone git@hf.co:username/repo-name
```

## GPG Commit Signing

Sign commits to verify authorship:

```bash
# Configure Git
git config --global user.signingkey YOUR_GPG_KEY_ID
git config --global commit.gpgsign true

# Add GPG key to HF
# https://huggingface.co/settings/keys

# Signed commits show verified badge
```

## Single Sign-On (SSO)

Enterprise feature for organization authentication.

### Supported Providers

- SAML 2.0
- Okta
- Azure AD
- Google Workspace

Configure in Organization Settings → Security → SSO.

## Resource Groups

Enterprise feature for fine-grained access control.

```python
# Create resource group
api.create_resource_group(
    organization="my-org",
    name="research-team",
    description="Access to research models"
)

# Add repo to group
api.add_repo_to_resource_group(
    organization="my-org",
    resource_group="research-team",
    repo_id="my-org/research-model"
)

# Grant user access
api.add_user_to_resource_group(
    organization="my-org",
    resource_group="research-team",
    user="team-member"
)
```

## Third-Party Scanners

### Protect AI

Scans for model-specific vulnerabilities.

### JFrog

Scans for supply chain security issues.

## Security Contacts

- Security issues: security@huggingface.co
- General questions: support@huggingface.co

## Compliance

- **SOC 2 Type 2** certified
- **GDPR** compliant
- BAA available for Enterprise

## Resources

- Security overview: https://huggingface.co/docs/hub/security
- Token settings: https://huggingface.co/settings/tokens
- SSH keys: https://huggingface.co/settings/keys
- Gated models guide: https://huggingface.co/docs/hub/models-gated
