# Inference Providers Reference

Complete guide for using Hugging Face Inference Providers API.

## Overview

Inference Providers allow you to run models via API without managing infrastructure. Models can be served by multiple providers (HF Inference, fal.ai, Replicate, Together, etc.).

## Setup

### Python Installation

```bash
pip install huggingface_hub
```

### TypeScript Installation

```bash
npm install @huggingface/inference
```

### Authentication

```bash
# Set environment variable (recommended)
export HF_TOKEN="hf_xxx"
```

Get tokens at: https://huggingface.co/settings/tokens

## Python Client

### Basic Setup

```python
import os
from huggingface_hub import InferenceClient

client = InferenceClient(
    api_key=os.environ["HF_TOKEN"]
)
```

### Provider Selection

```python
# Auto-select best available provider (default)
client = InferenceClient(provider="auto", api_key=os.environ["HF_TOKEN"])

# Specific provider
client = InferenceClient(provider="fal-ai", api_key=os.environ["HF_TOKEN"])
client = InferenceClient(provider="replicate", api_key=os.environ["HF_TOKEN"])
client = InferenceClient(provider="together", api_key=os.environ["HF_TOKEN"])
```

### Text Generation

```python
# Simple text generation
output = client.text_generation(
    "The answer to life is",
    model="meta-llama/Llama-3.1-8B-Instruct",
    max_new_tokens=100
)
print(output)

# With parameters
output = client.text_generation(
    "Write a poem about AI",
    model="meta-llama/Llama-3.1-8B-Instruct",
    max_new_tokens=200,
    temperature=0.7,
    top_p=0.9,
    repetition_penalty=1.1
)
```

### Chat Completion

```python
# OpenAI-compatible chat format
response = client.chat.completions.create(
    model="meta-llama/Llama-3.1-8B-Instruct",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is the capital of France?"}
    ],
    max_tokens=100,
    temperature=0.7
)
print(response.choices[0].message.content)
```

### Streaming

```python
# Stream text generation
for chunk in client.text_generation(
    "Tell me a story",
    model="meta-llama/Llama-3.1-8B-Instruct",
    max_new_tokens=500,
    stream=True
):
    print(chunk, end="", flush=True)

# Stream chat completion
for chunk in client.chat.completions.create(
    model="meta-llama/Llama-3.1-8B-Instruct",
    messages=[{"role": "user", "content": "Tell me a joke"}],
    stream=True
):
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
```

### Image Generation

```python
# Text to image
image = client.text_to_image(
    "A serene mountain landscape at sunset, digital art",
    model="black-forest-labs/FLUX.1-schnell"
)
# Returns PIL.Image
image.save("output.png")

# With parameters
image = client.text_to_image(
    "Astronaut riding a horse on Mars",
    model="black-forest-labs/FLUX.1-dev",
    num_inference_steps=30,
    guidance_scale=7.5
)
```

### Image Analysis

```python
from PIL import Image

# Image classification
image = Image.open("cat.jpg")
result = client.image_classification(image, model="google/vit-base-patch16-224")
# [{"label": "tabby cat", "score": 0.95}, ...]

# Object detection
detections = client.object_detection(image, model="facebook/detr-resnet-50")
# [{"label": "cat", "score": 0.98, "box": {"xmin": 10, "ymin": 20, ...}}, ...]

# Image captioning
caption = client.image_to_text(image, model="nlpconnect/vit-gpt2-image-captioning")
```

### Audio Tasks

```python
# Speech to text
with open("audio.wav", "rb") as f:
    transcription = client.automatic_speech_recognition(
        f,
        model="openai/whisper-large-v3"
    )
print(transcription.text)

# Text to speech
audio = client.text_to_speech(
    "Hello, how are you today?",
    model="facebook/mms-tts-eng"
)
# Returns bytes
with open("output.wav", "wb") as f:
    f.write(audio)
```

### Embeddings

```python
# Single text
embedding = client.feature_extraction(
    "This is a sentence to embed",
    model="sentence-transformers/all-MiniLM-L6-v2"
)

# Multiple texts
embeddings = client.feature_extraction(
    ["First sentence", "Second sentence"],
    model="sentence-transformers/all-MiniLM-L6-v2"
)
```

### Other Tasks

