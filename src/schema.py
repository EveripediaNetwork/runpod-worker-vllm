INPUT_SCHEMA = {
    "prompt": {
        "type": str,
        "required": True,
    },
    "temperature": {"type": float, "required": False, "default": 1.31},
    "top_p": {"type": float, "required": False, "default": 0.14},
    "top_k": {"type": int, "required": False, "default": 49},
    "n": {"type": int, "required": False, "default": 1},
    "best_of": {"type": int, "required": False, "default": None},
    "presence_penalty": {"type": float, "required": False, "default": 0.0},
    "frequency_penalty": {"type": float, "required": False, "default": 0.0},
    "use_beam_search": {"type": bool, "required": False, "default": False},
    "stop": {"type": str, "required": False, "default": None},
    "ignore_eos": {"type": bool, "required": False, "default": False},
    "max_tokens": {"type": int, "required": False, "default": 256},
    "logprobs": {"type": float, "required": False, "default": None},
}
