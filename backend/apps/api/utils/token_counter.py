try:
    import tiktoken

    _tokenizer = tiktoken.get_encoding("cl100k_base")

    def count_tokens(text: str, model: str = "gpt-4") -> int:
        try:
            return len(_tokenizer.encode(text))
        except Exception:
            return len(text.split()) * 4 // 3

except ImportError:
    def count_tokens(text: str, model: str = "gpt-4") -> int:
        return len(text.split()) * 4 // 3


def estimate_cost(tokens: int, model: str) -> float:
    cost_map = {
        "openai/gpt-4o": 0.005,
        "openai/gpt-4o-mini": 0.00015,
        "anthropic/claude-3.5-sonnet": 0.003,
    }
    cost_per_1k = cost_map.get(model, 0.002)
    return (tokens / 1000) * cost_per_1k