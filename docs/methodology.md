# Methodology

Speculative decoding comparisons should be paired.

A speculative run and its baseline should use the same target model, prompt, output budget, temperature and repetition index. The draft model and speculative settings are the variables.

Wall-clock time is the primary comparison because an acceptance ratio alone does not include the cost of running the draft model.

Useful sweeps vary one of the following at a time:

- draft model;
- maximum drafted tokens;
- prompt length;
- output length;
- quantization;
- target/draft device placement.

Keep raw stdout and stderr because runtime versions may expose different counters over time.
