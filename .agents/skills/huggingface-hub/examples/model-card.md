---
language:
  - en
license: apache-2.0
library_name: transformers
pipeline_tag: text-classification
tags:
  - sentiment-analysis
  - bert
  - fine-tuned
  - pytorch
datasets:
  - stanfordnlp/imdb
  - rotten_tomatoes
base_model: bert-base-uncased
metrics:
  - accuracy
  - f1
  - precision
  - recall
model-index:
  - name: sentiment-bert
    results:
      - task:
          type: text-classification
          name: Text Classification
        dataset:
          name: IMDB
          type: stanfordnlp/imdb
          split: test
        metrics:
          - name: Accuracy
            type: accuracy
            value: 0.9234
          - name: F1
            type: f1
            value: 0.9215
      - task:
          type: text-classification
          name: Text Classification
        dataset:
          name: Rotten Tomatoes
          type: rotten_tomatoes
          split: test
        metrics:
          - name: Accuracy
            type: accuracy
            value: 0.8876
widget:
  - text: "I absolutely loved this movie! The acting was superb."
    example_title: Positive Review
  - text: "This was a waste of time. Terrible plot and bad acting."
    example_title: Negative Review
  - text: "An interesting concept but the execution was lacking."
    example_title: Mixed Review
inference:
  parameters:
    temperature: 1.0
co2_eq_emissions:
  emissions: 12.5
  source: CodeCarbon
  training_type: fine-tuning
  geographical_location: US-West
  hardware_used: NVIDIA A100 40GB
---

# Sentiment-BERT: Fine-tuned BERT for Sentiment Analysis

## Model Description

Sentiment-BERT is a fine-tuned version of [bert-base-uncased](https://huggingface.co/bert-base-uncased) for binary sentiment classification. The model classifies text as either positive or negative sentiment.

### Model Details

- **Model Type:** Transformer-based text classifier
- **Language:** English
- **License:** Apache 2.0
- **Fine-tuned from:** bert-base-uncased
- **Model Size:** ~110M parameters

## Intended Uses & Limitations

### Intended Uses

- Sentiment analysis of product reviews
- Movie/book review classification
- Social media sentiment monitoring
- Customer feedback analysis

### Limitations

- **Domain Specificity:** Trained primarily on movie reviews; may perform differently on other domains
- **Binary Classification:** Only supports positive/negative; no neutral class
- **Language:** English only
- **Length:** Best performance on texts under 512 tokens

### Out-of-Scope Uses

- Hate speech detection (not designed for this)
- Sarcasm detection (may struggle with sarcastic content)
- Multi-class emotion classification

## Training

### Training Data

The model was trained on:
- [IMDB Movie Reviews](https://huggingface.co/datasets/stanfordnlp/imdb) - 50,000 reviews
- [Rotten Tomatoes](https://huggingface.co/datasets/rotten_tomatoes) - 10,662 reviews

### Training Procedure

#### Preprocessing

- Lowercase text
- Standard BERT tokenization
- Max sequence length: 256 tokens
- Truncation: right side

#### Training Hyperparameters

| Parameter | Value |
|-----------|-------|
| Learning Rate | 2e-5 |
| Batch Size | 32 |
| Epochs | 3 |
| Warmup Steps | 500 |
| Weight Decay | 0.01 |
| Optimizer | AdamW |
| LR Scheduler | Linear with warmup |

#### Hardware

- GPU: 1x NVIDIA A100 40GB
- Training Time: ~2 hours

## Evaluation

### Metrics

| Dataset | Accuracy | F1 | Precision | Recall |
|---------|----------|-----|-----------|--------|
| IMDB (test) | 92.34% | 92.15% | 92.48% | 91.82% |
| Rotten Tomatoes (test) | 88.76% | 88.54% | 88.92% | 88.16% |

### Confusion Matrix (IMDB)

|  | Predicted Positive | Predicted Negative |
|--|-------------------|-------------------|
| **Actual Positive** | 11,542 | 958 |
| **Actual Negative** | 908 | 11,592 |

## Usage

### Using Transformers

```python
from transformers import pipeline

# Load the pipeline
classifier = pipeline("text-classification", model="your-username/sentiment-bert")

# Classify text
result = classifier("This movie was absolutely fantastic!")
print(result)
# [{'label': 'POSITIVE', 'score': 0.9987}]

# Batch classification
texts = [
    "I loved every minute of it!",
    "Terrible movie, don't waste your time.",
    "It was okay, nothing special."
]
results = classifier(texts)
```

### Using the Model Directly

```python
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# Load model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("your-username/sentiment-bert")
model = AutoModelForSequenceClassification.from_pretrained("your-username/sentiment-bert")

# Tokenize input
text = "This is a great product!"
inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=256)

# Get prediction
with torch.no_grad():
    outputs = model(**inputs)
    predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)

# Get label
labels = ["NEGATIVE", "POSITIVE"]
predicted_label = labels[predictions.argmax().item()]
confidence = predictions.max().item()

print(f"{predicted_label}: {confidence:.4f}")
```

### Using Inference API

```python
from huggingface_hub import InferenceClient

client = InferenceClient()
result = client.text_classification("Great movie!", model="your-username/sentiment-bert")
```

## Bias, Risks, and Limitations

### Known Biases

- **Review Style Bias:** Trained on formal review text; may not perform well on informal/slang text
- **Cultural Bias:** Predominantly Western movie reviews; may not generalize to other cultures
- **Length Bias:** Slightly better performance on longer, more detailed reviews

### Risks

- May misclassify sarcastic or ironic content
- Performance degrades on domain-specific jargon
- Should not be used for high-stakes decisions without human review

## Environmental Impact

- **Carbon Emissions:** 12.5 kg CO2eq
- **Hardware:** NVIDIA A100 40GB
- **Training Time:** 2 hours
- **Cloud Provider:** AWS US-West-2

Estimated using [CodeCarbon](https://codecarbon.io/).

## Technical Specifications

### Model Architecture

```
BertForSequenceClassification(
  (bert): BertModel(
    (embeddings): BertEmbeddings(...)
    (encoder): BertEncoder(12 layers)
    (pooler): BertPooler(...)
  )
  (dropout): Dropout(p=0.1)
  (classifier): Linear(768 -> 2)
)
```

### Compute Infrastructure

- **Training:** AWS EC2 p4d.24xlarge
- **Inference:** CPU compatible, GPU recommended

## Citation

If you use this model, please cite:

```bibtex
@misc{sentiment-bert-2024,
  author = {Your Name},
  title = {Sentiment-BERT: Fine-tuned BERT for Sentiment Analysis},
  year = {2024},
  publisher = {Hugging Face},
  journal = {Hugging Face Model Hub},
  howpublished = {\url{https://huggingface.co/your-username/sentiment-bert}}
}
```

## Model Card Authors

- [Your Name](https://huggingface.co/your-username)

## Model Card Contact

For questions or issues, please open a discussion on the model page or contact: your-email@example.com
