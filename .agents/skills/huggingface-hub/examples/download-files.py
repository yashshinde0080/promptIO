"""
Download Files from Hub Examples

Complete examples of downloading models, datasets, and files
from Hugging Face Hub using various methods.

Requirements:
    pip install huggingface_hub transformers datasets
"""

import os
from pathlib import Path


# =============================================================================
# Method 1: hf_hub_download (Single Files)
# =============================================================================

def example_single_file_download():
    """Download individual files from a repository."""
    from huggingface_hub import hf_hub_download

    # Download a config file
    config_path = hf_hub_download(
        repo_id="bert-base-uncased",
        filename="config.json",
    )
    print(f"Config downloaded to: {config_path}")

    # Download to specific directory
    model_path = hf_hub_download(
        repo_id="bert-base-uncased",
        filename="pytorch_model.bin",
        local_dir="./my_model",
    )
    print(f"Model downloaded to: {model_path}")

    # Download specific revision/branch
    config_path = hf_hub_download(
        repo_id="bert-base-uncased",
        filename="config.json",
        revision="main",  # or commit hash, tag
    )

    # Download from subfolder
    file_path = hf_hub_download(
        repo_id="user/repo",
        filename="model.safetensors",
        subfolder="checkpoints",
    )

    # Download dataset file
    data_path = hf_hub_download(
        repo_id="squad",
        filename="train-v1.1.json",
        repo_type="dataset",
    )
    print(f"Dataset file: {data_path}")

    # Force re-download (bypass cache)
    fresh_path = hf_hub_download(
        repo_id="bert-base-uncased",
        filename="config.json",
        force_download=True,
    )

    return config_path


# =============================================================================
# Method 2: snapshot_download (Entire Repository)
# =============================================================================

def example_snapshot_download():
    """Download entire repositories."""
    from huggingface_hub import snapshot_download

    # Download entire model repository
    model_dir = snapshot_download(repo_id="bert-base-uncased")
    print(f"Model downloaded to: {model_dir}")

    # Download to specific directory
    model_dir = snapshot_download(
        repo_id="bert-base-uncased",
        local_dir="./bert-model",
    )

    # Download only specific files (by pattern)
    model_dir = snapshot_download(
        repo_id="bert-base-uncased",
        allow_patterns=["*.json", "*.txt"],  # Only JSON and text files
        ignore_patterns=["*.bin", "*.safetensors"],  # Skip weights
    )

    # Download specific revision
    model_dir = snapshot_download(
        repo_id="bert-base-uncased",
        revision="v1.0",
    )

    # Download dataset
    dataset_dir = snapshot_download(
        repo_id="squad",
        repo_type="dataset",
    )

    return model_dir


# =============================================================================
# Method 3: CLI Download
# =============================================================================

def example_cli_download():
    """Examples using the huggingface-cli."""
    import subprocess

    # Download entire repository
    # subprocess.run(["hf", "download", "bert-base-uncased"])

    # Download specific files
    # subprocess.run(["hf", "download", "bert-base-uncased", "config.json", "tokenizer.json"])

    # Download to specific directory
    # subprocess.run(["hf", "download", "bert-base-uncased", "--local-dir", "./my-bert"])

    # Download dataset
    # subprocess.run(["hf", "download", "squad", "--repo-type", "dataset"])

    print("CLI commands (run in terminal):")
    print("  hf download bert-base-uncased")
    print("  hf download bert-base-uncased config.json tokenizer.json")
    print("  hf download bert-base-uncased --local-dir ./my-bert")
    print("  hf download squad --repo-type dataset")


# =============================================================================
# Method 4: Transformers Library
# =============================================================================

