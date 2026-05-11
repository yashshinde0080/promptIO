# JavaScript SDK Reference

Reference for `@huggingface/hub` and `@huggingface/inference` packages.

## Installation

```bash
# Hub operations (download, upload, repo management)
npm install @huggingface/hub

# Inference client
npm install @huggingface/inference

# Both
npm install @huggingface/hub @huggingface/inference
```

## Authentication

```typescript
// Environment variable (recommended)
// Set HF_TOKEN in your environment

// Or pass directly
const HF_TOKEN = process.env.HF_TOKEN;
```

## @huggingface/hub

### Download Files

```typescript
import { downloadFile } from "@huggingface/hub";

// Download single file
const response = await downloadFile({
  repo: "bert-base-uncased",
  path: "config.json",
  credentials: { accessToken: HF_TOKEN }, // optional for public repos
});

const content = await response.text();
// or
const json = await response.json();
```

### List Repository Files

```typescript
import { listFiles } from "@huggingface/hub";

// List all files
for await (const file of listFiles({ repo: "bert-base-uncased" })) {
  console.log(file.path, file.size);
}

// With credentials for private repos
for await (const file of listFiles({
  repo: "user/private-model",
  credentials: { accessToken: HF_TOKEN },
})) {
  console.log(file.path);
}
```

### Upload Files

```typescript
import { uploadFile, uploadFiles } from "@huggingface/hub";

// Upload single file
await uploadFile({
  repo: "user/my-model",
  credentials: { accessToken: HF_TOKEN },
  file: {
    path: "config.json",
    content: new Blob([JSON.stringify({ model_type: "bert" })]),
  },
  commitTitle: "Add config",
});

// Upload multiple files
await uploadFiles({
  repo: "user/my-model",
  credentials: { accessToken: HF_TOKEN },
  files: [
    { path: "config.json", content: new Blob([configJson]) },
    { path: "vocab.txt", content: new Blob([vocabContent]) },
  ],
  commitTitle: "Add model files",
});

// Upload from file input (browser)
const fileInput = document.querySelector('input[type="file"]');
await uploadFile({
  repo: "user/my-model",
  credentials: { accessToken: HF_TOKEN },
  file: {
    path: fileInput.files[0].name,
    content: fileInput.files[0],
  },
});
```

### Repository Operations

```typescript
import { createRepo, deleteRepo, RepoType } from "@huggingface/hub";

// Create repository
await createRepo({
  repo: "user/new-model",
  credentials: { accessToken: HF_TOKEN },
  repoType: "model", // "model" | "dataset" | "space"
  private: false,
});

// Create Space
await createRepo({
  repo: "user/new-space",
  credentials: { accessToken: HF_TOKEN },
  repoType: "space",
  spaceSdk: "gradio",
});

// Delete repository
await deleteRepo({
  repo: "user/old-model",
  credentials: { accessToken: HF_TOKEN },
});
```

### Get Repository Info

```typescript
import { repoInfo } from "@huggingface/hub";

const info = await repoInfo({
  repo: "bert-base-uncased",
  credentials: { accessToken: HF_TOKEN }, // optional
});

console.log(info.sha);       // Latest commit SHA
console.log(info.private);   // Is private?
console.log(info.siblings);  // File list
```

### Commit Operations

```typescript
import { commit } from "@huggingface/hub";

// Create a commit with multiple operations
await commit({
  repo: "user/my-model",
  credentials: { accessToken: HF_TOKEN },
  title: "Update model",
  operations: [
    {
      operation: "addOrUpdate",
      path: "config.json",
      content: new Blob([JSON.stringify(config)]),
    },
    {
      operation: "delete",
      path: "old_file.txt",
    },
  ],
});
```

## @huggingface/inference

### InferenceClient Setup

```typescript
import { InferenceClient } from "@huggingface/inference";

const client = new InferenceClient(process.env.HF_TOKEN);

// Or with specific options
const client = new InferenceClient({
  accessToken: process.env.HF_TOKEN,
});
```

### Text Generation

```typescript
const client = new InferenceClient(process.env.HF_TOKEN);

// Simple text generation
const result = await client.textGeneration({
  model: "gpt2",
  inputs: "The answer to the universe is",
  parameters: {
    max_new_tokens: 50,
    temperature: 0.7,
  },
});
console.log(result.generated_text);

// Chat completion
const response = await client.chatCompletion({
  model: "meta-llama/Llama-3.1-8B-Instruct",
  messages: [
    { role: "user", content: "What is the capital of France?" },
  ],
  max_tokens: 100,
});
console.log(response.choices[0].message.content);
```

### Streaming

```typescript
// Stream text generation
for await (const chunk of client.textGenerationStream({
  model: "meta-llama/Llama-3.1-8B-Instruct",
  inputs: "Write a poem about",
  parameters: { max_new_tokens: 100 },
})) {
  process.stdout.write(chunk.token.text);
}

// Stream chat completion
for await (const chunk of client.chatCompletionStream({
  model: "meta-llama/Llama-3.1-8B-Instruct",
  messages: [{ role: "user", content: "Tell me a story" }],
})) {
  if (chunk.choices[0]?.delta?.content) {
    process.stdout.write(chunk.choices[0].delta.content);
  }
}
```

