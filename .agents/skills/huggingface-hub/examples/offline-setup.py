"""
Offline / Air-Gapped Environment Setup

This script helps set up Hugging Face models and datasets for use in
environments without internet access.

Two phases:
1. DOWNLOAD PHASE (on connected machine): Download models/datasets
2. OFFLINE PHASE (on air-gapped machine): Use cached files

Prerequisites:
    pip install huggingface_hub transformers datasets
"""

import os
import shutil
from pathlib import Path

# =============================================================================
# PHASE 1: DOWNLOAD (Run on internet-connected machine)
# =============================================================================

def download_models_for_offline(
    models: list[str],
    export_dir: str = "./hf_offline_cache",
    include_tokenizer: bool = True
):
    """
    Download models to a directory for offline use.

    Args:
        models: List of model IDs to download
        export_dir: Directory to save models
        include_tokenizer: Also download tokenizer files
    """
    from huggingface_hub import snapshot_download

    export_path = Path(export_dir)
    export_path.mkdir(parents=True, exist_ok=True)

    for model_id in models:
        print(f"\nDownloading: {model_id}")

        # Create safe directory name
        safe_name = model_id.replace("/", "--")
        model_dir = export_path / safe_name

        # Download entire model repository
        snapshot_download(
            repo_id=model_id,
            local_dir=str(model_dir),
            local_dir_use_symlinks=False,  # Copy files, don't symlink
        )

        print(f"  Saved to: {model_dir}")

    print(f"\n=== Download complete ===")
    print(f"Models saved to: {export_path}")
    print(f"\nTransfer this directory to your offline machine.")


def download_datasets_for_offline(
    datasets: list[str],
    export_dir: str = "./hf_offline_cache/datasets"
):
    """
    Download datasets for offline use.

    Args:
        datasets: List of dataset IDs to download
        export_dir: Directory to save datasets
    """
    from huggingface_hub import snapshot_download

    export_path = Path(export_dir)
    export_path.mkdir(parents=True, exist_ok=True)

    for dataset_id in datasets:
        print(f"\nDownloading dataset: {dataset_id}")

        safe_name = dataset_id.replace("/", "--")
        dataset_dir = export_path / safe_name

        snapshot_download(
            repo_id=dataset_id,
            repo_type="dataset",
            local_dir=str(dataset_dir),
            local_dir_use_symlinks=False,
        )

        print(f"  Saved to: {dataset_dir}")

    print(f"\n=== Dataset download complete ===")


def download_specific_files(
    repo_id: str,
    filenames: list[str],
    export_dir: str,
    repo_type: str = "model"
):
    """
    Download specific files from a repository.

    Useful for large models where you only need certain files.
    """
    from huggingface_hub import hf_hub_download

    export_path = Path(export_dir)
    safe_name = repo_id.replace("/", "--")
    repo_dir = export_path / safe_name
    repo_dir.mkdir(parents=True, exist_ok=True)

    for filename in filenames:
        print(f"Downloading: {repo_id}/{filename}")
        path = hf_hub_download(
            repo_id=repo_id,
            filename=filename,
            repo_type=repo_type,
            local_dir=str(repo_dir),
            local_dir_use_symlinks=False,
        )
        print(f"  Saved to: {path}")


# =============================================================================
# PHASE 2: OFFLINE USAGE (Run on air-gapped machine)
# =============================================================================

def setup_offline_environment(cache_dir: str = "./hf_offline_cache"):
    """
    Set environment variables for offline mode.

    Call this at the start of your script on the offline machine.
    """
    cache_path = Path(cache_dir).absolute()

    # Disable all network requests
    os.environ["HF_HUB_OFFLINE"] = "1"
    os.environ["TRANSFORMERS_OFFLINE"] = "1"
    os.environ["HF_DATASETS_OFFLINE"] = "1"

    # Set cache directories
    os.environ["HF_HOME"] = str(cache_path)
    os.environ["HF_HUB_CACHE"] = str(cache_path / "hub")
    os.environ["HUGGINGFACE_HUB_CACHE"] = str(cache_path / "hub")

    # Disable telemetry
    os.environ["HF_HUB_DISABLE_TELEMETRY"] = "1"
    os.environ["DO_NOT_TRACK"] = "1"

    print(f"Offline mode enabled")
    print(f"Cache directory: {cache_path}")


def load_model_offline(model_dir: str):
    """
    Load a model from local directory in offline mode.
    """
    from transformers import AutoModelForCausalLM, AutoTokenizer

    print(f"Loading model from: {model_dir}")

    # Load directly from local directory
    model = AutoModelForCausalLM.from_pretrained(
        model_dir,
        local_files_only=True,  # Important: only use local files
    )

    tokenizer = AutoTokenizer.from_pretrained(
        model_dir,
        local_files_only=True,
    )

    print("Model loaded successfully!")
    return model, tokenizer


