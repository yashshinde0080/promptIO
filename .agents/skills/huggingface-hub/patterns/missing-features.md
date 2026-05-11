# Missing Features and Workarounds

This document provides guidance for features that don't have official Hugging Face support but have common workarounds.

## iOS / Mobile Development

**Status:** No official Hugging Face SDK for iOS, Android, or React Native.

### Recommended Approaches

#### 1. REST API (Recommended)

Use the HTTP API directly from any platform:

```swift
// Swift example
let url = URL(string: "https://router.huggingface.co/v1/chat/completions")!
var request = URLRequest(url: url)
request.httpMethod = "POST"
request.addValue("Bearer \(hfToken)", forHTTPHeaderField: "Authorization")
request.addValue("application/json", forHTTPHeaderField: "Content-Type")

let body: [String: Any] = [
    "model": "meta-llama/Llama-3.1-8B-Instruct",
    "messages": [["role": "user", "content": "Hello!"]]
]
request.httpBody = try? JSONSerialization.data(withJSONObject: body)
```

```kotlin
// Kotlin/Android example
val client = OkHttpClient()
val json = """
{
    "model": "meta-llama/Llama-3.1-8B-Instruct",
    "messages": [{"role": "user", "content": "Hello!"}]
}
""".trimIndent()

val request = Request.Builder()
    .url("https://router.huggingface.co/v1/chat/completions")
    .addHeader("Authorization", "Bearer $hfToken")
    .post(json.toRequestBody("application/json".toMediaType()))
    .build()
```

#### 2. Core ML Export (iOS On-Device)

For on-device inference on iOS:

1. Export model to Core ML format using `coremltools`
2. Include the `.mlmodel` file in your Xcode project
3. Use Apple's Core ML framework for inference

```python
# Export to Core ML
import coremltools as ct
from transformers import AutoModelForSequenceClassification

model = AutoModelForSequenceClassification.from_pretrained("distilbert-base-uncased")
# Convert to Core ML (see coremltools documentation for full process)
```

#### 3. ONNX Runtime Mobile

For cross-platform mobile inference:

1. Export model to ONNX format
2. Use ONNX Runtime Mobile SDK

```python
# Export to ONNX
from transformers import AutoModel
from transformers.onnx import export

model = AutoModel.from_pretrained("bert-base-uncased")
# Use optimum library for export
# pip install optimum[onnxruntime]
from optimum.onnxruntime import ORTModelForSequenceClassification
ort_model = ORTModelForSequenceClassification.from_pretrained("bert-base-uncased", export=True)
```

## Next.js / React Patterns

**Status:** No official Next.js-specific documentation, but patterns work well.

### Server-Side (API Routes / Server Actions)

```typescript
// app/api/chat/route.ts (App Router)
import { NextResponse } from 'next/server';

export async function POST(request: Request) {
  const { message } = await request.json();

  const response = await fetch('https://router.huggingface.co/v1/chat/completions', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${process.env.HF_TOKEN}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      model: 'meta-llama/Llama-3.1-8B-Instruct',
      messages: [{ role: 'user', content: message }],
    }),
  });

  const data = await response.json();
  return NextResponse.json(data);
}
```

### Client-Side with @huggingface/inference

```typescript
// components/Chat.tsx
'use client';

import { InferenceClient } from '@huggingface/inference';

const client = new InferenceClient(process.env.NEXT_PUBLIC_HF_TOKEN);

async function chat(message: string) {
  const response = await client.chatCompletion({
    model: 'meta-llama/Llama-3.1-8B-Instruct',
    messages: [{ role: 'user', content: message }],
  });
  return response.choices[0].message.content;
}
```

### Streaming with Server Actions

```typescript
// app/actions.ts
'use server';

export async function* streamChat(message: string) {
  const response = await fetch('https://router.huggingface.co/v1/chat/completions', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${process.env.HF_TOKEN}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      model: 'meta-llama/Llama-3.1-8B-Instruct',
      messages: [{ role: 'user', content: message }],
      stream: true,
    }),
  });

  const reader = response.body?.getReader();
  // Process SSE stream...
}
```

