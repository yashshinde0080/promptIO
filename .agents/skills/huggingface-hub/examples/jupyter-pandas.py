"""
Jupyter + Pandas Workflow with Hugging Face Hub

This example demonstrates how to work with HF datasets using pandas
in Jupyter notebooks or Python scripts. Uses the hf:// protocol for
seamless access to Hub data.

Prerequisites:
    pip install pandas pyarrow huggingface_hub
    huggingface-cli login  # For private datasets or saving
"""

import pandas as pd
from huggingface_hub import HfApi, login

# =============================================================================
# LOADING DATA FROM HUB
# =============================================================================

# Load Parquet file directly with hf:// protocol
df = pd.read_parquet("hf://datasets/stanfordnlp/imdb/plain_text/train-00000-of-00001.parquet")
print(f"Loaded {len(df)} rows")
print(df.head())

# Load CSV file
# df = pd.read_csv("hf://datasets/username/my-dataset/data.csv")

# Load JSON file
# df = pd.read_json("hf://datasets/username/my-dataset/data.json")

# Load with glob pattern (multiple files)
# df = pd.read_parquet("hf://datasets/username/my-dataset/train-*.parquet")


# =============================================================================
# EXPLORING DATA
# =============================================================================

# Basic exploration
print("\n--- Dataset Info ---")
print(f"Shape: {df.shape}")
print(f"Columns: {df.columns.tolist()}")
print(f"Data types:\n{df.dtypes}")

# Quick statistics
print("\n--- Sample Data ---")
print(df.head(10))

# Value counts for label column
if 'label' in df.columns:
    print("\n--- Label Distribution ---")
    print(df['label'].value_counts())

# Text length analysis
if 'text' in df.columns:
    df['text_length'] = df['text'].str.len()
    print("\n--- Text Length Statistics ---")
    print(df['text_length'].describe())


# =============================================================================
# DATA TRANSFORMATIONS
# =============================================================================

# Filter data
positive_reviews = df[df['label'] == 1]
print(f"\nPositive reviews: {len(positive_reviews)}")

# Sample data
sample = df.sample(n=100, random_state=42)

# Create train/validation/test splits
from sklearn.model_selection import train_test_split  # type: ignore

train_df, temp_df = train_test_split(df, test_size=0.3, random_state=42)
val_df, test_df = train_test_split(temp_df, test_size=0.5, random_state=42)

print(f"\nSplits: train={len(train_df)}, val={len(val_df)}, test={len(test_df)}")


# =============================================================================
# SAVING DATA TO HUB
# =============================================================================

# First, login if not already (interactive prompt)
# login()

# Create a new dataset repository
api = HfApi()
# api.create_repo(repo_id="username/my-processed-dataset", repo_type="dataset")

# Save to Hub using hf:// protocol
# df.to_parquet("hf://datasets/username/my-processed-dataset/data.parquet", index=False)

# Save splits separately
# train_df.to_parquet("hf://datasets/username/my-processed-dataset/train.parquet", index=False)
# val_df.to_parquet("hf://datasets/username/my-processed-dataset/validation.parquet", index=False)
# test_df.to_parquet("hf://datasets/username/my-processed-dataset/test.parquet", index=False)


# =============================================================================
# WORKING WITH IMAGES
# =============================================================================

# For image datasets with metadata CSV
# folder_path = "path/to/folder/"
# df = pd.read_csv(folder_path + "metadata.csv")
#
# Iterate over images
# for image_path in (folder_path + df["file_name"]):
#     # Process image
#     pass
#
# Upload folder to Hub
# api.upload_folder(
#     folder_path=folder_path,
#     repo_id="username/my-image-dataset",
#     repo_type="dataset",
# )


# =============================================================================
# USING TRANSFORMERS WITH PANDAS
# =============================================================================

# Text classification pipeline
from transformers import pipeline  # type: ignore
from tqdm import tqdm  # type: ignore

# Load a classification model
classifier = pipeline(
    "text-classification",
    model="distilbert-base-uncased-finetuned-sst-2-english"
)

# Classify texts (with progress bar)
sample_df = df.head(100).copy()
results = [
    classifier(text)[0]
    for text in tqdm(sample_df['text'], desc="Classifying")
]

# Add predictions to dataframe
sample_df['predicted_label'] = [r['label'] for r in results]
sample_df['confidence'] = [r['score'] for r in results]

print("\n--- Classification Results ---")
print(sample_df[['text', 'label', 'predicted_label', 'confidence']].head())


# =============================================================================
# BATCH PROCESSING FOR LARGE DATASETS
# =============================================================================

def process_in_batches(df, batch_size=32):
    """Process large dataframes in batches to manage memory."""
    results = []

    for i in tqdm(range(0, len(df), batch_size), desc="Processing batches"):
        batch = df.iloc[i:i+batch_size]
        # Process batch
        batch_results = classifier(batch['text'].tolist())
        results.extend(batch_results)

    return results

# Usage:
# all_results = process_in_batches(df, batch_size=32)


# =============================================================================
# EXPORT RESULTS
# =============================================================================

# Save locally
# sample_df.to_csv("results.csv", index=False)
# sample_df.to_parquet("results.parquet", index=False)
# sample_df.to_json("results.json", orient="records", lines=True)

# Save to Hub
# sample_df.to_parquet("hf://datasets/username/my-results/predictions.parquet", index=False)

print("\n--- Done! ---")