def load_dataset_offline(dataset_dir: str):
    """
    Load a dataset from local directory in offline mode.
    """
    from datasets import load_from_disk, load_dataset

    print(f"Loading dataset from: {dataset_dir}")

    # Try loading as Arrow dataset first
    try:
        dataset = load_from_disk(dataset_dir)
    except:
        # Fall back to loading from parquet/csv files
        import pandas as pd
        parquet_files = list(Path(dataset_dir).glob("**/*.parquet"))
        if parquet_files:
            df = pd.concat([pd.read_parquet(f) for f in parquet_files])
            from datasets import Dataset
            dataset = Dataset.from_pandas(df)
        else:
            raise ValueError(f"No loadable data found in {dataset_dir}")

    print("Dataset loaded successfully!")
    return dataset


# =============================================================================
# HELPER: CREATE TRANSFER ARCHIVE
# =============================================================================

def create_transfer_archive(
    cache_dir: str = "./hf_offline_cache",
    archive_name: str = "hf_offline_transfer"
):
    """
    Create a compressed archive for transfer to air-gapped machine.
    """
    archive_path = shutil.make_archive(
        archive_name,
        'gztar',  # .tar.gz
        root_dir='.',
        base_dir=cache_dir
    )
    print(f"Created archive: {archive_path}")
    print(f"Transfer this file to your offline machine and extract with:")
    print(f"  tar -xzf {archive_name}.tar.gz")


# =============================================================================
# EXAMPLE USAGE
# =============================================================================

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Offline setup for Hugging Face")
    parser.add_argument("--mode", choices=["download", "offline", "archive"],
                        required=True, help="Operation mode")
    parser.add_argument("--cache-dir", default="./hf_offline_cache",
                        help="Cache directory")
    args = parser.parse_args()

    if args.mode == "download":
        print("=== DOWNLOAD MODE ===")
        print("Downloading models and datasets for offline use...\n")

        # Example: Download popular models
        MODELS_TO_DOWNLOAD = [
            "distilbert-base-uncased",
            "sentence-transformers/all-MiniLM-L6-v2",
            # Add more models as needed
        ]

        DATASETS_TO_DOWNLOAD = [
            "stanfordnlp/imdb",
            # Add more datasets as needed
        ]

        download_models_for_offline(MODELS_TO_DOWNLOAD, args.cache_dir + "/models")
        download_datasets_for_offline(DATASETS_TO_DOWNLOAD, args.cache_dir + "/datasets")

        print("\n=== DOWNLOAD COMPLETE ===")
        print(f"All files saved to: {args.cache_dir}")
        print("\nNext steps:")
        print("1. Run with --mode archive to create transfer archive")
        print("2. Transfer archive to air-gapped machine")
        print("3. Extract and run with --mode offline")

    elif args.mode == "archive":
        print("=== CREATING TRANSFER ARCHIVE ===")
        create_transfer_archive(args.cache_dir)

    elif args.mode == "offline":
        print("=== OFFLINE MODE ===")

        # Setup environment
        setup_offline_environment(args.cache_dir)

        # Example: Load a model
        model_dir = Path(args.cache_dir) / "models" / "distilbert-base-uncased"
        if model_dir.exists():
            model, tokenizer = load_model_offline(str(model_dir))

            # Test inference
            inputs = tokenizer("Hello, world!", return_tensors="pt")
            outputs = model(**inputs)
            print(f"Model output shape: {outputs.last_hidden_state.shape}")
        else:
            print(f"Model not found at {model_dir}")
            print("Make sure to run --mode download first on a connected machine")


# =============================================================================
# QUICK REFERENCE: ENVIRONMENT VARIABLES
# =============================================================================
"""
Key environment variables for offline mode:

# Disable network access
export HF_HUB_OFFLINE=1
export TRANSFORMERS_OFFLINE=1
export HF_DATASETS_OFFLINE=1

# Set cache location
export HF_HOME=/path/to/cache
export HF_HUB_CACHE=/path/to/cache/hub

# Disable telemetry
export HF_HUB_DISABLE_TELEMETRY=1
export DO_NOT_TRACK=1

# For specific library caches
export HUGGINGFACE_HUB_CACHE=/path/to/cache
export TRANSFORMERS_CACHE=/path/to/cache
export HF_DATASETS_CACHE=/path/to/cache
"""
