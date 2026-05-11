"""
Gradio Image Classifier Space Example

A complete example of an image classification Space using
a Hugging Face model with Gradio interface.

Requirements (requirements.txt):
    transformers
    torch
    Pillow

README.md header:
---
title: Image Classifier
emoji: 🖼️
colorFrom: green
colorTo: blue
sdk: gradio
sdk_version: 5.0.0
app_file: app.py
pinned: false
models:
  - google/vit-base-patch16-224
tags:
  - image-classification
  - vision
---
"""

import gradio as gr
from transformers import pipeline
from PIL import Image

# Initialize the image classification pipeline
# Model is downloaded and cached on first run
classifier = pipeline(
    task="image-classification",
    model="google/vit-base-patch16-224"
)


def classify_image(image: Image.Image) -> dict[str, float]:
    """
    Classify an image and return top predictions with confidence scores.

    Args:
        image: PIL Image to classify

    Returns:
        Dictionary mapping class labels to confidence scores
    """
    if image is None:
        return {}

    # Run classification
    predictions = classifier(image)

    # Format as {label: score} for gr.Label component
    return {pred["label"]: pred["score"] for pred in predictions}


def classify_with_details(image: Image.Image) -> tuple[dict[str, float], str]:
    """
    Classify image and provide detailed text output.

    Args:
        image: PIL Image to classify

    Returns:
        Tuple of (label dict, detailed text)
    """
    if image is None:
        return {}, "Please upload an image."

    predictions = classifier(image)

    # Format for label component
    label_dict = {pred["label"]: pred["score"] for pred in predictions}

    # Format detailed text
    details = "## Classification Results\n\n"
    for i, pred in enumerate(predictions, 1):
        confidence = pred["score"] * 100
        details += f"{i}. **{pred['label']}**: {confidence:.2f}%\n"

    return label_dict, details


# Simple interface
simple_demo = gr.Interface(
    fn=classify_image,
    inputs=gr.Image(
        type="pil",
        label="Upload Image",
        sources=["upload", "webcam", "clipboard"]
    ),
    outputs=gr.Label(
        num_top_classes=5,
        label="Predictions"
    ),
    title="🖼️ Image Classifier",
    description="Upload an image to classify it using Vision Transformer (ViT).",
    examples=[
        # Add example images here if available
        # ["examples/cat.jpg"],
        # ["examples/dog.jpg"],
    ],
    cache_examples=False,
    allow_flagging="never"
)


# Advanced interface with Blocks
def create_advanced_demo():
    """Create a more advanced demo with additional features."""

    with gr.Blocks(title="Advanced Image Classifier") as demo:
        gr.Markdown("""
        # 🖼️ Advanced Image Classifier

        Classify images using Google's Vision Transformer (ViT) model.
        Upload an image or use your webcam to get started.
        """)

        with gr.Row():
            with gr.Column(scale=1):
                image_input = gr.Image(
                    type="pil",
                    label="Input Image",
                    sources=["upload", "webcam"]
                )
                classify_btn = gr.Button("Classify", variant="primary")
                clear_btn = gr.Button("Clear")

            with gr.Column(scale=1):
                label_output = gr.Label(
                    num_top_classes=5,
                    label="Top 5 Predictions"
                )
                details_output = gr.Markdown(label="Details")

        # Event handlers
        classify_btn.click(
            fn=classify_with_details,
            inputs=image_input,
            outputs=[label_output, details_output]
        )

        # Auto-classify on image upload
        image_input.change(
            fn=classify_with_details,
            inputs=image_input,
            outputs=[label_output, details_output]
        )

        # Clear outputs
        clear_btn.click(
            fn=lambda: (None, {}, ""),
            outputs=[image_input, label_output, details_output]
        )

        gr.Markdown("""
        ---
        ### About

        This demo uses the [google/vit-base-patch16-224](https://huggingface.co/google/vit-base-patch16-224)
        model, a Vision Transformer trained on ImageNet-21k and fine-tuned on ImageNet-1k.

        **Model Details:**
        - Architecture: Vision Transformer (ViT)
        - Input Size: 224x224 pixels
        - Classes: 1,000 ImageNet categories
        """)

    return demo


# Create the advanced demo
advanced_demo = create_advanced_demo()

# Launch the app
if __name__ == "__main__":
    # Use simple_demo for basic interface, advanced_demo for full features
    advanced_demo.launch()
