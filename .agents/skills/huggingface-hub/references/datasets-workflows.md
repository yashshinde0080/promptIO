# Dataset Workflows Reference

Working with Hub datasets using pandas, Polars, DuckDB, and streaming.

## hf:// Protocol

Access Hub data directly with the `hf://` protocol:

```
hf://datasets/{username}/{dataset}/{path}
hf://datasets/{username}/{dataset}@{revision}/{path}
hf://datasets/{username}/{dataset}@~parquet/{path}  # Auto-converted parquet
```

## Pandas

### Loading Data

```python
import pandas as pd

# Load Parquet file
df = pd.read_parquet("hf://datasets/stanfordnlp/imdb/plain_text/train-00000-of-00001.parquet")

# Load CSV
df = pd.read_csv("hf://datasets/username/my-dataset/data.csv")

# Load JSON
df = pd.read_json("hf://datasets/username/my-dataset/data.json")

# Load multiple files with glob
df = pd.read_parquet("hf://datasets/username/my-dataset/train-*.parquet")
```

### Saving Data

```python
from huggingface_hub import HfApi, login

# Login first
login()

# Create dataset repo
api = HfApi()
api.create_repo(repo_id="username/my-dataset", repo_type="dataset")

# Save with hf:// protocol
df.to_parquet("hf://datasets/username/my-dataset/data.parquet", index=False)

# Save splits
df_train.to_parquet("hf://datasets/username/my-dataset/train.parquet")
df_valid.to_parquet("hf://datasets/username/my-dataset/validation.parquet")
df_test.to_parquet("hf://datasets/username/my-dataset/test.parquet")
```

### Image Datasets

```python
# Load metadata CSV with image paths
folder_path = "path/to/images/"
df = pd.read_csv(folder_path + "metadata.csv")

# Structure:
# folder/
# ├── metadata.csv
# ├── img001.png
# └── img002.png

# Upload to Hub
from huggingface_hub import HfApi
api = HfApi()
api.upload_folder(
    folder_path=folder_path,
    repo_id="username/my-image-dataset",
    repo_type="dataset"
)
```

## Polars

Native HF support since version 1.2.0 with query optimization.

### Loading Data

```python
import polars as pl

# Eager API (interactive)
df = pl.read_parquet("hf://datasets/stanfordnlp/imdb/plain_text/train-*.parquet")

# Lazy API (optimized, recommended for large data)
df = pl.scan_parquet("hf://datasets/stanfordnlp/imdb/plain_text/train-*.parquet")
result = df.filter(pl.col("label") == 1).collect()

# Auto-converted parquet (for non-parquet datasets)
df = pl.read_parquet("hf://datasets/username/csv-dataset@~parquet/data.parquet")
```

### Query Optimization

Polars automatically pushes predicates and projections:

```python
# Only downloads needed columns and filtered rows
df = (
    pl.scan_parquet("hf://datasets/large-dataset/data/*.parquet")
    .select(["id", "text"])  # Projection pushdown
    .filter(pl.col("id") > 1000)  # Predicate pushdown
    .collect()
)
```

### Saving Data

```python
# Write to Hub
df.write_parquet("hf://datasets/username/my-dataset/data.parquet")
```

## DuckDB

In-process SQL database with native HF support.

### CLI Usage

```bash
# Start DuckDB CLI
duckdb

# Query Hub dataset
SELECT * FROM 'hf://datasets/ibm/duorc/ParaphraseRC/*.parquet' LIMIT 10;

# Filter and aggregate
SELECT label, COUNT(*) as count
FROM 'hf://datasets/stanfordnlp/imdb/plain_text/*.parquet'
GROUP BY label;
```

### Python Usage

```python
import duckdb

# Create connection
conn = duckdb.connect()

# Query Hub dataset
df = conn.execute("""
    SELECT *
    FROM 'hf://datasets/ibm/duorc/ParaphraseRC/*.parquet'
    LIMIT 100
""").fetchdf()

# Complex analytics
result = conn.execute("""
    SELECT
        label,
        AVG(LENGTH(text)) as avg_length,
        COUNT(*) as count
    FROM 'hf://datasets/stanfordnlp/imdb/plain_text/*.parquet'
    GROUP BY label
""").fetchdf()
```

### Vector Similarity Search

