# Models Reference

Complete guide for model repositories on Hugging Face Hub.

## Model Repository Structure

```
my-model/
├── README.md              # Model card with metadata
├── config.json            # Model configuration
├── model.safetensors      # Model weights (preferred)
├── tokenizer.json         # Tokenizer (if applicable)
├── tokenizer_config.json  # Tokenizer configuration
├── vocab.txt              # Vocabulary file
└── special_tokens_map.json
```

## Model Card (README.md)

### Basic Structure

```yaml
---
language:
  - en
license: apache-2.0
library_name: transformers
pipeline_tag: text-classification
tags:
  - nlp
  - sentiment
---

# Model Card for MyModel

## Model Description

Brief description of what the model does...

## Intended Uses & Limitations

What the model should and shouldn't be used for...

## Training

Information about training data, procedure, hyperparameters...

## Evaluation

Model performance metrics and benchmarks...

## Citation

How to cite this model...
```

### Metadata Fields

#### Required/Recommended

| Field | Type | Description |
|-------|------|-------------|
| `license` | string | License identifier (e.g., `mit`, `apache-2.0`) |
| `pipeline_tag` | string | Task type for widget |
| `library_name` | string | Framework (e.g., `transformers`, `pytorch`) |

#### Language & Datasets

```yaml
language:
  - en
  - fr
  - multilingual  # For multilingual models

datasets:
  - stanfordnlp/imdb
  - squad
  - custom_dataset  # Non-Hub datasets
```

#### Tags

```yaml
tags:
  - text-classification
  - sentiment-analysis
  - bert
  - fine-tuned
```

#### Base Model

```yaml
# Fine-tuned model
base_model: bert-base-uncased

# Quantized model
base_model: meta-llama/Llama-3.1-8B
base_model_relation: quantized

# Merged model
base_model:
  - model-1
  - model-2
base_model_relation: merge
```

#### Metrics & Evaluation

```yaml
metrics:
  - accuracy
  - f1
  - rouge

model-index:
  - name: MyModel
    results:
      - task:
          type: text-classification
        dataset:
          name: SST-2
          type: sst2
        metrics:
          - name: Accuracy
            type: accuracy
            value: 0.92
```

#### New Version Pointer

```yaml
new_version: user/my-model-v2
```

### Pipeline Tags

| Tag | Description |
|-----|-------------|
| `text-generation` | Generate text |
| `text-classification` | Classify text |
| `token-classification` | NER, POS tagging |
| `question-answering` | Answer questions |
| `summarization` | Summarize text |
| `translation` | Translate between languages |
| `fill-mask` | Fill masked tokens |
| `text2text-generation` | Text-to-text |
| `image-classification` | Classify images |
| `object-detection` | Detect objects |
| `image-segmentation` | Segment images |
| `image-to-text` | Image captioning |
| `text-to-image` | Generate images |
| `automatic-speech-recognition` | Speech to text |
| `text-to-speech` | Text to speech |
| `audio-classification` | Classify audio |
| `feature-extraction` | Embeddings |
| `sentence-similarity` | Compare sentences |
| `zero-shot-classification` | Classify without training |

### Licenses

Common license identifiers:

| License | Identifier |
|---------|------------|
| Apache 2.0 | `apache-2.0` |
| MIT | `mit` |
| GPL 3.0 | `gpl-3.0` |
| CC BY 4.0 | `cc-by-4.0` |
| CC BY-NC 4.0 | `cc-by-nc-4.0` |
| Llama 3 | `llama3` |
| OpenRAIL | `openrail` |

Custom license:
```yaml
license: other
license_name: my-custom-license
license_link: https://example.com/license
# or
license_link: LICENSE  # File in repo
```

## Uploading Models

### Using transformers

```python
from transformers import AutoModel, AutoTokenizer

# Load or train model
model = AutoModel.from_pretrained("bert-base-uncased")
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

# Push to Hub
model.push_to_hub("user/my-fine-tuned-bert")
tokenizer.push_to_hub("user/my-fine-tuned-bert")
```

### Using PyTorchModelHubMixin