def example_transformers_download():
    """Download models using transformers library."""
    from transformers import AutoModel, AutoTokenizer, AutoConfig

    # Download model (caches automatically)
    model = AutoModel.from_pretrained("bert-base-uncased")
    tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

    # Download only config
    config = AutoConfig.from_pretrained("bert-base-uncased")
    print(f"Hidden size: {config.hidden_size}")

    # Download specific revision
    model = AutoModel.from_pretrained(
        "bert-base-uncased",
        revision="v1.0",
    )

    # Download private model
    model = AutoModel.from_pretrained(
        "user/private-model",
        token=os.environ.get("HF_TOKEN"),
    )

    # Download to specific cache directory
    model = AutoModel.from_pretrained(
        "bert-base-uncased",
        cache_dir="./my_cache",
    )

    return model, tokenizer


# =============================================================================
# Method 5: Datasets Library
# =============================================================================

def example_datasets_download():
    """Download datasets using datasets library."""
    from datasets import load_dataset

    # Download dataset
    dataset = load_dataset("stanfordnlp/imdb")
    print(f"Train samples: {len(dataset['train'])}")

    # Download specific split
    train_data = load_dataset("stanfordnlp/imdb", split="train")

    # Download specific configuration
    dataset = load_dataset("glue", "mrpc")

    # Stream large datasets (no full download)
    dataset = load_dataset("stanfordnlp/imdb", streaming=True)
    for example in dataset["train"]:
        print(example)
        break

    # Download private dataset
    dataset = load_dataset(
        "user/private-dataset",
        token=os.environ.get("HF_TOKEN"),
    )

    return dataset


# =============================================================================
# Method 6: High-Performance Downloads
# =============================================================================

def example_high_performance_download():
    """Enable high-performance download mode."""
    import os

    # Set environment variable for high-performance mode
    os.environ["HF_XET_HIGH_PERFORMANCE"] = "1"

    from huggingface_hub import snapshot_download

    # Downloads will now use all CPU cores
    model_dir = snapshot_download(repo_id="meta-llama/Llama-3.1-8B")

    print("High-performance download complete!")


# =============================================================================
# Method 7: Cached Downloads
# =============================================================================

def example_cache_management():
    """Manage downloaded cache."""
    from huggingface_hub import scan_cache_dir, HfApi

    # Scan cache to see what's downloaded
    cache_info = scan_cache_dir()
    print(f"Total cache size: {cache_info.size_on_disk_str}")

    for repo in cache_info.repos:
        print(f"  {repo.repo_id}: {repo.size_on_disk_str}")

    # Get cache directory
    from huggingface_hub import constants
    print(f"Cache directory: {constants.HF_HUB_CACHE}")

    # Clear specific repo from cache
    # delete_strategy = cache_info.delete_revisions("bert-base-uncased")
    # delete_strategy.execute()


# =============================================================================
# Method 8: Conditional Downloads
# =============================================================================

def example_conditional_download():
    """Download only if not already cached."""
    from huggingface_hub import hf_hub_download, try_to_load_from_cache

    repo_id = "bert-base-uncased"
    filename = "config.json"

    # Check if file is already cached
    cached_path = try_to_load_from_cache(
        repo_id=repo_id,
        filename=filename,
    )

    if cached_path is not None:
        print(f"File already cached at: {cached_path}")
        return cached_path
    else:
        print("File not cached, downloading...")
        return hf_hub_download(repo_id=repo_id, filename=filename)


# =============================================================================
# Method 9: Download with Progress
# =============================================================================

def example_download_with_progress():
    """Download with progress callback."""
    from huggingface_hub import hf_hub_download

    # hf_hub_download shows progress by default
    path = hf_hub_download(
        repo_id="bert-base-uncased",
        filename="config.json",
        local_files_only=False,
    )

    print(f"Downloaded to: {path}")


# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":
    print("=== Single File Download ===")
    example_single_file_download()

    print("\n=== Snapshot Download ===")
    # example_snapshot_download()

    print("\n=== CLI Download ===")
    example_cli_download()

    print("\n=== Transformers Download ===")
    # example_transformers_download()

    print("\n=== Datasets Download ===")
    # example_datasets_download()

    print("\n=== Cache Management ===")
    # example_cache_management()

    print("\n=== Conditional Download ===")
    # example_conditional_download()
