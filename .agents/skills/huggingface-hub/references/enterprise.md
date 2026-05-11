# Enterprise Hub Features

Reference for Hugging Face Enterprise Hub features.

## Overview

Enterprise Hub provides:
- Private model/dataset hosting
- Team collaboration
- Access controls
- Audit logging
- SSO integration
- Dedicated support

## Organizations

### Creating Organizations

1. Go to https://huggingface.co/organizations/new
2. Choose organization name
3. Select plan (Free, Pro, Enterprise)

### Organization Settings

- **Members**: Invite and manage team members
- **Teams**: Create sub-groups with specific permissions
- **Billing**: Manage subscription and usage
- **SSO**: Configure single sign-on
- **Audit Logs**: View activity history

## Access Controls

### Repository Visibility

```python
from huggingface_hub import HfApi

api = HfApi()

# Create private repo
api.create_repo(
    repo_id="org/model",
    private=True
)

# Change visibility
api.update_repo_visibility(
    repo_id="org/model",
    private=True
)
```

### Team-Based Access

1. Create teams in organization settings
2. Assign repos to teams
3. Set team permissions (read/write/admin)

### Gated Repositories

For controlled access:

1. Enable gating in repo settings
2. Configure access request form
3. Review and approve requests
4. Optionally auto-approve for org members

```yaml
# In README.md metadata for gated models
---
gated: true
gated_prompt: "Please describe your intended use case"
gated_fields:
  - name: company
    type: text
  - name: use_case
    type: text
---
```

## SSO Integration

### SAML SSO

1. Configure SAML in organization settings
2. Provide IdP metadata URL
3. Configure attribute mapping
4. Enable SSO enforcement

Supported providers:
- Okta
- Azure AD
- Google Workspace
- OneLogin
- Custom SAML 2.0

### SSO Configuration

```
IdP Entity ID: https://your-idp.com
SSO URL: https://your-idp.com/sso
Certificate: [Upload X.509 certificate]

Attribute Mapping:
- email: user.email
- name: user.name
```

## Audit Logs

View all organization activity:

- Repository access
- Member changes
- Settings modifications
- API usage

Access via Organization Settings → Audit Logs

### Log Events

| Event | Description |
|-------|-------------|
| `repo.create` | Repository created |
| `repo.delete` | Repository deleted |
| `repo.update_visibility` | Visibility changed |
| `member.add` | Member added |
| `member.remove` | Member removed |
| `team.create` | Team created |
| `sso.login` | SSO login |

## Inference Endpoints

Deploy models as dedicated endpoints:

```python
from huggingface_hub import create_inference_endpoint

endpoint = create_inference_endpoint(
    name="my-endpoint",
    repository="org/model",
    framework="pytorch",
    task="text-generation",
    accelerator="gpu",
    instance_size="medium",
    instance_type="nvidia-a10g",
    region="us-east-1"
)

# Wait for deployment
endpoint.wait()

# Use endpoint
result = endpoint.client.text_generation("Hello")
```

### Endpoint Configuration

| Setting | Options |
|---------|---------|
| `accelerator` | `cpu`, `gpu` |
| `instance_size` | `small`, `medium`, `large`, `xlarge` |
| `instance_type` | `nvidia-t4`, `nvidia-a10g`, `nvidia-a100` |
| `region` | `us-east-1`, `eu-west-1`, `ap-southeast-1` |
| `min_replica` | 0-10 (0 for scale-to-zero) |
| `max_replica` | 1-10 |

### Autoscaling

```python
endpoint = create_inference_endpoint(
    name="my-endpoint",
    repository="org/model",
    # ...
    min_replica=0,     # Scale to zero when idle
    max_replica=5,     # Max 5 replicas
    scale_to_zero_timeout=15  # Minutes before scaling to zero
)
```

## Private Hub

For on-premise or VPC deployment:

- Self-hosted Hub instance
- Air-gapped environments
- Custom domain
- Full data control

Contact sales for Private Hub setup.

## Resource Groups

Organize repositories by project or team:

```python
# Create resource group
api.create_collection(
    title="Project Alpha Models",
    namespace="org",
    description="Models for Project Alpha"
)

# Add items to collection
api.add_collection_item(
    collection_slug="org/project-alpha-models",
    item_id="org/model-1",
    item_type="model"
)
```

## Billing & Usage

### View Usage

```python
# Check organization usage
# Available in organization settings dashboard
```

### Cost Management

- Set spending limits
- Monitor usage alerts
- Export billing reports

## Compliance

### SOC 2

Enterprise Hub is SOC 2 Type II certified.

### GDPR

- Data Processing Agreement available
- EU data residency options
- Right to deletion support

### HIPAA

Contact sales for HIPAA BAA.

## API Rate Limits

Enterprise plans have higher rate limits:

| Plan | Requests/min | Requests/hour |
|------|-------------|---------------|
| Free | 100 | 1,000 |
| Pro | 500 | 10,000 |
| Enterprise | Custom | Custom |

## Support

### Support Channels

- **Free**: Community forum, GitHub issues
- **Pro**: Email support, 48h response
- **Enterprise**: Dedicated support, SLA, Slack channel

### Enterprise SLA

- 99.9% uptime guarantee
- 4-hour response time for critical issues
- Dedicated customer success manager

## Integrations

### CI/CD Integration

```yaml
# GitHub Actions example
name: Push to Hub

on:
  push:
    branches: [main]

jobs:
  push:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Push to Hub
        env:
          HF_TOKEN: ${{ secrets.HF_TOKEN }}
        run: |
          pip install huggingface_hub
          huggingface-cli upload org/model ./model
```

### Webhook Integration

Configure webhooks for:
- Repository events
- Discussion updates
- Deployment status

```
Webhook URL: https://your-service.com/webhook
Events: repo.push, discussion.create
Secret: [your-webhook-secret]
```

## Security Best Practices

1. **Use fine-grained tokens** - Minimal permissions
2. **Enable SSO** - Centralized authentication
3. **Review audit logs** - Regular monitoring
4. **Gate sensitive models** - Controlled access
5. **Rotate tokens** - Regular credential rotation
6. **Use private repos** - Default to private
7. **Enable 2FA** - For all members

## Migration

### From Other Platforms

```python
# Migrate from S3
from huggingface_hub import upload_folder
import boto3

# Download from S3
s3 = boto3.client('s3')
s3.download_file('bucket', 'model/', './model')

# Upload to Hub
upload_folder(
    folder_path="./model",
    repo_id="org/model",
    repo_type="model"
)
```

### Bulk Operations

```python
# Migrate multiple repositories
repos = ["model1", "model2", "model3"]

for repo in repos:
    api.create_repo(f"org/{repo}")
    upload_folder(f"./{repo}", f"org/{repo}")
```
