from pathlib import Path

from .planner import Job


def build(job: Job, binary: str = "llama-cli") -> list[str]:
    prompt = Path(job.prompt_file).read_text(encoding="utf-8")
    command = [
        binary,
        "-m", job.target_model,
        "-p", prompt,
        "-n", str(job.output_tokens),
        "--temp", str(job.temperature),
        "-ngl", job.target_gpu_layers,
        "--no-display-prompt",
    ]

    if not job.baseline:
        if not job.draft_model:
            raise ValueError("speculative job requires a draft model")
        command += [
            "--spec-type", job.spec_type,
            "--spec-draft-model", job.draft_model,
            "--spec-draft-n-min", str(job.draft_n_min),
            "--spec-draft-n-max", str(job.draft_n_max),
            "--spec-draft-ngl", job.draft_gpu_layers,
        ]

    return command
