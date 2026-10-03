from __future__ import annotations

from time import perf_counter
import subprocess

from .commands import build
from .parsing import parse_perf
from .planner import Job


def run(job: Job, binary: str = "llama-cli") -> dict:
    command = build(job, binary)
    started = perf_counter()
    proc = subprocess.run(command, text=True, capture_output=True)
    elapsed = perf_counter() - started
    combined = proc.stderr + "\n" + proc.stdout
    parsed = parse_perf(combined)

    return {
        "job_id": job.id,
        "pair_key": list(job.pair_key()),
        "baseline": job.baseline,
        "target_model": job.target_model,
        "draft_model": job.draft_model,
        "prompt_file": job.prompt_file,
        "spec_type": job.spec_type,
        "draft_n_min": job.draft_n_min,
        "draft_n_max": job.draft_n_max,
        "output_tokens_requested": job.output_tokens,
        "repeat": job.repeat,
        "temperature": job.temperature,
        "elapsed_seconds": elapsed,
        "returncode": proc.returncode,
        "ok": proc.returncode == 0,
        "command": command,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
        **parsed,
    }
