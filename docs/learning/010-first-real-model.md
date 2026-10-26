# 010. A real model on this Mac

**Step:** `/gvm-build` P1-C02. **Date:** 2026-10-26.

## The lesson before the step

We loaded the smallest candidate, Qwen3.5-0.8B compressed to 4 bits, in a
separate child process, asked it to classify one made-up system, and measured
time and memory. Testing the riskiest join first is called a tracer bullet.

## What happened

| Measure on this Mac | Result |
|---|---|
| Model size on disk | 652 MB |
| Loading (with safety checks) | about 2.5 seconds |
| One answer | about 1.6 seconds |
| Peak memory | 0.67 GB of 8 GB |

- **It fits easily.** The borrowed estimate for training was 3.9 GB; answering
  takes 0.67 GB. Training will use more, and we will measure it.
- **Its answer was wrong.** It called an email sorter "transparency-only" when it
  should be minimal, and filled fields with nonsense ("art50" as an Annex III
  area). This is the untrained starting point. It is exactly what fine-tuning,
  and our measurements, are for.
- **Before downloading, we checked the listing.** The model is a vision-and-text
  model, converted with a different tool than the one we use, and its listing
  named a "Base" model. Both were checked before you were asked.
- **Supply-chain safety.** The download is pinned to one exact version; every
  weights file's fingerprint (SHA-256) is checked before loading; any code or
  pickle file in the download is refused; the model is never allowed to run its
  own code.

## Terms that came up

- **Quantisation (4-bit).** Storing each weight in 4 bits instead of 16. About a
  quarter of the memory for a small loss of precision.
- **Revision.** The exact version of a model repository, named by a 40-character
  code. "main" would mean "whatever is newest", which can change under you.
- **SHA-256 fingerprint.** A 64-character code computed from a file; any change
  to the file changes it.
- **Chat template.** The special markers a model family expects around a
  conversation. The library applies them.
- **Peak memory.** The most memory used at any moment, which is what decides
  whether something fits.

## Try it yourself (optional, about 10 seconds)

```bash
.venv/bin/python -m lab.bakeoff smoke --model qwen3.5-0.8b
```

You should see the load and answer times, the peak memory, and the model's answer.

## What you just learned

- A 0.8-billion-parameter model answers on a laptop in under two seconds.
- An untrained small model can produce confident nonsense in the right shape.
- Pinning versions and checking fingerprints is how you know you are running
  what you think you are running.

## Check questions

1. Why run the model in a separate child process?
2. The model's answer "parsed" but was wrong. What will catch the garbled fields?
3. Why is pinning to an exact revision safer than "main"?
