# Gradio Spaces Reference

Complete guide for building Gradio Spaces on Hugging Face Hub.

## Quick Start

### Minimal Space Structure

```
my-space/
├── README.md          # YAML config + description
├── app.py             # Gradio application
└── requirements.txt   # Python dependencies
```

### README.md

```yaml
---
title: My Gradio Space
emoji: 🚀
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: 5.0.0
app_file: app.py
pinned: false
---

# My Gradio Space

Description of your Space...
```

### app.py

```python
import gradio as gr

def greet(name):
    return f"Hello, {name}!"

demo = gr.Interface(fn=greet, inputs="text", outputs="text")
demo.launch()
```

### requirements.txt

```
transformers
torch
Pillow
```

## Common Patterns

### Image Classification

```python
import gradio as gr
from transformers import pipeline

classifier = pipeline("image-classification", model="google/vit-base-patch16-224")

def classify_image(image):
    predictions = classifier(image)
    return {p["label"]: p["score"] for p in predictions}

demo = gr.Interface(
    fn=classify_image,
    inputs=gr.Image(type="pil"),
    outputs=gr.Label(num_top_classes=5),
    title="Image Classifier",
    examples=["example1.jpg", "example2.jpg"]
)

if __name__ == "__main__":
    demo.launch()
```

### Text Generation

```python
import gradio as gr
from transformers import pipeline

generator = pipeline("text-generation", model="gpt2")

def generate_text(prompt, max_length=100):
    result = generator(prompt, max_length=max_length, num_return_sequences=1)
    return result[0]["generated_text"]

demo = gr.Interface(
    fn=generate_text,
    inputs=[
        gr.Textbox(label="Prompt", placeholder="Enter your prompt..."),
        gr.Slider(minimum=10, maximum=200, value=50, label="Max Length")
    ],
    outputs=gr.Textbox(label="Generated Text"),
    title="Text Generator"
)

demo.launch()
```

### Chat Interface

```python
import gradio as gr
from transformers import pipeline

chatbot = pipeline("text-generation", model="microsoft/DialoGPT-medium")

def chat(message, history):
    # Format conversation history
    conversation = ""
    for user_msg, bot_msg in history:
        conversation += f"User: {user_msg}\nBot: {bot_msg}\n"
    conversation += f"User: {message}\nBot:"

    response = chatbot(conversation, max_length=1000, pad_token_id=50256)
    bot_response = response[0]["generated_text"].split("Bot:")[-1].strip()

    return bot_response

demo = gr.ChatInterface(
    fn=chat,
    title="Chatbot",
    description="Chat with DialoGPT",
    examples=["Hello!", "Tell me a joke", "What's the weather like?"]
)

demo.launch()
```

### Using Inference Client

```python
import gradio as gr
import os
from huggingface_hub import InferenceClient

client = InferenceClient(api_key=os.environ.get("HF_TOKEN"))

def generate_image(prompt):
    image = client.text_to_image(
        prompt,
        model="black-forest-labs/FLUX.1-schnell"
    )
    return image

demo = gr.Interface(
    fn=generate_image,
    inputs=gr.Textbox(label="Prompt"),
    outputs=gr.Image(label="Generated Image"),
    title="Image Generator"
)

demo.launch()
```

## Gradio Components

### Input Components

```python
# Text
gr.Textbox(label="Input", placeholder="Type here...", lines=3)

# Number
gr.Number(label="Value", value=0, minimum=0, maximum=100)
gr.Slider(minimum=0, maximum=100, step=1, value=50, label="Slider")

# Choices
gr.Dropdown(choices=["Option 1", "Option 2"], label="Select")
gr.Radio(choices=["A", "B", "C"], label="Choose one")
gr.Checkbox(label="Enable feature")
gr.CheckboxGroup(choices=["A", "B", "C"], label="Select multiple")

# Files
gr.Image(type="pil", label="Upload Image")
gr.Image(type="filepath", label="Image Path")
gr.Audio(type="filepath", label="Upload Audio")
gr.Video(label="Upload Video")
gr.File(label="Upload File", file_types=[".pdf", ".txt"])

# Special
gr.ColorPicker(label="Choose color")
gr.Dataframe(label="Data")
```

### Output Components

```python
# Text
gr.Textbox(label="Output")
gr.Markdown()
gr.JSON()
gr.Code(language="python")

# Media
gr.Image(label="Output Image")
gr.Audio(label="Output Audio")
gr.Video(label="Output Video")

# Classification
gr.Label(num_top_classes=5)
gr.HighlightedText()

# Data
gr.Dataframe()
gr.Plot()  # matplotlib, plotly, etc.
```

## Layouts

### Blocks API

```python
import gradio as gr

with gr.Blocks() as demo:
    gr.Markdown("# My Application")

    with gr.Row():
        with gr.Column(scale=1):
            input_text = gr.Textbox(label="Input")
            submit_btn = gr.Button("Submit")

        with gr.Column(scale=2):
            output_text = gr.Textbox(label="Output")

    submit_btn.click(fn=process, inputs=input_text, outputs=output_text)

demo.launch()
```