```python
import duckdb
import numpy as np

conn = duckdb.connect()

# Load embeddings
conn.execute("""
    CREATE TABLE embeddings AS
    SELECT * FROM 'hf://datasets/username/embeddings/data.parquet'
""")

# Find similar vectors
query_vector = np.random.rand(384).tolist()
results = conn.execute(f"""
    SELECT id, text,
           list_cosine_similarity(embedding, {query_vector}) as similarity
    FROM embeddings
    ORDER BY similarity DESC
    LIMIT 10
""").fetchdf()
```

## Streaming with datasets Library

For datasets too large to fit in memory.

```python
from datasets import load_dataset

# Stream without downloading entire dataset
dataset = load_dataset("HuggingFaceFW/fineweb", streaming=True, split="train")

# Iterate
for example in dataset.take(1000):
    process(example)

# With transformations
dataset = dataset.map(tokenize_function, batched=True)
dataset = dataset.filter(lambda x: len(x["text"]) > 100)

# Convert to pandas in chunks
for batch in dataset.iter(batch_size=10000):
    df_chunk = pd.DataFrame(batch)
    process_chunk(df_chunk)
```

## Private Datasets

### Authentication

```python
import os
os.environ["HF_TOKEN"] = "hf_xxx"

# Or login
from huggingface_hub import login
login()

# Now hf:// works with private datasets
df = pd.read_parquet("hf://datasets/username/private-dataset/data.parquet")
```

### DuckDB with Auth

```python
import duckdb
import os

conn = duckdb.connect()

# Set token for DuckDB
conn.execute(f"SET hf_token='{os.environ['HF_TOKEN']}'")

# Query private dataset
df = conn.execute("""
    SELECT * FROM 'hf://datasets/username/private-dataset/data.parquet'
""").fetchdf()
```

## Dataset Viewer Compatibility

For the Dataset Viewer to work, use supported structures:

### Parquet (Recommended)

```
dataset/
├── train.parquet
├── validation.parquet
└── test.parquet
```

Or sharded:

```
dataset/
├── train/
│   ├── 0000.parquet
│   └── 0001.parquet
└── test/
    └── 0000.parquet
```

### CSV/JSON

```
dataset/
├── data.csv
└── README.md
```

### Image Dataset

```
dataset/
├── metadata.csv    # Must have 'file_name' column
├── train/
│   ├── img001.png
│   └── img002.png
└── test/
    └── img003.png
```

## Data Format Conversion

### Auto-Converted Parquet

Hub auto-converts many formats to Parquet:

```python
# Access auto-converted version
df = pd.read_parquet("hf://datasets/username/csv-dataset@~parquet/data.parquet")

# Same with Polars
df = pl.read_parquet("hf://datasets/username/csv-dataset@~parquet/data.parquet")
```

### Manual Conversion

```python
from datasets import load_dataset

# Load any format
dataset = load_dataset("username/my-dataset")

# Save as Parquet
dataset.to_parquet("data.parquet")

# Push back to Hub
from huggingface_hub import HfApi
api = HfApi()
api.upload_file(
    path_or_fileobj="data.parquet",
    path_in_repo="data.parquet",
    repo_id="username/my-dataset",
    repo_type="dataset"
)
```

## Performance Tips

### 1. Use Parquet Format

Parquet is columnar and compressed - much faster than CSV.

### 2. Partition Large Datasets

```
data/
├── year=2023/
│   ├── month=01/
│   │   └── data.parquet
│   └── month=02/
│       └── data.parquet
└── year=2024/
    └── month=01/
        └── data.parquet
```

Query only needed partitions:

```python
df = pl.scan_parquet("hf://datasets/user/data/year=2024/**/*.parquet")
```

### 3. Use Lazy Evaluation (Polars)

```python
# Lazy - only computes what's needed
result = (
    pl.scan_parquet("hf://...")
    .select(["col1", "col2"])
    .filter(pl.col("col1") > 0)
    .collect()
)
```

### 4. Stream Large Datasets

```python
# Don't load everything at once
from datasets import load_dataset
ds = load_dataset("huge-dataset", streaming=True)
```

## Resources

- Pandas guide: https://huggingface.co/docs/hub/datasets-pandas
- Polars guide: https://huggingface.co/docs/hub/datasets-polars
- DuckDB guide: https://huggingface.co/docs/hub/datasets-duckdb
- datasets library: https://huggingface.co/docs/datasets
