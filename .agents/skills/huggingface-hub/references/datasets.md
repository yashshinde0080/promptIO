# Datasets Reference

Complete guide for dataset repositories on Hugging Face Hub.

## Dataset Repository Structure

```
my-dataset/
├── README.md           # Dataset card with metadata
├── data/
│   ├── train.parquet   # Training split
│   ├── test.parquet    # Test split
│   └── validation.parquet
└── dataset_info.json   # Optional metadata
```

## Supported Formats

| Format | Extensions | Notes |
|--------|------------|-------|
| Parquet | `.parquet` | Recommended, efficient |
| CSV | `.csv` | Common, text-based |
| JSON | `.json`, `.jsonl` | Flexible structure |
| Arrow | `.arrow` | Fast loading |
| Text | `.txt` | One sample per line |
| Images | `.jpg`, `.png`, etc. | With metadata files |
| Audio | `.wav`, `.mp3`, etc. | With metadata files |

## Dataset Card (README.md)

### Basic Structure

```yaml
---
language:
  - en
license: cc-by-4.0
task_categories:
  - text-classification
pretty_name: My Dataset
size_categories:
  - 10K<n<100K
---

# Dataset Card for My Dataset

## Dataset Description

Brief description of the dataset...

## Dataset Structure

### Data Fields

- `text`: The input text
- `label`: Classification label (0 or 1)

### Data Splits

| Split | Samples |
|-------|---------|
| train | 10,000 |
| test | 2,000 |

## Dataset Creation

How the dataset was created...

## Considerations for Using the Data

Potential biases, limitations...
```

### Metadata Fields

#### Basic Metadata

```yaml
pretty_name: Human-Readable Dataset Name
license: cc-by-4.0

language:
  - en
  - fr

size_categories:
  - n<1K
  - 1K<n<10K
  - 10K<n<100K
  - 100K<n<1M
  - 1M<n<10M
  - 10M<n<100M
  - 100M<n<1B
  - n>1B
```

#### Task Categories

```yaml
task_categories:
  - text-classification
  - token-classification
  - question-answering
  - summarization
  - translation
  - text-generation
  - image-classification
  - object-detection
  - automatic-speech-recognition
  - audio-classification
  - text-to-image
  - conversational
```

#### Tags

```yaml
tags:
  - sentiment-analysis
  - news
  - social-media
  - curated
```

#### Modality Tags

```yaml
# Force specific modality detection
tags:
  - audio
  - image
  - text
  - tabular
  - video
  - geospatial
  - 3d
  - timeseries
```

#### Associated Libraries

```yaml
tags:
  - datasets        # HF datasets library
  - pandas         # pandas compatible
  - webdataset     # WebDataset format
  - mlcroissant    # ML Croissant format
```

## Uploading Datasets

### Using datasets Library

```python
from datasets import Dataset, DatasetDict

# Create dataset
data = {
    "text": ["Hello", "World"],
    "label": [0, 1]
}
dataset = Dataset.from_dict(data)

# Push to Hub
dataset.push_to_hub("user/my-dataset")

# With splits
dataset_dict = DatasetDict({
    "train": train_dataset,
    "test": test_dataset
})
dataset_dict.push_to_hub("user/my-dataset")
```

### Using huggingface_hub

```python
from huggingface_hub import HfApi, upload_folder

api = HfApi()

# Create repo
api.create_repo(repo_id="user/my-dataset", repo_type="dataset")

# Upload folder
upload_folder(
    folder_path="./my_data",
    repo_id="user/my-dataset",
    repo_type="dataset"
)
```

### From Pandas

```python
import pandas as pd
from datasets import Dataset

df = pd.read_csv("data.csv")
dataset = Dataset.from_pandas(df)
dataset.push_to_hub("user/my-dataset")
```

### Parquet Files Directly

```python
import pandas as pd

df = pd.read_csv("data.csv")
df.to_parquet("train.parquet")

# Upload parquet file
api.upload_file(
    path_or_fileobj="train.parquet",
    path_in_repo="data/train.parquet",
    repo_id="user/my-dataset",
    repo_type="dataset"
)
```

