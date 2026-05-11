#!/bin/bash
# Hugging Face Inference Providers - Complete curl Examples
#
# Prerequisites:
#   export HF_TOKEN="hf_your_token_here"
#
# Get tokens at: https://huggingface.co/settings/tokens

# =============================================================================
# CHAT COMPLETION
# =============================================================================

# Basic chat completion
curl https://router.huggingface.co/v1/chat/completions \
  -H "Authorization: Bearer $HF_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "meta-llama/Llama-3.1-8B-Instruct",
    "messages": [
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": "What is the capital of France?"}
    ]
  }'

# Streaming chat completion
curl https://router.huggingface.co/v1/chat/completions \
  -H "Authorization: Bearer $HF_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "meta-llama/Llama-3.1-8B-Instruct",
    "messages": [{"role": "user", "content": "Tell me a short story"}],
    "stream": true,
    "max_tokens": 500
  }'

# With temperature and other parameters
curl https://router.huggingface.co/v1/chat/completions \
  -H "Authorization: Bearer $HF_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "meta-llama/Llama-3.1-8B-Instruct",
    "messages": [{"role": "user", "content": "Write a haiku about coding"}],
    "temperature": 0.7,
    "max_tokens": 100,
    "top_p": 0.9
  }'

# =============================================================================
# PROVIDER SELECTION
# =============================================================================

# Use fastest provider (highest throughput)
curl https://router.huggingface.co/v1/chat/completions \
  -H "Authorization: Bearer $HF_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "meta-llama/Llama-3.1-8B-Instruct:fastest",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'

# Use cheapest provider
curl https://router.huggingface.co/v1/chat/completions \
  -H "Authorization: Bearer $HF_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "meta-llama/Llama-3.1-8B-Instruct:cheapest",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'

# Use specific provider (e.g., Together, SambaNova, Groq)
curl https://router.huggingface.co/v1/chat/completions \
  -H "Authorization: Bearer $HF_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "meta-llama/Llama-3.1-8B-Instruct:together",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'

# =============================================================================
# VISION MODELS (VLM)
# =============================================================================

# Image understanding with URL
curl https://router.huggingface.co/v1/chat/completions \
  -H "Authorization: Bearer $HF_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "meta-llama/Llama-3.2-11B-Vision-Instruct",
    "messages": [
      {
        "role": "user",
        "content": [
          {"type": "text", "text": "What do you see in this image?"},
          {"type": "image_url", "image_url": {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/47/PNG_transparency_demonstration_1.png/280px-PNG_transparency_demonstration_1.png"}}
        ]
      }
    ]
  }'

# Image with base64 encoding
curl https://router.huggingface.co/v1/chat/completions \
  -H "Authorization: Bearer $HF_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "meta-llama/Llama-3.2-11B-Vision-Instruct",
    "messages": [
      {
        "role": "user",
        "content": [
          {"type": "text", "text": "Describe this image"},
          {"type": "image_url", "image_url": {"url": "data:image/png;base64,'"$(base64 -i image.png)"'"}}
        ]
      }
    ]
  }'

# =============================================================================
# TEXT TO IMAGE
# =============================================================================

# Generate image and save to file
curl https://router.huggingface.co/hf-inference/models/black-forest-labs/FLUX.1-schnell \
  -H "Authorization: Bearer $HF_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"inputs": "A serene mountain landscape at sunset, photorealistic"}' \
  --output generated_image.png

# =============================================================================
# EMBEDDINGS
# =============================================================================

# Generate embeddings for text
curl https://router.huggingface.co/hf-inference/models/sentence-transformers/all-MiniLM-L6-v2 \
  -H "Authorization: Bearer $HF_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"inputs": "The quick brown fox jumps over the lazy dog"}'

# =============================================================================
# SPEECH TO TEXT
# =============================================================================

# Transcribe audio file
curl https://router.huggingface.co/hf-inference/models/openai/whisper-large-v3 \
  -H "Authorization: Bearer $HF_TOKEN" \
  -H "Content-Type: audio/flac" \
  --data-binary @audio.flac

# =============================================================================
# HUB API - FILE OPERATIONS
# =============================================================================

# Download file from public repo
curl -L "https://huggingface.co/bert-base-uncased/resolve/main/config.json" \
  -o config.json

# Download file from private/gated repo
curl -L "https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct/resolve/main/config.json" \
  -H "Authorization: Bearer $HF_TOKEN" \
  -o config.json

# =============================================================================
# HUB API - MODEL INFO
# =============================================================================

# Get model info
curl "https://huggingface.co/api/models/bert-base-uncased"

# List models with inference providers
curl "https://huggingface.co/api/models?inference_provider=all&pipeline_tag=text-generation&limit=10"

# Get model providers
curl "https://huggingface.co/api/models/meta-llama/Llama-3.1-8B-Instruct?expand[]=inferenceProviderMapping"

# =============================================================================
# LIST AVAILABLE MODELS
# =============================================================================

# List all models available through inference providers
curl https://router.huggingface.co/v1/models \
  -H "Authorization: Bearer $HF_TOKEN"
