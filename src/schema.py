"""
This file contains the schema for the input parameters for the API. 
"""
INPUT_SCHEMA = {
    "prompt": {
        "type": str,
        "required": True,
    },
    "max_tokens": {"type": int, "required": False, "default": 256},
    "n": {"type": int, "required": False, "default": 1},
    "best_of": {"type": int, "required": False, "default": None},
    "presence_penalty": {"type": float, "required": False, "default": 0.0},
    "repetition_penalty": {"type": float, "required": False, "default": None},
    "frequency_penalty": {"type": float, "required": False, "default": 0.0},
    "temperature": {"type": float, "required": False, "default": 1.31},
    "top_p": {"type": float, "required": False, "default": 0.14},
    "top_k": {"type": int, "required": False, "default": 49},
    "use_beam_search": {"type": bool, "required": False, "default": False},
    "length_penalty": {"type": float, "required": False, "default": 0.0},
    "early_stopping": {"type": bool, "required": False, "default": False},
    "stop": {"type": str, "required": False, "default": None},
    "stop_token_ids": {"type": int, "required": False, "default": None},
    "ignore_eos": {"type": bool, "required": False, "default": False},
    "logprobs": {"type": float, "required": False, "default": None},
    "prompt_logprobs": {"type": float, "required": False, "default": None},
    "skip_special_tokens": {"type": bool, "required": False, "default": True},
    "logits_processors": {"type": list, "required": False, "default": None},
    "spaces_between_special_tokens": {
        "type": bool,
        "required": False,
        "default": True,
    },
}
