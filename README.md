# AI Act Lab

A learning project: fine-tune a small open language model, on a laptop, to triage
AI systems under the EU AI Act.

You describe an AI system in plain English. The model returns a structured record:
risk tier, the Annex III category if high-risk, the article it relied on, a
one-sentence reason, or an honest "needs human review". A small, maintained lookup
table, not the model, attaches the current dates and duties for that tier.

**Status:** started 2026-10-26. Expert roster and impact map approved
(`impact-map.md`); requirements next. Target date 16 November 2026. Built with the
GVM pipeline, one phase at a time, owner review between phases.

Read first:

- `docs/00-plan.md`: why this project, the design decision that matters, the stages,
  and what the research settled
- `docs/01-glossary.md`: the words, in plain English
- `docs/02-reading-list-slm-fine-tuning.md`: the papers worth knowing, verified and ranked
  for this project
- `docs/learning/`: the owner's own textbook, one entry per step
- `notebook/`: one entry per training run, once training starts

**Hardware this runs on:** Apple M2, 8 GB memory. Everything in this repo must fit that.

**Honesty:** a 0.8B-parameter model is not a lawyer. The target is a triage assistant
that is right about nine times in ten on clean descriptions and hands the rest to a
human. This is a learning project, not legal advice.
