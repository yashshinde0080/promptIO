# Advanced Model Formats

Reference for GGUF, PEFT/LoRA adapters, quantization, and integration with local inference tools.

## GGUF Format

GGUF is a binary format optimized for fast loading and inference with llama.cpp and compatible tools.

### Finding GGUF Models

Browse GGUF models: https://huggingface.co/models?library=gguf

Convert your own models: https://huggingface.co/spaces/ggml-org/gguf-my-repo

### Quantization Types

| Type | Bits/Weight | Quality | Speed | Use Case |
|------|-------------|---------|-------|----------|
| F16 | 16 | Highest | Slow | Reference quality |
| Q8_0 | 8 | Very High | Fast | Good balance |
| Q6_K | 6.5 | High | Fast | Recommended default |
| Q5_K | 5.5 | Good | Faster | Memory constrained |
| Q4_K | 4.5 | Acceptable | Fastest | Low memory |
| Q3_K | 3.4 | Lower | Fastest | Minimum viable |
| Q2_K | 2.6 | Lowest | Fastest | Experimental |

**I-Quants (Importance Matrix):**
- `IQ4_XS`, `IQ3_S`, `IQ2_XXS` - Better quality at same bit rate
- Requires importance matrix during quantization

### Using with llama.cpp

```bash
# Download GGUF model
huggingface-cli download TheBloke/Llama-2-7B-Chat-GGUF \
  llama-2-7b-chat.Q4_K_M.gguf \
  --local-dir ./models

# Run with llama.cpp
./llama-cli -m ./models/llama-2-7b-chat.Q4_K_M.gguf \
  -p "Hello, how are you?" \
  -n 100
```

### Using with Ollama

```bash
# Create Modelfile
cat > Modelfile << 'EOF'
FROM hf.co/TheBloke/Llama-2-7B-Chat-GGUF:Q4_K_M
EOF

# Create and run
ollama create my-llama -f Modelfile
ollama run my-llama "Hello!"
```

Or use direct HF reference:

```bash
ollama run hf.co/TheBloke/Llama-2-7B-Chat-GGUF:Q4_K_M
```

### Using with LM Studio

1. Search for model in LM Studio
2. Select quantization level (Q4_K_M recommended)
3. Download and load model
4. Use chat interface or local API

### Parsing GGUF Metadata (JavaScript)

```javascript
import { gguf } from "@huggingface/gguf";

const URL = "https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/resolve/main/llama-2-7b-chat.Q4_K_M.gguf";

const { metadata, tensorInfos } = await gguf(URL);
console.log(metadata);  // Model configuration
console.log(tensorInfos);  // Tensor shapes and types
```

## PEFT / LoRA Adapters

PEFT (Parameter-Efficient Fine-Tuning) creates small adapter weights instead of full model copies.

### Finding Adapters

Browse PEFT models: https://huggingface.co/models?library=peft

### Loading Adapters

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

# Load base model
base_model = "mistralai/Mistral-7B-v0.1"
adapter_model = "username/my-mistral-adapter"

model = AutoModelForCausalLM.from_pretrained(base_model)
model = PeftModel.from_pretrained(model, adapter_model)
tokenizer = AutoTokenizer.from_pretrained(base_model)

# Use model
inputs = tokenizer("Hello, how are you?", return_tensors="pt")
outputs = model.generate(**inputs, max_new_tokens=50)
print(tokenizer.decode(outputs[0]))
```

### Creating Adapters

```python
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments
from peft import LoraConfig, get_peft_model, TaskType
from trl import SFTTrainer

# Load base model
model = AutoModelForCausalLM.from_pretrained(
    "mistralai/Mistral-7B-v0.1",
    load_in_8bit=True,  # or load_in_4bit=True
    device_map="auto"
)

# Configure LoRA
lora_config = LoraConfig(
    r=16,  # Rank
    lora_alpha=32,
    target_modules=["q_proj", "v_proj", "k_proj", "o_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type=TaskType.CAUSAL_LM
)

# Apply LoRA
model = get_peft_model(model, lora_config)
model.print_trainable_parameters()

# Train with SFTTrainer (from trl library)
# trainer = SFTTrainer(...)
# trainer.train()
```

### Merging Adapters

```python
from peft import PeftModel
from transformers import AutoModelForCausalLM

# Load and merge
base_model = AutoModelForCausalLM.from_pretrained("mistralai/Mistral-7B-v0.1")
model = PeftModel.from_pretrained(base_model, "username/my-adapter")
merged_model = model.merge_and_unload()

# Save merged model
merged_model.save_pretrained("./merged-model")

# Push to Hub
merged_model.push_to_hub("username/my-merged-model")
```

### Adapter Model Card

```yaml
---
library_name: peft
base_model: mistralai/Mistral-7B-v0.1
license: apache-2.0
tags:
  - lora
  - fine-tuned
datasets:
  - my-dataset
---

# LoRA Adapter for Mistral-7B

This adapter was fine-tuned on [dataset] for [task].

## Usage

```python
from peft import PeftModel
from transformers import AutoModelForCausalLM

model = AutoModelForCausalLM.from_pretrained("mistralai/Mistral-7B-v0.1")
model = PeftModel.from_pretrained(model, "username/this-adapter")
```
```

## Quantization Methods

### BitsAndBytes (QLoRA)

```python
from transformers import AutoModelForCausalLM, BitsAndBytesConfig

# 4-bit quantization config
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype="float16",
    bnb_4bit_use_double_quant=True
)

model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-3.1-8B",
    quantization_config=bnb_config,
    device_map="auto"
)
```

### GPTQ

```python
from transformers import AutoModelForCausalLM, GPTQConfig

gptq_config = GPTQConfig(bits=4, dataset="c4", tokenizer=tokenizer)

model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-3.1-8B",
    quantization_config=gptq_config,
    device_map="auto"
)
```

### AWQ

```python
from transformers import AutoModelForCausalLM

# Load pre-quantized AWQ model
model = AutoModelForCausalLM.from_pretrained(
    "TheBloke/Llama-2-7B-AWQ",
    device_map="auto"
)
```

## SafeTensors Format

SafeTensors is the recommended format for model weights (secure, fast loading).

### Converting to SafeTensors

```python
from safetensors.torch import save_file, load_file
import torch

# Save
state_dict = model.state_dict()
save_file(state_dict, "model.safetensors")

# Load
state_dict = load_file("model.safetensors")
model.load_state_dict(state_dict)
```

### Checking if Model Uses SafeTensors

Models with `model.safetensors` instead of `pytorch_model.bin` use the safer format.

## Model Sharding

Large models are automatically sharded:

```
model/
├── model-00001-of-00003.safetensors
├── model-00002-of-00003.safetensors
├── model-00003-of-00003.safetensors
└── model.safetensors.index.json
```

Load sharded models normally - `from_pretrained` handles it automatically.

## Format Comparison

| Format | Size | Load Speed | Security | Use Case |
|--------|------|------------|----------|----------|
| SafeTensors | Base | Fastest | Secure | Default choice |
| PyTorch .bin | Base | Fast | Pickle risk | Legacy |
| GGUF | Quantized | Fast | Secure | Local inference |
| ONNX | Optimized | Very Fast | Secure | Production/Mobile |

## Resources

- GGUF spec: https://github.com/ggerganov/ggml/blob/master/docs/gguf.md
- PEFT docs: https://huggingface.co/docs/peft
- BitsAndBytes: https://github.com/TimDettmers/bitsandbytes
- SafeTensors: https://huggingface.co/docs/safetensors
