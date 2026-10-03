# speculative-decoding-lab

A local experiment harness for comparing ordinary decoding with speculative decoding in llama.cpp-style runtimes.

Speculative decoding adds a second model or draft mechanism in the hope that cheap candidate tokens can be accepted by the target model faster than the target would decode them alone. The extra model, draft depth and acceptance behaviour also add overhead, so the optimization is workload-dependent.

This repository treats speculative decoding as an experiment matrix rather than an assumed speedup.

## Questions the lab is built around

- when does a small draft model improve target-model throughput?
- how sensitive is the result to the maximum number of drafted tokens?
- does a longer prompt change the break-even point?
- how much memory does the target + draft pair require?
- do different speculative modes behave differently on the same workload?
- when does the baseline target-only run remain faster?
- how stable is the speedup over repeated runs?

## Current llama.cpp-style controls

The command planner supports the modern speculative arguments:

- `--spec-type`
- `--spec-draft-model`
- `--spec-draft-n-min`
- `--spec-draft-n-max`
- `--spec-draft-ngl`

A baseline job is always generated with speculative decoding disabled.

## Workflow

```text
experiment manifest
       |
       v
 target x draft x prompt x depth matrix
       |
       +--> target-only baseline
       |
       +--> speculative configurations
       |
       v
   llama-cli runner
       |
       +--> wall-clock duration
       +--> stdout / stderr
       +--> prompt/decode timing
       +--> drafted / accepted counters when exposed
       +--> exact command
       |
       v
      raw JSONL
       |
       +--> pair with baseline
       +--> acceptance ratio
       +--> speedup ratio
       +--> win / tie / loss
       +--> prompt-length report
```

## Example

```bash
python -m speculative_decoding_lab plan \
  configs/experiment.example.json \
  > runs/plan.jsonl

python -m speculative_decoding_lab run \
  runs/plan.jsonl \
  --out runs/raw.jsonl

python -m speculative_decoding_lab report runs/raw.jsonl
```

## Manifest

```json
{
  "target_models": ["models/target.gguf"],
  "draft_models": ["models/draft.gguf"],
  "prompt_files": ["prompts/short.txt", "prompts/long.txt"],
  "spec_types": ["draft-simple"],
  "draft_n_max": [2, 4, 8],
  "output_tokens": [128, 512],
  "repeats": 3
}
```

The planner emits target-only control jobs for every target/prompt/output combination in addition to speculative jobs.

## Result interpretation

A speculative configuration is only considered faster relative to its paired baseline using the same target model, prompt, generation budget and repeat.

The report keeps several signals separate:

- elapsed wall time
- target-side reported generation throughput when parseable
- drafted-token count
- accepted-token count
- acceptance ratio
- paired wall-time speedup
- run-to-run variation

A high acceptance ratio does not guarantee a wall-clock improvement if the draft model itself is expensive.

## Repository layout

- `planner.py` — baseline + speculative matrix expansion
- `commands.py` — llama.cpp command construction
- `parsing.py` — timing and speculative-counter parsing
- `runner.py` — subprocess execution and raw records
- `pairing.py` — baseline/speculative matching
- `report.py` — grouped speedup and acceptance summaries
- `io.py` — JSONL artifacts
- `configs/` — experiment manifests
- `prompts/` — repeatable workload fixtures
- `docs/` — methodology and interpretation notes
- `tests/` — planner/parser/report tests without model files

No model weights or precomputed benchmark claims are committed.

Maintained by **Aarnav Saboo**.
