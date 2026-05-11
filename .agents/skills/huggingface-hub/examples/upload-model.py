"""
Upload Model to Hub Example

Complete examples of uploading PyTorch models to Hugging Face Hub
using PyTorchModelHubMixin and direct upload methods.

Requirements:
    pip install huggingface_hub torch safetensors transformers
"""

import os
import json
import torch
import torch.nn as nn
from huggingface_hub import (
    PyTorchModelHubMixin,
    HfApi,
    upload_file,
    upload_folder,
    create_repo,
)


# =============================================================================
# Method 1: PyTorchModelHubMixin (Recommended for PyTorch models)
# =============================================================================

class TextClassifier(
    nn.Module,
    PyTorchModelHubMixin,
    # Metadata for model card (optional but recommended)
    repo_url="https://huggingface.co/your-username/text-classifier",
    pipeline_tag="text-classification",
    license="mit",
    tags=["pytorch", "text-classification", "sentiment"],
):
    """
    A simple text classification model.

    Inheriting from PyTorchModelHubMixin adds:
    - from_pretrained() class method
    - save_pretrained() instance method
    - push_to_hub() instance method
    """

    def __init__(
        self,
        vocab_size: int = 30000,
        embedding_dim: int = 128,
        hidden_dim: int = 256,
        num_classes: int = 2,
        dropout: float = 0.1,
    ):
        super().__init__()

        # All init args are saved to config.json automatically
        self.vocab_size = vocab_size
        self.embedding_dim = embedding_dim
        self.hidden_dim = hidden_dim
        self.num_classes = num_classes

        # Model layers
        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        self.lstm = nn.LSTM(
            embedding_dim,
            hidden_dim,
            batch_first=True,
            bidirectional=True,
        )
        self.dropout = nn.Dropout(dropout)
        self.classifier = nn.Linear(hidden_dim * 2, num_classes)

    def forward(self, input_ids: torch.Tensor) -> torch.Tensor:
        """Forward pass."""
        embedded = self.embedding(input_ids)
        lstm_out, _ = self.lstm(embedded)
        pooled = lstm_out.mean(dim=1)
        dropped = self.dropout(pooled)
        return self.classifier(dropped)


def example_pytorch_mixin():
    """Example using PyTorchModelHubMixin."""

    # Create model
    model = TextClassifier(
        vocab_size=30000,
        embedding_dim=128,
        hidden_dim=256,
        num_classes=2,
    )

    # Train your model...
    # model = train(model, data)

    # Save locally (creates config.json + model.safetensors)
    model.save_pretrained("./my-text-classifier")
    print("Model saved to ./my-text-classifier")

    # Push to Hub
    model.push_to_hub(
        "your-username/my-text-classifier",
        commit_message="Upload trained model",
    )
    print("Model pushed to Hub!")

    # Load from Hub
    loaded_model = TextClassifier.from_pretrained(
        "your-username/my-text-classifier"
    )
    print(f"Loaded model with {loaded_model.num_classes} classes")

    # Load from local
    local_model = TextClassifier.from_pretrained("./my-text-classifier")
    print("Loaded model from local directory")


# =============================================================================
# Method 2: Direct Upload with HfApi
# =============================================================================

def example_direct_upload():
    """Example using direct file uploads."""

    # Initialize API
    api = HfApi()

    # Create repository
    repo_id = "your-username/my-model"
    create_repo(
        repo_id=repo_id,
        repo_type="model",
        exist_ok=True,  # Don't error if exists
    )
    print(f"Created repository: {repo_id}")

    # Create a simple model
    model = nn.Sequential(
        nn.Linear(10, 64),
        nn.ReLU(),
        nn.Linear(64, 2),
    )

    # Save model weights
    torch.save(model.state_dict(), "pytorch_model.bin")

    # Or use safetensors (recommended)
    from safetensors.torch import save_file
    save_file(model.state_dict(), "model.safetensors")

    # Create config
    config = {
        "model_type": "simple_classifier",
        "input_dim": 10,
        "hidden_dim": 64,
        "output_dim": 2,
    }
    with open("config.json", "w") as f:
        json.dump(config, f, indent=2)

    # Upload individual files
    upload_file(
        path_or_fileobj="model.safetensors",
        path_in_repo="model.safetensors",
        repo_id=repo_id,
        commit_message="Add model weights",
    )

    upload_file(
        path_or_fileobj="config.json",
        path_in_repo="config.json",
        repo_id=repo_id,
        commit_message="Add config",
    )

    print("Files uploaded!")

    # Or upload entire folder
    # upload_folder(
    #     folder_path="./model_dir",
    #     repo_id=repo_id,
    #     commit_message="Upload model",
    # )


