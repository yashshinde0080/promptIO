---
language:
  - en
license: cc-by-4.0
task_categories:
  - text-classification
  - token-classification
task_ids:
  - sentiment-analysis
  - named-entity-recognition
pretty_name: Customer Reviews Dataset
size_categories:
  - 100K<n<1M
source_datasets:
  - original
annotations_creators:
  - crowdsourced
multilinguality:
  - monolingual
tags:
  - e-commerce
  - reviews
  - sentiment
  - ner
dataset_info:
  features:
    - name: text
      dtype: string
    - name: label
      dtype:
        class_label:
          names:
            '0': negative
            '1': neutral
            '2': positive
    - name: entities
      sequence:
        - name: start
          dtype: int32
        - name: end
          dtype: int32
        - name: label
          dtype: string
  splits:
    - name: train
      num_examples: 850000
    - name: validation
      num_examples: 50000
    - name: test
      num_examples: 100000
configs:
  - config_name: default
    data_files:
      - split: train
        path: data/train-*.parquet
      - split: validation
        path: data/validation.parquet
      - split: test
        path: data/test.parquet
---

# Customer Reviews Dataset

## Dataset Description

A large-scale dataset of customer reviews from e-commerce platforms, annotated for sentiment analysis and named entity recognition.

### Dataset Summary

This dataset contains 1 million customer reviews collected from various e-commerce platforms. Each review is annotated with:
- **Sentiment labels**: negative, neutral, positive
- **Named entities**: product names, brands, features, prices

### Supported Tasks

| Task | Description |
|------|-------------|
| `text-classification` | Predict sentiment (negative/neutral/positive) |
| `token-classification` | Extract named entities from reviews |

### Languages

English (en)

## Dataset Structure

### Data Instances

```json
{
  "text": "The Samsung Galaxy S21 has an amazing camera but the battery life could be better.",
  "label": 2,
  "entities": [
    {"start": 4, "end": 20, "label": "PRODUCT"},
    {"start": 32, "end": 38, "label": "FEATURE"},
    {"start": 47, "end": 59, "label": "FEATURE"}
  ]
}
```

### Data Fields

| Field | Type | Description |
|-------|------|-------------|
| `text` | string | The review text |
| `label` | int | Sentiment: 0=negative, 1=neutral, 2=positive |
| `entities` | list | Named entities with start, end, and label |

### Data Splits

| Split | Examples | Description |
|-------|----------|-------------|
| train | 850,000 | Training data |
| validation | 50,000 | Validation data |
| test | 100,000 | Held-out test data |

## Dataset Creation

### Curation Rationale

Created to support research in multi-task learning combining sentiment analysis and NER on product reviews.

### Source Data

Reviews collected from publicly available e-commerce review pages with permission.

### Annotations

#### Annotation Process

- Sentiment labels: 3 annotators per review, majority vote
- Named entities: Expert annotators with adjudication

#### Who are the annotators?

Crowdsourced workers on Amazon Mechanical Turk (sentiment) and trained linguists (NER).

### Personal and Sensitive Information

All personally identifiable information (names, emails, addresses) has been removed or anonymized.

## Considerations for Using the Data

### Social Impact

This dataset can be used to improve product recommendations and customer service automation.

### Discussion of Biases

- English-only limits applicability
- E-commerce domain may not generalize to other review types
- Potential brand representation imbalances

### Other Known Limitations

- Reviews longer than 512 tokens are truncated
- Some sarcastic reviews may be mislabeled

## Additional Information

### Dataset Curators

Created by the NLP Research Team at Example University.

### Licensing Information

Creative Commons Attribution 4.0 International (CC BY 4.0)

### Citation Information

```bibtex
@dataset{customer_reviews_2024,
  author = {Research Team},
  title = {Customer Reviews Dataset for Sentiment and NER},
  year = {2024},
  publisher = {Hugging Face},
  url = {https://huggingface.co/datasets/your-username/customer-reviews}
}
```

### Contributions

Thanks to [@username](https://huggingface.co/username) for adding this dataset.

## Usage

```python
from datasets import load_dataset

# Load the dataset
dataset = load_dataset("your-username/customer-reviews")

# Access splits
train = dataset["train"]
test = dataset["test"]

# Stream large dataset
dataset = load_dataset("your-username/customer-reviews", streaming=True)
for example in dataset["train"]:
    print(example)
    break
```