## Loading Datasets

### Basic Loading

```python
from datasets import load_dataset

# Load from Hub
dataset = load_dataset("user/my-dataset")

# Specific split
train_data = load_dataset("user/my-dataset", split="train")

# Specific configuration
dataset = load_dataset("user/my-dataset", "config_name")
```

### Streaming (Large Datasets)

```python
# Stream without downloading
dataset = load_dataset("user/my-dataset", streaming=True)

for example in dataset["train"]:
    print(example)
    break
```

### Private Datasets

```python
dataset = load_dataset(
    "user/private-dataset",
    token=os.environ["HF_TOKEN"]
)
```

## Data Files Configuration

### Automatic Detection

Files in `data/` are auto-detected by split name:
- `train.parquet`, `train.csv` → train split
- `test.parquet`, `test.csv` → test split
- `validation.parquet` → validation split

### Manual Configuration

In README.md YAML:

```yaml
---
configs:
  - config_name: default
    data_files:
      train: data/train/*.parquet
      test: data/test/*.parquet
---
```

### Multiple Configurations

```yaml
---
configs:
  - config_name: english
    data_files:
      train: en/train.parquet
      test: en/test.parquet
  - config_name: french
    data_files:
      train: fr/train.parquet
      test: fr/test.parquet
---
```

### Pattern Matching

```yaml
---
configs:
  - config_name: default
    data_files:
      train:
        - "data/train-*.parquet"
        - "data/extra/*.parquet"
      test: "data/test.parquet"
---
```

## Image Datasets

### Structure with Metadata

```
my-image-dataset/
├── README.md
├── metadata.csv
└── images/
    ├── image001.jpg
    ├── image002.jpg
    └── ...
```

**metadata.csv:**
```csv
file_name,label
images/image001.jpg,cat
images/image002.jpg,dog
```

### ImageFolder Format

```
my-image-dataset/
├── README.md
├── train/
│   ├── cat/
│   │   ├── 001.jpg
│   │   └── 002.jpg
│   └── dog/
│       ├── 001.jpg
│       └── 002.jpg
└── test/
    ├── cat/
    └── dog/
```

```python
dataset = load_dataset("imagefolder", data_dir="my-image-dataset")
```

## Audio Datasets

### Structure

```
my-audio-dataset/
├── README.md
├── metadata.csv
└── audio/
    ├── clip001.wav
    ├── clip002.wav
    └── ...
```

**metadata.csv:**
```csv
file_name,transcription
audio/clip001.wav,Hello world
audio/clip002.wav,How are you
```

## Dataset Viewer

Datasets automatically get:
- Preview of first 100 rows
- Column statistics
- Search functionality

Configure viewer:
```yaml
---
viewer: true  # Enable (default)
viewer: false # Disable
---
```

## SQL Console

Query datasets with SQL:

```sql
SELECT * FROM train WHERE label = 'positive' LIMIT 10
```

Available at dataset page under "SQL Console" tab.

## Private Datasets

```python
# Create private
api.create_repo(
    repo_id="user/private-data",
    repo_type="dataset",
    private=True
)

# Access
dataset = load_dataset(
    "user/private-data",
    token=os.environ["HF_TOKEN"]
)
```

## Gated Datasets

For datasets requiring terms acceptance:

1. Enable gating in Settings
2. Add terms text
3. Users must accept before access

## Dataset Statistics

Track:
- Total downloads
- Views
- Favorites

View at: `https://huggingface.co/datasets/user/dataset/stats`

## Linking Paper

```yaml
---
# Include arXiv link in README
---

Paper: https://arxiv.org/abs/2203.xxxxx
```

Automatically adds `arxiv:2203.xxxxx` tag.

## Best Practices

1. **Use Parquet format** - Efficient, compressed, typed
2. **Include clear documentation** - Data fields, collection, biases
3. **Add task categories** - Improves discoverability
4. **Specify license clearly** - Required for proper use
5. **Include data statistics** - Size, splits, distributions
6. **Add examples** - Show sample data in README
7. **Document preprocessing** - How to use the data
