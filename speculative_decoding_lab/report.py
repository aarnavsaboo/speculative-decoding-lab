from __future__ import annotations

from collections import defaultdict
from statistics import median

from .pairing import pair_with_baseline


def summarize(rows: list[dict]) -> list[dict]:
    pairs = pair_with_baseline(rows)
    groups = defaultdict(list)
    for row in pairs:
        groups[
            (
                row["target_model"],
                row["draft_model"],
                row["prompt_file"],
                row["spec_type"],
                row["draft_n_max"],
            )
        ].append(row)

    output = []
    for key, group in sorted(groups.items(), key=lambda item: str(item[0])):
        target, draft, prompt, spec_type, draft_n_max = key
        speedups = [float(x["speedup"]) for x in group if x.get("speedup") is not None]
        acceptance = [
            float(x["acceptance_ratio"])
            for x in group
            if x.get("acceptance_ratio") is not None
        ]
        output.append({
            "target_model": target,
            "draft_model": draft,
            "prompt_file": prompt,
            "spec_type": spec_type,
            "draft_n_max": draft_n_max,
            "pairs": len(group),
            "median_speedup": None if not speedups else median(speedups),
            "wins": sum(x > 1 for x in speedups),
            "ties": sum(x == 1 for x in speedups),
            "losses": sum(x < 1 for x in speedups),
            "median_acceptance_ratio": None if not acceptance else median(acceptance),
        })
    return output
