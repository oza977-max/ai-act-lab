# AI Act Lab

A learning project, built in public: fine-tune a small open language model, on a
laptop, to triage AI systems under the EU AI Act. Everything here, including the
mistakes, is written so that someone else can learn from it.

You describe an AI system in plain English. The model returns a structured record:
risk tier, the Annex III category if high-risk, the article it relied on, a
one-sentence reason, or an honest "needs human review". A small, maintained lookup
table, not the model, attaches the current dates and duties for that tier.

**Honesty:** a 0.8B-parameter model is not a lawyer. The target is a triage assistant
that is right about nine times in ten on the cases it answers, hands the rest to a
human, and runs with no data leaving the laptop. This is a learning project, not
legal advice.

**Status (2026-10-27):** planning complete and reviewed; build in progress. The
evaluation tool works and a first model runs on the laptop. Next: a practice
fine-tune. Target date 16 November 2026.

---

## How we approached it

### 1. Start from one design decision

The EU AI Act's dates changed in July 2026 (Regulation (EU) 2026/1744, the Digital
Omnibus on AI) and will change again. A model trained on dates would recite stale
ones with full confidence. So **the model learns judgement and output format; dates
and duties live in a maintained lookup table with sources and "last checked"
dates.** Published evidence supports this: fine-tuning a model on facts it does not
already know makes it hallucinate more (Gekhman et al., EMNLP 2024).

### 2. Use a method that forces evidence before code

The project follows the Grounded Vibe Methodology: one phase at a time, each
reviewed by the owner before the next, every decision tied to a named published
source. The phases so far, each with its artefact:

| Phase | What it produced | Read |
|---|---|---|
| Expert calibration | The reference shelf: 22 authorities, each scored twice independently | `init/init-001.md`, `scoring-reports/` |
| Reading list | 60 arXiv papers on small-model fine-tuning, each checked at source | `docs/02-reading-list-slm-fine-tuning.md` |
| Impact map | Two measured goals, three people, eighteen deliverables | `impact-map.md` |
| Requirements | 45 testable requirements for the first slice | `requirements/requirements.md` |
| Test cases | 64 tests written before any code | `test-cases/test-cases.md` |
| Technical spec | Four short specs and an 18-chunk build guide | `specs/` |
| Design review | Five independent reviewers; 59 findings, all fixed | `design-review/design-review-001.html` |
| Build | Test-first code, each chunk reviewed until clean | `build/handovers/` |

### 3. Measure before training

The goals are numbers, not adjectives: on a held-out test, at least 90% right on the
cases the model answers, at least 75% of cases answered, and a gain over the
untrained model larger than its margin of error. "Needs human review" is a designed
output, scored with two numbers together (accuracy when answering, and share
answered), because accuracy alone can be bought by refusing everything (Geifman and
El-Yaniv, NeurIPS 2017). Every number carries a 95% interval (Miller, 2024).

The measuring stick is built first: a labelling guideline, 100 hand-checked "gold"
cases, and an evaluation tool proven on a ten-case set small enough to count by hand.

### 4. Compare base models instead of assuming one

Four candidates under 2B parameters are measured on the same cases before choosing:
Qwen3.5-0.8B, Llama 3.2 1B, Gemma 3 1B, and EuroLLM-1.7B (EU-funded, Apache 2.0).
Licence and provenance criteria for a European compliance audience are written down
before any result is seen.

### 5. Get hands-on early

A practice fine-tune on public data (the CC-BY-4.0 AI Act Evaluation Benchmark,
Davvetas et al., 2026) comes before the gold set, so the owner learns the training
loop in the first week. It is labelled practice: its numbers decide nothing.

## What we measured so far

| On an Apple M2 with 8 GB | Result |
|---|---|
| Qwen3.5-0.8B, 4-bit: download | 652 MB |
| Loading, including safety checks | about 2.5 s |
| One answer | about 1.6 s |
| Peak memory while answering | 0.67 GB |
| Untrained answer to a simple case | Wrong tier, garbled fields (the starting point) |

## What went wrong, and how it was caught

Kept here on purpose: these are the most useful lessons.

- **A reviewer can be wrong, and so can we.** A paper's figure in the reading list
  ("tens to a few hundred examples per task") came from an older version; checking
  the source before citing it found "a few hundred to a thousand". A verification
  pass also recorded a dataset as unlicensed; a direct check found CC-BY-4.0. Both
  are corrected, with changelog rows.
- **Specs that read well can still be unbuildable.** The design review found that
  "fits in 8 GB" had no actual limit and that the review spreadsheet could not hold
  every field. Both would have broken the build.
- **A safety check you must remember to run is not a check.** The confidentiality
  guard started as a word list run by hand; reviews found that file names with
  spaces and lines starting "++" slipped past it. It is now a git pre-commit hook
  with a private, never-committed name list, and tested.
- **Download listings need checking.** The first model is a vision-and-text model
  converted with a different tool, and its listing named a base model. Both were
  checked before downloading; every weights file is now fingerprint-verified.
- **Time estimates.** Early deadline options suggested months; the honest estimate
  is 15 to 20 hours of the owner's time over two to three weeks.

## Learn along

- `docs/learning/000-the-whole-picture.md`: the whole project in plain English, as a
  six-step story about training a junior colleague. Start here.
- `docs/learning/`: the owner's textbook, one entry per step, each with a lesson,
  what happened, the terms, and check questions.
- `docs/01-glossary.md`: the words, in plain English.
- `docs/00-plan.md`: the original plan and the decisions log.
- `notebook/`: one entry per training run (from the practice run on).

## Run it yourself

On an Apple Silicon Mac with Python 3.13:

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python -m pytest
.venv/bin/python -m lab.evaluate --gold tests/fixtures/eval-10/gold.jsonl --run tests/fixtures/eval-10/run/
.venv/bin/python -m lab.bakeoff smoke --model qwen3.5-0.8b
```

The last command downloads about 650 MB of model weights on first use.

## Ground rules this project keeps

- Public regulation text and freshly written, fictional cases only. Nothing from any
  workplace, ever; a pre-commit hook enforces it.
- Report what was measured, including failures.
- Model weights and adapters are never committed; datasets and results are.

## Credits

Built with Claude Code (Anthropic) under the Grounded Vibe Methodology. Practice
data: AI Act Evaluation Benchmark by Davvetas, Papademas, Ziouvelou and
Karkaletsis (NCSR "Demokritos", Panteion University), CC-BY-4.0. Papers and
authorities cited are listed in `docs/02-reading-list-slm-fine-tuning.md` and
`init/init-001.md`.
