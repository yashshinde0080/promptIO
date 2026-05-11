# Spaces Integration Reference

Embedding Spaces, OAuth authentication, and MCP server hosting.

## Embedding Spaces

Embed your Space in any website using iframes or WebComponents.

### Direct URL

Every Space has a unique URL:

```
https://<username>-<space-name>.hf.space
```

Example: `https://nimaboscarino-hotdog-gradio.hf.space`

Find the URL in Space options menu → "Embed this Space"

### IFrame Embedding

```html
<iframe
    src="https://username-spacename.hf.space"
    frameborder="0"
    width="850"
    height="450"
></iframe>
```

**Responsive iframe:**

```html
<div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden;">
    <iframe
        src="https://username-spacename.hf.space"
        style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"
        frameborder="0"
    ></iframe>
</div>
```

### WebComponents (Gradio Spaces)

WebComponents auto-adjust size and are faster than iframes.

```html
<!-- Load Gradio JS (match version in Space) -->
<script
    type="module"
    src="https://gradio.s3-us-west-2.amazonaws.com/5.0.0/gradio.js"
></script>

<!-- Embed the Space -->
<gradio-app src="https://username-spacename.hf.space"></gradio-app>
```

**With custom styling:**

```html
<gradio-app
    src="https://username-spacename.hf.space"
    initial_height="500px"
    eager="true"
></gradio-app>
```

### Disable Embedding

Prevent your Space from being embedded:

```yaml
---
disable_embedding: true
---
```

### Cross-Origin Headers

Enable SharedArrayBuffer for advanced features:

```yaml
---
custom_headers:
  cross-origin-embedder-policy: require-corp
  cross-origin-opener-policy: same-origin
  cross-origin-resource-policy: cross-origin
---
```

## OAuth / Sign-In with HF

Enable HF account sign-in in your Space.

### Enable OAuth

```yaml
---
hf_oauth: true
hf_oauth_scopes:
  - read-repos      # Read user's repos
  - write-repos     # Write to user's repos
  - inference-api   # Make inference requests
hf_oauth_expiration_minutes: 480  # Token duration (default 8h, max 30 days)
---
```

### Available Scopes

| Scope | Description |
|-------|-------------|
| `openid` | Always included - ID token |
| `profile` | Always included - username, avatar |
| `email` | User's email address |
| `read-billing` | Check payment method |
| `read-repos` | Read user's private repos |
| `write-repos` | Write to user's repos |
| `manage-repos` | Full repo access + create/delete |
| `inference-api` | Make inference requests for user |

### Environment Variables

When OAuth is enabled, these are available:

```python
import os

OAUTH_CLIENT_ID = os.environ["OAUTH_CLIENT_ID"]
OAUTH_CLIENT_SECRET = os.environ["OAUTH_CLIENT_SECRET"]
OAUTH_SCOPES = os.environ["OAUTH_SCOPES"]
OPENID_PROVIDER_URL = os.environ["OPENID_PROVIDER_URL"]
```

### Gradio Integration

```python
import gradio as gr

def greet(profile: gr.OAuthProfile | None):
    if profile is None:
        return "Please log in with your HF account"
    return f"Hello, {profile.name}! (Username: {profile.username})"

with gr.Blocks() as demo:
    gr.LoginButton()  # Built-in login button
    output = gr.Textbox()
    demo.load(greet, outputs=output)

demo.launch()
```

### JavaScript Integration

```javascript
import { oauthLoginUrl, oauthHandleRedirectIfPresent } from "@huggingface/hub";

// Check if returning from OAuth
const oauthResult = await oauthHandleRedirectIfPresent();

if (!oauthResult) {
    // Redirect to login
    window.location.href = await oauthLoginUrl();
} else {
    // User is logged in
    console.log("Access token:", oauthResult.accessToken);
    console.log("User info:", oauthResult.userInfo);
}
```

### Manual OAuth Flow

1. **Redirect user to authorization:**

