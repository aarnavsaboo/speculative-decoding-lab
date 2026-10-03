from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha1
from itertools import product
from typing import Any
import json


@dataclass(frozen=True)
class Job:
    id: str
    target_model: str
    draft_model: str | None
    prompt_file: str
    spec_type: str
    draft_n_min: int
    draft_n_max: int
    output_tokens: int
    repeat: int
    target_gpu_layers: str
    draft_gpu_layers: str
    temperature: float

    @property
    def baseline(self) -> bool:
        return self.spec_type == "none"

    def pair_key(self) -> tuple:
        return (
            self.target_model,
            self.prompt_file,
            self.output_tokens,
            self.repeat,
            self.temperature,
        )

    def to_dict(self) -> dict[str, Any]:
        row = asdict(self)
        row["baseline"] = self.baseline
        return row


def _values(value):
    return value if isinstance(value, list) else [value]


def _make(**payload) -> Job:
    canonical = dict(payload)
    encoded = json.dumps(canonical, sort_keys=True).encode()
    return Job(id=sha1(encoded).hexdigest()[:16], **canonical)


def expand(config: dict[str, Any]) -> list[Job]:
    targets = _values(config["target_models"])
    drafts = _values(config.get("draft_models", []))
    prompts = _values(config["prompt_files"])
    outputs = _values(config.get("output_tokens", [256]))
    repeats = range(int(config.get("repeats", 3)))
    temperatures = _values(config.get("temperature", [0.0]))
    target_gpu = str(config.get("target_gpu_layers", "all"))
    draft_gpu = str(config.get("draft_gpu_layers", "all"))

    jobs: list[Job] = []

    # One target-only control for every workload cell.
    for target, prompt, output, repeat, temp in product(
        targets, prompts, outputs, repeats, temperatures
    ):
        jobs.append(_make(
            target_model=str(target),
            draft_model=None,
            prompt_file=str(prompt),
            spec_type="none",
            draft_n_min=0,
            draft_n_max=0,
            output_tokens=int(output),
            repeat=int(repeat),
            target_gpu_layers=target_gpu,
            draft_gpu_layers=draft_gpu,
            temperature=float(temp),
        ))

    spec_types = _values(config.get("spec_types", ["draft-simple"]))
    mins = _values(config.get("draft_n_min", [0]))
    maxes = _values(config.get("draft_n_max", [3]))

    for target, draft, prompt, spec_type, n_min, n_max, output, repeat, temp in product(
        targets, drafts, prompts, spec_types, mins, maxes, outputs, repeats, temperatures
    ):
        if int(n_min) > int(n_max):
            raise ValueError("draft_n_min cannot exceed draft_n_max")
        jobs.append(_make(
            target_model=str(target),
            draft_model=str(draft),
            prompt_file=str(prompt),
            spec_type=str(spec_type),
            draft_n_min=int(n_min),
            draft_n_max=int(n_max),
            output_tokens=int(output),
            repeat=int(repeat),
            target_gpu_layers=target_gpu,
            draft_gpu_layers=draft_gpu,
            temperature=float(temp),
        ))

    return jobs
