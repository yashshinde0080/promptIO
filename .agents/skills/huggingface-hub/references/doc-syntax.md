# Doc-Builder Markdown Syntax Reference

Complete reference for writing Hugging Face documentation using doc-builder.

## Tips and Warnings

Use blockquote syntax for highlighted notes:

```markdown
> [!TIP]
> Helpful tip for the reader.
>
> Can span multiple lines.

> [!WARNING]
> Important warning or caution.

> [!NOTE]
> Additional context or information.
```

## Internal Links to Code Objects

Link to classes, functions, and methods with auto-generated documentation links:

```markdown
[`ClassName`]                    # Links to class docs
[`~ClassName`]                   # Links with short name (no module path)
[`module.ClassName`]             # Links with full path
[`~module.ClassName`]            # Full path link, short display
[`ClassName.method`]             # Links to method
[`~ClassName.method`]            # Method link, short display
[`function_name`]                # Links to function
```

Examples:
- `[`BertModel`]` - Links to BertModel class
- `[`~transformers.BertModel`]` - Shows "BertModel", links to full path
- `[`PreTrainedModel.from_pretrained`]` - Links to method

## External Links to Other Libraries

Link across Hugging Face libraries:

```markdown
[`transformers.BertModel`]       # Link to transformers library
[`datasets.Dataset`]             # Link to datasets library
[`accelerate.Accelerator`]       # Link to accelerate library
```

## Custom Anchor Links

Headings auto-generate anchors (lowercase, spaces to dashes). Override with:

```markdown
## My Section Title[[custom-anchor]]

Link to it: [see section](#custom-anchor)
```

## Framework-Specific Content

Show different content for PyTorch, TensorFlow, or Flax:

```html
<frameworkcontent>
<pt>
```python
# PyTorch code
import torch
model = torch.nn.Linear(10, 5)
```
</pt>
<tf>
```python
# TensorFlow code
import tensorflow as tf
model = tf.keras.layers.Dense(5)
```
</tf>
<flax>
```python
# Flax code
import flax.linen as nn
model = nn.Dense(5)
```
</flax>
</frameworkcontent>
```

All frameworks are optional. Order doesn't matter.

## Options/Tabs

Show selectable alternatives:

```html
<hfoptions id="installation">
<hfoption id="pip">

Install with pip:
```bash
pip install transformers
```

</hfoption>
<hfoption id="conda">

Install with conda:
```bash
conda install -c huggingface transformers
```

</hfoption>
</hfoptions>
```

Use the same `id` across multiple `<hfoptions>` blocks to sync selection.

## LaTeX Math

Display mode (centered, own line):
```markdown
$$E = mc^2$$

$$\mathrm{MSE} = \frac{1}{n}\sum_{i=1}^{n}(y_i - \hat{y}_i)^2$$
```

Inline mode (within text):
```markdown
The equation \\( E = mc^2 \\) shows mass-energy equivalence.
```

## Code Blocks

Standard markdown code blocks with syntax highlighting:

````markdown
```python
from transformers import AutoModel
model = AutoModel.from_pretrained("bert-base-uncased")
```

```bash
pip install transformers
```

```yaml
model: bert-base-uncased
batch_size: 32
```
````

### Doctest Syntax

Use `>>>` for testable examples:

```python
>>> from transformers import pipeline
>>> classifier = pipeline("sentiment-analysis")
>>> classifier("I love this!")
[{'label': 'POSITIVE', 'score': 0.999...}]
```

### Wrap Code Blocks

Force text wrapping instead of horizontal scroll:

```markdown
<!-- WRAP CODE BLOCKS -->

Your content here with long code lines that will wrap...
```

## Stretch Tables

Make tables span full width:

```markdown
<!-- STRETCH TABLES -->

| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Data     | Data     | Data     |
```

## Autodoc (API Documentation)

Auto-generate documentation from docstrings:

```markdown
[[autodoc]] BertModel

[[autodoc]] BertTokenizer
    - build_inputs_with_special_tokens
    - get_special_tokens_mask

[[autodoc]] Pipeline
    - all
    - __call__
```

## Docstring Format

Write docstrings in Google format with markdown:

```python
def my_function(input_ids, attention_mask=None, labels=None):
    """
    Process input tensors through the model.

    Args:
        input_ids (`torch.LongTensor` of shape `(batch_size, sequence_length)`):
            Indices of input sequence tokens in the vocabulary.

            Indices can be obtained using [`AutoTokenizer`].
        attention_mask (`torch.FloatTensor`, *optional*):
            Mask to avoid attention on padding tokens.
        labels (`torch.LongTensor`, *optional*):
            Labels for computing loss.

    Returns:
        [`ModelOutput`]: Model outputs including loss and logits.

    Raises:
        `ValueError`: If input_ids and labels have mismatched shapes.

    Example:
        ```python
        >>> from transformers import AutoModel
        >>> model = AutoModel.from_pretrained("bert-base-uncased")
        >>> outputs = model(input_ids)
        ```
    """
```

### Parameter Typing

```python
Args:
    x (`str`):                           # Required string
    y (`int`, *optional*):               # Optional, defaults to None
    z (`float`, *optional*, defaults to 1.0):  # Optional with default
    config ([`BertConfig`]):             # Link to config class
```

### Returns/Yields

```python
Returns:
    `List[int]`: A list of token indices.

Returns:
    `tuple(torch.FloatTensor)` comprising:
    - **loss** (`torch.FloatTensor` of shape `(1,)`) -- The loss value.
    - **logits** (`torch.FloatTensor` of shape `(batch_size, num_labels)`) -- Predictions.

Yields:
    `tuple[str, bytes]`: Filename and file contents.
```

## Version Directives

Mark added, changed, or deprecated features:

```markdown
<Added version="4.30.0">

New feature description.

</Added>

<Changed version="4.30.0">

What changed in this version.

</Changed>

<Deprecated version="4.30.0">

Use `new_function` instead.

</Deprecated>
```

## Light/Dark Mode Images

Show different images based on theme:

```markdown
<!-- Using URI fragments (for uploaded images) -->
![Logo](https://cdn.../logo-light.png#hf-light-mode-only)
![Logo](https://cdn.../logo-dark.png#hf-dark-mode-only)

<!-- Using Tailwind classes (for hosted images) -->
<img class="dark:hidden" src="logo-light.png" alt="Logo" />
<img class="hidden dark:block" src="logo-dark.png" alt="Logo" />
```

## Notebook Conversion

Enable Colab notebook generation:

```markdown
[[open-in-colab]]

# Tutorial Title

This tutorial will be converted to a Colab notebook...
```

## Literal Include (File References)

Include code from external files:

```html
<literalinclude>
{"path": "./examples/example.py",
"language": "python",
"start-after": "START example",
"end-before": "END example",
"dedent": 4}
</literalinclude>
```

## Common Patterns

### Link to External Documentation

```markdown
For more details, see the [Transformers documentation](https://huggingface.co/docs/transformers).
```

### Reference Related Guides

```markdown
> [!TIP]
> Check out the [quickstart guide](./quickstart) for a complete example.
```

### Document Configuration Options

```markdown
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `hidden_size` | `int` | `768` | Dimensionality of encoder layers. |
| `num_attention_heads` | `int` | `12` | Number of attention heads. |
```