```python
import torch.nn as nn
from huggingface_hub import PyTorchModelHubMixin

class MyModel(nn.Module, PyTorchModelHubMixin,
              repo_url="https://huggingface.co/user/my-model",
              pipeline_tag="text-classification",
              license="mit"):
    def __init__(self, hidden_size: int = 256):
        super().__init__()
        self.linear = nn.Linear(hidden_size, 10)

    def forward(self, x):
        return self.linear(x)

model = MyModel(hidden_size=512)
model.push_to_hub("user/my-model")
```

### Using huggingface_hub

```python
from huggingface_hub import HfApi, upload_folder

api = HfApi()

# Create repo
api.create_repo(repo_id="user/my-model", repo_type="model")

# Upload folder
upload_folder(
    folder_path="./my_model_dir",
    repo_id="user/my-model"
)

# Or upload individual files
api.upload_file(
    path_or_fileobj="model.safetensors",
    path_in_repo="model.safetensors",
    repo_id="user/my-model"
)
```

### Web Interface

1. Go to https://huggingface.co/new
2. Create model repository
3. Upload files via "Add file" button
4. Edit model card via web editor

## Loading Models

### From transformers

```python
from transformers import AutoModel, AutoTokenizer

model = AutoModel.from_pretrained("user/my-model")
tokenizer = AutoTokenizer.from_pretrained("user/my-model")

# Private model
model = AutoModel.from_pretrained(
    "user/private-model",
    token="hf_xxx"
)

# Specific revision
model = AutoModel.from_pretrained(
    "user/my-model",
    revision="v1.0"
)
```

### From huggingface_hub

```python
from huggingface_hub import hf_hub_download, snapshot_download

# Single file
config_path = hf_hub_download(
    repo_id="bert-base-uncased",
    filename="config.json"
)

# Entire repository
model_dir = snapshot_download(repo_id="bert-base-uncased")
```

## Safetensors Format

Preferred format for model weights:

```python
from safetensors.torch import save_file, load_file

# Save
tensors = {"weight": model.weight, "bias": model.bias}
save_file(tensors, "model.safetensors")

# Load
tensors = load_file("model.safetensors")
```

Benefits:
- Faster loading (memory-mapped)
- Safe (no arbitrary code execution)
- Smaller file sizes

## Model Versioning

### Using Branches

```python
# Push to specific branch
model.push_to_hub("user/my-model", branch="v2")

# Load from branch
model = AutoModel.from_pretrained("user/my-model", revision="v2")
```

### Using Tags

```bash
git tag v1.0.0
git push origin v1.0.0
```

```python
model = AutoModel.from_pretrained("user/my-model", revision="v1.0.0")
```

## Private Models

```python
# Create private repo
api.create_repo(repo_id="user/private-model", private=True)

# Access private model
model = AutoModel.from_pretrained(
    "user/private-model",
    token=os.environ["HF_TOKEN"]
)
```

## Gated Models

For models requiring acceptance of terms:

1. Enable gating in repo settings
2. Users must accept terms before access
3. Access with token after acceptance

## Model Widgets

Automatic inference widgets based on `pipeline_tag`:

```yaml
pipeline_tag: text-classification
# Enables classification widget on model page
```

Custom widget examples:
```yaml
widget:
  - text: "I love this product!"
  - text: "This is terrible."
```

## Download Statistics

Models automatically track:
- Total downloads
- Downloads per file
- Download trends

View at: `https://huggingface.co/user/model/stats`

## Discussion & Community

Each model repo has:
- Discussions tab for Q&A
- Community tab for contributions
- Pull requests for changes

## Library Integration

Specify library for proper loading instructions:

```yaml
library_name: transformers  # or pytorch, tensorflow, jax, etc.
```

Supported libraries:
`transformers`, `diffusers`, `timm`, `sentence-transformers`,
`spacy`, `flair`, `allennlp`, `asteroid`, `espnet`, `fairseq`,
`keras`, `nemo`, `paddlenlp`, `peft`, `sklearn`, `speechbrain`,
`stanza`, `tensorboard`, and more.