```
https://huggingface.co/oauth/authorize?
  client_id={OAUTH_CLIENT_ID}&
  redirect_uri={YOUR_CALLBACK_URL}&
  scope=openid%20profile&
  state={RANDOM_STATE}
```

2. **Handle callback:**

```python
# User returns with ?code=XXX&state=YYY
code = request.args.get("code")
state = request.args.get("state")

# Verify state matches what you sent
```

3. **Exchange code for tokens:**

```python
import requests
import base64

credentials = base64.b64encode(
    f"{OAUTH_CLIENT_ID}:{OAUTH_CLIENT_SECRET}".encode()
).decode()

response = requests.post(
    "https://huggingface.co/oauth/token",
    headers={"Authorization": f"Basic {credentials}"},
    data={
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": YOUR_CALLBACK_URL
    }
)

tokens = response.json()
access_token = tokens["access_token"]
id_token = tokens["id_token"]
```

### Restrict to Organization

```yaml
---
hf_oauth: true
hf_oauth_authorized_org: my-organization
# Or multiple orgs:
hf_oauth_authorized_org:
  - org1
  - org2
---
```

## MCP Servers

Host Model Context Protocol (MCP) servers in Spaces.

### What is MCP?

MCP enables AI assistants to interact with external tools and data sources.
Spaces can host MCP servers that Claude and other AI tools can connect to.

### MCP Server Space Example

```yaml
---
title: My MCP Server
emoji: 🔧
sdk: docker
app_port: 8000
tags:
  - mcp-server
---
```

**Dockerfile:**

```dockerfile
FROM python:3.10-slim

RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user PATH=/home/user/.local/bin:$PATH
WORKDIR $HOME/app

COPY --chown=user requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=user . .

EXPOSE 8000

CMD ["python", "server.py"]
```

**server.py:**

```python
from mcp.server import Server
from mcp.server.stdio import stdio_server

server = Server("my-mcp-server")

@server.tool()
async def search_hub(query: str) -> str:
    """Search Hugging Face Hub for models."""
    from huggingface_hub import HfApi
    api = HfApi()
    models = api.list_models(search=query, limit=5)
    return "\n".join([m.id for m in models])

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

### Connecting to MCP Server

In Claude Desktop or compatible clients:

```json
{
  "mcpServers": {
    "hf-search": {
      "url": "https://username-mcp-server.hf.space"
    }
  }
}
```

## Programmatic Space Control

### Request Hardware Change

```python
from huggingface_hub import HfApi

api = HfApi()

# Request GPU
api.request_space_hardware(
    repo_id="username/my-space",
    hardware="t4-small"
)
```

### Pause/Restart Space

```python
# Pause (stop billing)
api.pause_space(repo_id="username/my-space")

# Restart
api.restart_space(repo_id="username/my-space")

# Restart with factory reset
api.restart_space(
    repo_id="username/my-space",
    factory_reboot=True
)
```

### Get Space Runtime Status

```python
runtime = api.get_space_runtime(repo_id="username/my-space")
print(f"Stage: {runtime.stage}")  # RUNNING, BUILDING, etc.
print(f"Hardware: {runtime.hardware}")
```

### Duplicate a Space

```python
api.duplicate_space(
    from_id="gradio/text-generation",
    to_id="username/my-copy",
    private=True
)
```

## Space Secrets via API

```python
# Add secret
api.add_space_secret(
    repo_id="username/my-space",
    key="API_KEY",
    value="sk-xxx"
)

# Delete secret
api.delete_space_secret(
    repo_id="username/my-space",
    key="API_KEY"
)
```

## Resources

- Spaces embedding docs: https://huggingface.co/docs/hub/spaces-embed
- OAuth guide: https://huggingface.co/docs/hub/spaces-oauth
- Gradio OAuth: https://www.gradio.app/guides/sharing-your-app#o-auth-login-via-hugging-face
- huggingface.js OAuth: https://huggingface.co/docs/huggingface.js/hub/README#oauth-login
