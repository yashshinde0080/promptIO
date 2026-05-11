"""
LoRA / PEFT Adapter Workflow

Complete workflow for finding, loading, merging, and deploying LoRA adapters.

Prerequisites:
    pip install transformers peft accelerate bitsandbytes
    huggingface-cli login
"""

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import PeftModel, PeftConfig, LoraConfig, get_peft_model
from huggingface_hub import HfApi

# =============================================================================
# 1. FINDING ADAPTERS
# =============================================================================

api = HfApi()

# Search for PEFT/LoRA adapters
adapters = api.list_models(
    library="peft",
    sort="downloads",
    limit=10
)

print("Popular PEFT adapters:")
for adapter in adapters:
    print(f"  - {adapter.id}")


# =============================================================================
# 2. LOADING AN EXISTING ADAPTER
# =============================================================================

# Define base model and adapter
BASE_MODEL = "mistralai/Mistral-7B-v0.1"
ADAPTER_MODEL = "dfurman/Mistral-7B-Instruct-v0.2"  # Example adapter

# Get adapter config to verify base model
config = PeftConfig.from_pretrained(ADAPTER_MODEL)
print(f"\nAdapter base model: {config.base_model_name_or_path}")

# Load base model (optionally quantized for memory efficiency)
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True
)

base_model = AutoModelForCausalLM.from_pretrained(
    BASE_MODEL,
    quantization_config=bnb_config,
    device_map="auto",
    trust_remote_code=True
)

tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)
tokenizer.pad_token = tokenizer.eos_token

# Load adapter on top of base model
model = PeftModel.from_pretrained(base_model, ADAPTER_MODEL)
model.eval()

print(f"\nLoaded adapter: {ADAPTER_MODEL}")


# =============================================================================
# 3. INFERENCE WITH ADAPTER
# =============================================================================

def generate(prompt: str, max_new_tokens: int = 100) -> str:
    """Generate text using the adapter model."""
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            temperature=0.7,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id
        )

    return tokenizer.decode(outputs[0], skip_special_tokens=True)


# Test inference
prompt = "Explain quantum computing in simple terms:"
response = generate(prompt)
print(f"\n--- Inference Test ---")
print(f"Prompt: {prompt}")
print(f"Response: {response}")


# =============================================================================
# 4. MERGING ADAPTER INTO BASE MODEL
# =============================================================================

def merge_and_save(base_model_id: str, adapter_id: str, output_dir: str):
    """Merge LoRA adapter into base model and save."""

    # Load base model (full precision for merging)
    base = AutoModelForCausalLM.from_pretrained(
        base_model_id,
        torch_dtype=torch.float16,
        device_map="auto"
    )

    # Load and merge adapter
    merged = PeftModel.from_pretrained(base, adapter_id)
    merged = merged.merge_and_unload()

    # Save merged model
    merged.save_pretrained(output_dir)
    tokenizer = AutoTokenizer.from_pretrained(base_model_id)
    tokenizer.save_pretrained(output_dir)

    print(f"Merged model saved to: {output_dir}")
    return merged

# Example usage (commented to avoid running by default):
# merged_model = merge_and_save(BASE_MODEL, ADAPTER_MODEL, "./merged-model")


# =============================================================================
# 5. CREATING YOUR OWN ADAPTER
# =============================================================================

def create_lora_adapter(base_model_id: str):
    """Create a new LoRA adapter configuration."""

    # LoRA configuration
    lora_config = LoraConfig(
        r=16,  # Rank - higher = more parameters, better quality
        lora_alpha=32,  # Scaling factor
        target_modules=[
            "q_proj", "k_proj", "v_proj", "o_proj",  # Attention
            "gate_proj", "up_proj", "down_proj"  # MLP (for Llama-style)
        ],
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM"
    )

    # Load base model
    base = AutoModelForCausalLM.from_pretrained(
        base_model_id,
        torch_dtype=torch.float16,
        device_map="auto"
    )

    # Apply LoRA
    peft_model = get_peft_model(base, lora_config)

    # Show trainable parameters
    peft_model.print_trainable_parameters()

    return peft_model, lora_config

# Example:
# peft_model, config = create_lora_adapter("mistralai/Mistral-7B-v0.1")


# =============================================================================
# 6. PUSHING ADAPTER TO HUB
# =============================================================================

def push_adapter_to_hub(
    model: PeftModel,
    repo_id: str,
    base_model_id: str
):
    """Push trained adapter to Hugging Face Hub."""

    # Push adapter (not full model - much smaller!)
    model.push_to_hub(repo_id)

    # Create model card
    card_content = f"""---
library_name: peft
base_model: {base_model_id}
license: apache-2.0
tags:
  - lora
  - fine-tuned
---

# LoRA Adapter

This is a LoRA adapter for [{base_model_id}](https://huggingface.co/{base_model_id}).

## Usage

```python
from transformers import AutoModelForCausalLM
from peft import PeftModel

base_model = AutoModelForCausalLM.from_pretrained("{base_model_id}")
model = PeftModel.from_pretrained(base_model, "{repo_id}")
```

## Training Details

- Base model: {base_model_id}
- Method: LoRA
- Rank: 16
"""

    # Upload model card
    api = HfApi()
    api.upload_file(
        path_or_fileobj=card_content.encode(),
        path_in_repo="README.md",
        repo_id=repo_id,
        repo_type="model"
    )

    print(f"Adapter pushed to: https://huggingface.co/{repo_id}")

# Example:
# push_adapter_to_hub(trained_model, "username/my-adapter", BASE_MODEL)


# =============================================================================
# 7. LOADING MULTIPLE ADAPTERS
# =============================================================================

def load_multiple_adapters(base_model_id: str, adapters: dict):
    """Load multiple adapters and switch between them."""

    base = AutoModelForCausalLM.from_pretrained(
        base_model_id,
        torch_dtype=torch.float16,
        device_map="auto"
    )

    # Load first adapter
    first_name = list(adapters.keys())[0]
    model = PeftModel.from_pretrained(
        base,
        adapters[first_name],
        adapter_name=first_name
    )

    # Load additional adapters
    for name, adapter_id in list(adapters.items())[1:]:
        model.load_adapter(adapter_id, adapter_name=name)

    return model

# Example:
# adapters = {
#     "coding": "username/coding-adapter",
#     "chat": "username/chat-adapter",
# }
# multi_model = load_multiple_adapters(BASE_MODEL, adapters)
# multi_model.set_adapter("coding")  # Switch to coding adapter
# multi_model.set_adapter("chat")  # Switch to chat adapter


# =============================================================================
# 8. ADAPTER SIZE COMPARISON
# =============================================================================

def compare_sizes():
    """Compare adapter size vs full model size."""

    # Typical sizes (approximate)
    sizes = {
        "Full Mistral-7B": "14 GB",
        "LoRA r=8": "~20 MB",
        "LoRA r=16": "~40 MB",
        "LoRA r=32": "~80 MB",
        "LoRA r=64": "~160 MB",
        "QLoRA (4-bit base + LoRA)": "~4 GB + adapter"
    }

    print("\n--- Size Comparison ---")
    for name, size in sizes.items():
        print(f"  {name}: {size}")

compare_sizes()

print("\n--- Workflow Complete ---")
