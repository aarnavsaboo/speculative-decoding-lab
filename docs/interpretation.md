# Interpreting results

A speedup value above 1 means the speculative run finished faster than its paired target-only baseline.

Three common outcomes are useful:

1. **high acceptance and real speedup** — the draft model is cheap enough and predicts useful continuations;
2. **high acceptance but little speedup** — draft overhead or memory pressure offsets the saved target work;
3. **low acceptance and slowdown** — the extra draft computation is mostly discarded.

The third case is not a broken experiment. It is often the most useful boundary to record.