## Fully Offline / Air-Gapped Environments

**Status:** Supported but requires manual setup.

### Environment Variables

```bash
# Disable all network requests
export HF_HUB_OFFLINE=1

# Set custom cache directory
export HF_HOME=/path/to/cache
export HF_HUB_CACHE=/path/to/cache/hub

# Disable telemetry
export HF_HUB_DISABLE_TELEMETRY=1
export TRANSFORMERS_OFFLINE=1
export DATASETS_OFFLINE=1
```

### Pre-Download Strategy

**On a connected machine:**

```python
from huggingface_hub import snapshot_download

# Download entire model repository
snapshot_download(
    repo_id="bert-base-uncased",
    local_dir="/path/to/export/bert-base-uncased",
    local_dir_use_symlinks=False  # Copy files, don't symlink
)

# Download specific files only
from huggingface_hub import hf_hub_download
hf_hub_download(
    repo_id="bert-base-uncased",
    filename="config.json",
    local_dir="/path/to/export"
)
```

**Transfer to air-gapped machine:**

```bash
# Archive the cache
tar -czvf hf_cache.tar.gz /path/to/export/

# On air-gapped machine
tar -xzvf hf_cache.tar.gz -C $HF_HOME/hub/
```

**Use offline:**

```python
import os
os.environ['HF_HUB_OFFLINE'] = '1'
os.environ['HF_HOME'] = '/path/to/cache'

from transformers import AutoModel
# Will load from local cache only
model = AutoModel.from_pretrained("bert-base-uncased")
```

### Local Model Loading

```python
# Load from local directory directly
from transformers import AutoModelForCausalLM, AutoTokenizer

model = AutoModelForCausalLM.from_pretrained(
    "/path/to/local/model",
    local_files_only=True
)
tokenizer = AutoTokenizer.from_pretrained(
    "/path/to/local/model",
    local_files_only=True
)
```

## WebAssembly / Edge Runtime

**Status:** Transformers.js provides browser/edge support.

### Browser Inference with Transformers.js

```html
<script type="module">
  import { pipeline } from 'https://cdn.jsdelivr.net/npm/@huggingface/transformers';

  // Models are downloaded and cached in browser
  const classifier = await pipeline(
    'sentiment-analysis',
    'Xenova/distilbert-base-uncased-finetuned-sst-2-english'
  );

  const result = await classifier('I love this!');
  console.log(result);
</script>
```

### Cloudflare Workers / Vercel Edge

```typescript
// Works in edge runtime
import { InferenceClient } from '@huggingface/inference';

export const runtime = 'edge';

export async function POST(request: Request) {
  const client = new InferenceClient(process.env.HF_TOKEN);

  const result = await client.chatCompletion({
    model: 'meta-llama/Llama-3.1-8B-Instruct',
    messages: [{ role: 'user', content: 'Hello!' }],
  });

  return Response.json(result);
}
```

## Limitations Summary

| Feature | Status | Workaround |
|---------|--------|------------|
| iOS SDK | Not available | Use REST API or Core ML export |
| Android SDK | Not available | Use REST API or ONNX Runtime |
| React Native | Not available | Use REST API |
| Next.js docs | Community patterns | Server/client patterns above |
| Full offline | Manual setup | Pre-download + env vars |
| Edge Runtime | Partial | Transformers.js or API calls |

## Getting Help

- **Community Forum:** https://discuss.huggingface.co
- **GitHub Issues:** https://github.com/huggingface/huggingface_hub/issues
- **Discord:** https://hf.co/join/discord

If you need a feature that's missing, consider:
1. Opening a feature request on GitHub
2. Contributing to the open-source libraries
3. Using the REST API as a universal fallback