### Tabs

```python
with gr.Blocks() as demo:
    with gr.Tabs():
        with gr.Tab("Text"):
            text_input = gr.Textbox()
            text_output = gr.Textbox()

        with gr.Tab("Image"):
            image_input = gr.Image()
            image_output = gr.Image()
```

### Accordion

```python
with gr.Blocks() as demo:
    with gr.Accordion("Advanced Options", open=False):
        temperature = gr.Slider(0, 1, value=0.7)
        max_tokens = gr.Slider(10, 500, value=100)
```

## State Management

### Session State

```python
import gradio as gr

def update_count(count):
    return count + 1, f"Count: {count + 1}"

with gr.Blocks() as demo:
    count = gr.State(0)  # Session-specific state
    output = gr.Textbox(value="Count: 0")
    btn = gr.Button("Increment")

    btn.click(update_count, inputs=count, outputs=[count, output])
```

### Global State

```python
# For data shared across all users (use carefully)
shared_data = {"total_calls": 0}

def process(text):
    shared_data["total_calls"] += 1
    return f"Call #{shared_data['total_calls']}: {text}"
```

## Events and Interactivity

```python
with gr.Blocks() as demo:
    text = gr.Textbox()
    output = gr.Textbox()

    # Button click
    btn = gr.Button("Submit")
    btn.click(fn=process, inputs=text, outputs=output)

    # On change
    text.change(fn=preview, inputs=text, outputs=output)

    # On submit (Enter key)
    text.submit(fn=process, inputs=text, outputs=output)

    # Chained events
    btn.click(step1, text, output).then(step2, output, output)
```

## Streaming

```python
import gradio as gr

def stream_text(prompt):
    response = ""
    for word in prompt.split():
        response += word + " "
        yield response

demo = gr.Interface(
    fn=stream_text,
    inputs="text",
    outputs="text",
    live=True  # Enable streaming
)
```

## Examples

```python
demo = gr.Interface(
    fn=process,
    inputs=["text", "image"],
    outputs="text",
    examples=[
        ["Hello world", "example1.jpg"],
        ["Test input", "example2.jpg"],
    ],
    cache_examples=True  # Pre-compute results
)
```

## Authentication

### HF OAuth

```yaml
---
hf_oauth: true
hf_oauth_scopes:
  - read-repos
  - write-repos
---
```

```python
import gradio as gr

def greet(profile: gr.OAuthProfile | None):
    if profile is None:
        return "Please log in"
    return f"Hello, {profile.name}!"

with gr.Blocks() as demo:
    login_btn = gr.LoginButton()
    output = gr.Textbox()

    demo.load(greet, outputs=output)
```

### Basic Auth

```python
demo.launch(auth=("username", "password"))

# Or multiple users
demo.launch(auth=[("user1", "pass1"), ("user2", "pass2")])

# Or function
def check_auth(username, password):
    return username == "admin" and password == "secret"

demo.launch(auth=check_auth)
```

## Environment Variables and Secrets

### Using Secrets

Set secrets in Space Settings, access in code:

```python
import os

HF_TOKEN = os.environ.get("HF_TOKEN")
API_KEY = os.environ.get("MY_API_KEY")
```

### Required Secrets

```yaml
---
secrets:
  - HF_TOKEN
  - OPENAI_API_KEY
---
```

## Flagging

```python
demo = gr.Interface(
    fn=process,
    inputs="text",
    outputs="text",
    flagging_mode="manual",  # or "auto", "never"
    flagging_dir="flagged_data"
)
```

## Deployment Tips

### Preload Models

```yaml
---
preload_from_hub:
  - bert-base-uncased config.json,pytorch_model.bin
  - user/model
---
```

### Hardware Selection

```yaml
---
suggested_hardware: t4-small
---
```

### Full Width Layout

```yaml
---
fullWidth: true
---
```

### Mini Header

```yaml
---
header: mini
---
```

## Error Handling

```python
import gradio as gr

def safe_process(text):
    try:
        result = risky_operation(text)
        return result
    except Exception as e:
        raise gr.Error(f"Processing failed: {str(e)}")

# Or with warnings
def process_with_warning(text):
    if len(text) < 5:
        gr.Warning("Input is very short, results may be poor")
    return process(text)
```

## Custom CSS

```python
css = """
.gradio-container {
    max-width: 800px !important;
}
#custom-button {
    background-color: #ff6b6b !important;
}
"""

with gr.Blocks(css=css) as demo:
    gr.Button("Styled", elem_id="custom-button")
```

## API Access

Every Gradio Space automatically gets an API:

```python
from gradio_client import Client

client = Client("user/my-space")
result = client.predict("Hello", api_name="/predict")
```

Disable API:

```python
demo.launch(show_api=False)
```
