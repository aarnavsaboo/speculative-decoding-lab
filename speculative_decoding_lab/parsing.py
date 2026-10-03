from __future__ import annotations

import re


NUMBER = r"([0-9]+(?:\.[0-9]+)?)"


def _last(pattern: str, text: str) -> float | None:
    matches = re.findall(pattern, text, flags=re.IGNORECASE)
    if not matches:
        return None
    value = matches[-1]
    if isinstance(value, tuple):
        value = value[-1]
    return float(value)


def parse_perf(text: str) -> dict:
    # llama.cpp output wording has changed over time, so parsing is
    # deliberately permissive and raw output is always retained too.
    prompt_tps = _last(r"prompt eval time.*?\b" + NUMBER + r"\s+tokens per second", text)
    eval_tps = _last(r"eval time.*?\b" + NUMBER + r"\s+tokens per second", text)

    drafted = _last(r"(?:drafted|n_drafted)\D+" + NUMBER, text)
    accepted = _last(r"(?:accepted|n_accept(?:ed)?)\D+" + NUMBER, text)

    # Some builds print compact counters such as "drafted = 20, accepted = 14".
    if drafted is None:
        drafted = _last(r"draft(?:ed)?\s*[=:]\s*" + NUMBER, text)
    if accepted is None:
        accepted = _last(r"accept(?:ed)?\s*[=:]\s*" + NUMBER, text)

    acceptance = None
    if drafted is not None and drafted > 0 and accepted is not None:
        acceptance = accepted / drafted

    return {
        "prompt_tps": prompt_tps,
        "eval_tps": eval_tps,
        "drafted_tokens": None if drafted is None else int(drafted),
        "accepted_tokens": None if accepted is None else int(accepted),
        "acceptance_ratio": acceptance,
    }
