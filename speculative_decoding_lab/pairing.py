from __future__ import annotations

from collections import defaultdict


def _key(row: dict) -> tuple:
    value = row.get("pair_key")
    if value is not None:
        return tuple(value)
    return (
        row["target_model"],
        row["prompt_file"],
        row["output_tokens_requested"],
        row["repeat"],
        row["temperature"],
    )


def pair_with_baseline(rows: list[dict]) -> list[dict]:
    controls = {
        _key(row): row
        for row in rows
        if row.get("ok") and row.get("baseline")
    }
    output = []
    for row in rows:
        if not row.get("ok") or row.get("baseline"):
            continue
        baseline = controls.get(_key(row))
        if not baseline:
            continue
        base_time = float(baseline["elapsed_seconds"])
        spec_time = float(row["elapsed_seconds"])
        output.append({
            "baseline_job_id": baseline["job_id"],
            "speculative_job_id": row["job_id"],
            "target_model": row["target_model"],
            "draft_model": row["draft_model"],
            "prompt_file": row["prompt_file"],
            "spec_type": row["spec_type"],
            "draft_n_max": row["draft_n_max"],
            "repeat": row["repeat"],
            "baseline_seconds": base_time,
            "speculative_seconds": spec_time,
            "speedup": None if spec_time <= 0 else base_time / spec_time,
            "elapsed_delta_seconds": spec_time - base_time,
            "acceptance_ratio": row.get("acceptance_ratio"),
            "drafted_tokens": row.get("drafted_tokens"),
            "accepted_tokens": row.get("accepted_tokens"),
            "baseline_eval_tps": baseline.get("eval_tps"),
            "speculative_eval_tps": row.get("eval_tps"),
        })
    return output