```python
# Text classification
result = client.text_classification(
    "I love this product!",
    model="distilbert-base-uncased-finetuned-sst-2-english"
)
# [{"label": "POSITIVE", "score": 0.999}]

# Named entity recognition
entities = client.token_classification(
    "My name is John and I live in New York",
    model="dslim/bert-base-NER"
)

# Question answering
answer = client.question_answering(
    question="What is the capital of France?",
    context="France is a country in Europe. Its capital is Paris."
)

# Summarization
summary = client.summarization(
    "Long article text here...",
    model="facebook/bart-large-cnn"
)

# Translation
translation = client.translation(
    "Hello, how are you?",
    model="Helsinki-NLP/opus-mt-en-fr"
)

# Fill mask
predictions = client.fill_mask(
    "The capital of France is [MASK].",
    model="bert-base-uncased"
)
```

## TypeScript Client

### Setup

```typescript
import { InferenceClient } from "@huggingface/inference";

const client = new InferenceClient(process.env.HF_TOKEN);
```

### Text Generation

```typescript
// Simple generation
const result = await client.textGeneration({
  model: "meta-llama/Llama-3.1-8B-Instruct",
  inputs: "The answer to life is",
  parameters: { max_new_tokens: 100 },
});
console.log(result.generated_text);

// Chat completion
const response = await client.chatCompletion({
  model: "meta-llama/Llama-3.1-8B-Instruct",
  messages: [{ role: "user", content: "Hello!" }],
  max_tokens: 100,
});
console.log(response.choices[0].message.content);
```

### Streaming

```typescript
// Stream text
for await (const chunk of client.textGenerationStream({
  model: "meta-llama/Llama-3.1-8B-Instruct",
  inputs: "Write a story",
  parameters: { max_new_tokens: 500 },
})) {
  process.stdout.write(chunk.token.text);
}

// Stream chat
for await (const chunk of client.chatCompletionStream({
  model: "meta-llama/Llama-3.1-8B-Instruct",
  messages: [{ role: "user", content: "Tell me a joke" }],
})) {
  if (chunk.choices[0]?.delta?.content) {
    process.stdout.write(chunk.choices[0].delta.content);
  }
}
```

### Image Generation

```typescript
const image = await client.textToImage({
  model: "black-forest-labs/FLUX.1-schnell",
  inputs: "A beautiful sunset",
  provider: "fal-ai",
});
// image is a Blob

// Save to file (Node.js)
import { writeFile } from "fs/promises";
const buffer = Buffer.from(await image.arrayBuffer());
await writeFile("output.png", buffer);
```

## Available Providers

| Provider | Strengths |
|----------|-----------|
| `hf-inference` | Hugging Face native, wide model support |
| `fal-ai` | Fast image generation |
| `replicate` | Diverse model catalog |
| `together` | LLM specialization |
| `fireworks-ai` | High-performance inference |
| `nebius` | European infrastructure |
| `nscale` | Scalable inference |

### Provider-Specific Configuration

```python
# Use auto for automatic selection and failover
client = InferenceClient(provider="auto")

# Specify provider for consistent behavior
client = InferenceClient(provider="fal-ai")
image = client.text_to_image("...", model="black-forest-labs/FLUX.1-schnell")
```

## Error Handling

```python
from huggingface_hub import InferenceClient
from huggingface_hub.errors import HfHubHTTPError

client = InferenceClient(api_key=os.environ["HF_TOKEN"])

try:
    result = client.text_generation("test", model="nonexistent/model")
except HfHubHTTPError as e:
    print(f"Error: {e}")
    print(f"Status code: {e.response.status_code}")
```

## Rate Limits and Billing

- Rate limits depend on your subscription tier
- Check usage at: https://huggingface.co/settings/billing
- Provider-specific limits may apply
- Use `provider="auto"` for automatic failover

## Async Support

```python
import asyncio
from huggingface_hub import AsyncInferenceClient

async def main():
    client = AsyncInferenceClient(api_key=os.environ["HF_TOKEN"])

    result = await client.text_generation(
        "Hello world",
        model="meta-llama/Llama-3.1-8B-Instruct"
    )
    print(result)

asyncio.run(main())
```

## Finding Supported Models

Browse models with Inference Provider support:

```
https://huggingface.co/models?inference_provider=fal-ai,hf-inference,replicate,together
```

Or filter by task:

```
https://huggingface.co/models?pipeline_tag=text-to-image&inference_provider=fal-ai
```