### Image Generation

```typescript
// Text to image
const image = await client.textToImage({
  model: "black-forest-labs/FLUX.1-schnell",
  inputs: "A beautiful sunset over mountains",
  parameters: {
    num_inference_steps: 4,
  },
});
// image is a Blob

// Save to file (Node.js)
import { writeFile } from "fs/promises";
const buffer = Buffer.from(await image.arrayBuffer());
await writeFile("output.png", buffer);

// Display in browser
const url = URL.createObjectURL(image);
document.querySelector("img").src = url;
```

### Image Analysis

```typescript
// Image classification
const result = await client.imageClassification({
  model: "google/vit-base-patch16-224",
  data: imageBlob,
});
// [{ label: "cat", score: 0.95 }, ...]

// Object detection
const detections = await client.objectDetection({
  model: "facebook/detr-resnet-50",
  data: imageBlob,
});
// [{ label: "cat", score: 0.98, box: { xmin, ymin, xmax, ymax } }, ...]

// Image to text (captioning)
const caption = await client.imageToText({
  model: "nlpconnect/vit-gpt2-image-captioning",
  data: imageBlob,
});
```

### Audio Tasks

```typescript
// Speech recognition
const transcription = await client.automaticSpeechRecognition({
  model: "openai/whisper-large-v3",
  data: audioBlob,
});
console.log(transcription.text);

// Text to speech
const audio = await client.textToSpeech({
  model: "facebook/mms-tts-eng",
  inputs: "Hello, how are you?",
});
// audio is a Blob
```

### Embeddings

```typescript
// Text embeddings
const embeddings = await client.featureExtraction({
  model: "sentence-transformers/all-MiniLM-L6-v2",
  inputs: "This is a sentence to embed",
});
// Returns embedding vector

// Multiple texts
const embeddings = await client.featureExtraction({
  model: "sentence-transformers/all-MiniLM-L6-v2",
  inputs: ["First sentence", "Second sentence"],
});
```

### Using Inference Providers

```typescript
// Auto-select provider
const image = await client.textToImage({
  model: "black-forest-labs/FLUX.1-schnell",
  inputs: "Astronaut riding a horse",
  provider: "auto", // default
});

// Specific provider
const image = await client.textToImage({
  model: "black-forest-labs/FLUX.1-schnell",
  inputs: "Astronaut riding a horse",
  provider: "fal-ai",
});

// Other providers: "replicate", "together", "fireworks-ai", etc.
```

## Transformers.js

Run models directly in browser/Node.js:

```bash
npm install @xenova/transformers
```

### Basic Usage

```typescript
import { pipeline } from "@xenova/transformers";

// Text classification
const classifier = await pipeline("sentiment-analysis");
const result = await classifier("I love this product!");
// [{ label: "POSITIVE", score: 0.999 }]

// Text generation
const generator = await pipeline("text-generation", "Xenova/gpt2");
const output = await generator("The quick brown fox", {
  max_new_tokens: 20,
});

// Feature extraction (embeddings)
const extractor = await pipeline(
  "feature-extraction",
  "Xenova/all-MiniLM-L6-v2"
);
const embeddings = await extractor("This is a sentence");
```

### Supported Tasks

```typescript
// NLP
const classifier = await pipeline("text-classification");
const ner = await pipeline("token-classification");
const qa = await pipeline("question-answering");
const summarizer = await pipeline("summarization");
const translator = await pipeline("translation");
const generator = await pipeline("text-generation");
const fillMask = await pipeline("fill-mask");

// Vision
const imageClassifier = await pipeline("image-classification");
const objectDetector = await pipeline("object-detection");
const segmenter = await pipeline("image-segmentation");

// Audio
const asr = await pipeline("automatic-speech-recognition");

// Multimodal
const vqa = await pipeline("visual-question-answering");
```

### Loading Models

```typescript
// From Hub
const classifier = await pipeline(
  "text-classification",
  "distilbert-base-uncased-finetuned-sst-2-english"
);

// Quantized model (smaller, faster)
const classifier = await pipeline("text-classification", "Xenova/bert-base-uncased", {
  quantized: true,
});

// With progress callback
const classifier = await pipeline("text-classification", "model-name", {
  progress_callback: (progress) => {
    console.log(`Loading: ${progress.progress}%`);
  },
});
```

## Error Handling

```typescript
import { HfInferenceError } from "@huggingface/inference";

try {
  const result = await client.textGeneration({
    model: "nonexistent/model",
    inputs: "test",
  });
} catch (error) {
  if (error instanceof HfInferenceError) {
    console.log("Inference error:", error.message);
    console.log("Status:", error.statusCode);
  }
}
```

## TypeScript Types

```typescript
import type {
  RepoId,
  Credentials,
  CommitOperation,
  TextGenerationOutput,
  ChatCompletionOutput,
  ImageClassificationOutput,
} from "@huggingface/hub";
```