# =============================================================================
# Method 3: Upload with Model Card
# =============================================================================

MODEL_CARD_TEMPLATE = """---
language:
  - en
license: mit
library_name: pytorch
pipeline_tag: text-classification
tags:
  - sentiment-analysis
  - pytorch
datasets:
  - stanfordnlp/imdb
metrics:
  - accuracy
  - f1
base_model: null
model-index:
  - name: {model_name}
    results:
      - task:
          type: text-classification
        dataset:
          name: IMDB
          type: stanfordnlp/imdb
        metrics:
          - name: Accuracy
            type: accuracy
            value: {accuracy}
---

# {model_name}

## Model Description

A text classification model for sentiment analysis.

## Intended Uses

- Sentiment analysis of movie reviews
- General positive/negative text classification

## Training

- **Dataset:** IMDB movie reviews
- **Epochs:** 10
- **Batch Size:** 32
- **Learning Rate:** 2e-5

## Evaluation Results

| Metric | Value |
|--------|-------|
| Accuracy | {accuracy} |
| F1 Score | {f1_score} |

## Usage

```python
from huggingface_hub import PyTorchModelHubMixin
import torch.nn as nn

class TextClassifier(nn.Module, PyTorchModelHubMixin):
    # ... model definition ...

model = TextClassifier.from_pretrained("{repo_id}")
```

## Limitations

- Trained only on English movie reviews
- May not generalize well to other domains

## Citation

```bibtex
@misc{{{model_name}}},
  author = {{Your Name}},
  title = {{{model_name}}},
  year = {{2024}},
  publisher = {{Hugging Face}},
  url = {{https://huggingface.co/{repo_id}}}
}}
```
"""


def example_with_model_card():
    """Example uploading model with a complete model card."""

    repo_id = "your-username/sentiment-classifier"
    api = HfApi()

    # Create repo
    create_repo(repo_id=repo_id, exist_ok=True)

    # Create model
    model = TextClassifier(num_classes=2)

    # Save model
    model.save_pretrained("./sentiment-classifier")

    # Create model card
    model_card = MODEL_CARD_TEMPLATE.format(
        model_name="Sentiment Classifier",
        repo_id=repo_id,
        accuracy=0.92,
        f1_score=0.91,
    )

    with open("./sentiment-classifier/README.md", "w") as f:
        f.write(model_card)

    # Upload everything
    upload_folder(
        folder_path="./sentiment-classifier",
        repo_id=repo_id,
        commit_message="Upload model with documentation",
    )

    print(f"Model uploaded to: https://huggingface.co/{repo_id}")


# =============================================================================
# Method 4: Transformers Integration
# =============================================================================

def example_transformers_upload():
    """Example uploading a transformers model."""
    from transformers import AutoModelForSequenceClassification, AutoTokenizer

    # Load pre-trained model
    model = AutoModelForSequenceClassification.from_pretrained(
        "distilbert-base-uncased",
        num_labels=2,
    )
    tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")

    # Fine-tune your model...
    # trainer.train()

    # Push to Hub
    model.push_to_hub("your-username/fine-tuned-distilbert")
    tokenizer.push_to_hub("your-username/fine-tuned-distilbert")

    print("Transformers model uploaded!")


# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":
    # Ensure HF_TOKEN is set
    if not os.environ.get("HF_TOKEN"):
        print("Warning: HF_TOKEN not set. Set it with:")
        print("  export HF_TOKEN='your-token-here'")
        print("  # or")
        print("  huggingface-cli login")

    # Run examples
    print("\n=== PyTorchModelHubMixin Example ===")
    # example_pytorch_mixin()

    print("\n=== Direct Upload Example ===")
    # example_direct_upload()

    print("\n=== Model Card Example ===")
    # example_with_model_card()

    print("\n=== Transformers Example ===")
    # example_transformers_upload()

    print("\nUncomment the example you want to run!")
