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
evaluation tool works and now marks answers strictly (a wrong field, a missing box
or a second sentence makes an answer count as wrong, and any date in an answer is
flagged), a first model runs on the laptop, and the owner has run a first practice
fine-tune. The evaluation report is complete: every number carries a 95% interval,
cited articles are checked against the official text (including the July 2026
amendment), and two models can be compared case by case. Phase 2 has started:
the [labelling guideline](docs/guideline/labelling-guideline.md), the rulebook for
every gold label, is drafted with 18 worked examples and four owner decisions,
and the owner approved it. The [zero-shot prompt](prompts/zero-shot-v1.txt) is now
generated from that guideline, so the two cannot drift apart. The
[dates-and-duties table](data/dates/dates-table.toml) is built, every date read
from the Official Journal, and the owner approved it. Phase 2 is complete.
Phase 3 has started: the tools that turn drafted cases and the owner's review
sheets into the gold set are built. Next: the first batch of 20 cases.
Target date 16 November 2026.

## Start here

Pick the path that fits you:

- **Curious, no technical background.** Read
  [the whole picture](docs/learning/000-the-whole-picture.md) (a six-step story about
  training a junior colleague), then watch [the seven-minute film](docs/learning/012-video.html).
- **You want to learn to fine-tune a small model.** Follow the
  [learning log](docs/learning/README.md) in order. Each entry is one step, with a
  lesson, what happened, the new words and check questions. The
  [glossary](docs/01-glossary.md) covers every term.
- **You want to see how an AI assistant can build software you can trust.** Read
  [how this was built](docs/how-this-was-built.md), then open any file in
  [build/handovers](build/handovers/) to see one chunk's full record.
- **You want to run it.** Jump to [Run it yourself](#run-it-yourself).

<!-- stats:start -->
## Progress at a glance

*Counted from the repository by `scripts/repo_stats.py` on 2026-10-27; nothing in this block is typed by hand.*

| Measure | Now |
|---|---|
| Build chunks done | 9 of 21 (2 of 4 phases complete) |
| Automated tests | 408 passing |
| Independent review passes | 26 passes over 9 chunks; 55 serious findings caught and fixed before commit |
| Learning entries | 19, plus 1 film |
| Training runs logged | 1 |
| Commits | 66 |

**Build log.** Each chunk is reviewed by an independent reviewer until a pass finds nothing serious; the numbers show the serious findings each pass found.

| Chunk | What it builds | Review passes | Record |
|---|---|---|---|
| P1-C01 | Skeleton, guard hook, first evaluation | 4 → 2 → 0 | [handover](build/handovers/P1-C01.md) |
| P1-C02 | Model smoke test (tracer) | 2 → 0 | [handover](build/handovers/P1-C02.md) |
| P1-C02b | Practice fine-tune (owner-run) | 0 | [handover](build/handovers/P1-C02b.md) |
| P1-C03 | Record rules | 0 → 0 | [handover](build/handovers/P1-C03.md) |
| P1-C04 | Full evaluation | 1 → 0 | [handover](build/handovers/P1-C04.md) |
| P2-C01 | Guideline v1 | 10 → 8 → 3 → 4 → 3 → 1 → 0 | [handover](build/handovers/P2-C01.md) |
| P2-C02 | Prompt build | 1 → 1 → 0 | [handover](build/handovers/P2-C02.md) |
| P2-C03 | Dates table | 6 → 3 → 0 | [handover](build/handovers/P2-C03.md) |
| P3-C01 | Gold tooling | 5 → 1 → 0 | [handover](build/handovers/P3-C01.md) |
| P3-C02 | Gold batch 1 | not started |  |
| P3-C03 | Gold batch 2 | not started |  |
| P3-C04 | Gold batch 3 | not started |  |
| P3-C05 | Gold batch 4 | not started |  |
| P3-C06 | Gold batch 5 | not started |  |
| P3-C07 | Blind re-label | not started |  |
| P4-C00 | Spike: candidate builds | not started |  |
| P4-C01 | Licence criteria | not started |  |
| P4-C02 | Bake-off runner | not started |  |
| P4-C03 | Owner runs the bake-off | not started |  |
| P4-C04 | Comparison and choice | not started |  |
| P4-C05 | End-to-end closure | not started |  |
<!-- stats:end -->

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
source. [How this was built](docs/how-this-was-built.md) explains the method for
newcomers. The phases so far, each with its artefact:

| Phase | What it produced | Read |
|---|---|---|
| Expert calibration | The reference shelf: 22 authorities, each scored twice independently | `init/init-001.md`, `scoring-reports/` |
| Reading list | 60 arXiv papers on small-model fine-tuning, each checked at source | `docs/02-reading-list-slm-fine-tuning.md` |
| Impact map | Two measured goals, three people, eighteen deliverables | `impact-map.md` |
| Requirements | 45 testable requirements for the first slice | `requirements/requirements.md` |
| Test cases | 64 tests written before any code | `test-cases/test-cases.md` |
| Technical spec | Four short specs and a build guide of small chunks | `specs/` |
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

**Practice fine-tune** (public benchmark data; 20 held-out cases, far too few to be a
measurement):

| | Result |
|---|---|
| Training memory | Batch size 4 ran out of memory; batch 1 with gradient checkpointing and 8 layers peaked at 6.4 GB |
| Training time | 12 minutes for 300 steps; trainable share 0.24%; adapter 7.2 MB |
| Validation loss | 1.003 at the start, 0.149 at the end, still falling |
| Held-out label accuracy | 5 of 20 untrained (it said "high-risk" every time); 16 of 20 after training |
| Halfway snapshot (step 200) | Good loss (0.176) but 0 usable answers: every answer looped repeating article numbers |

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
- **Loss is not the result.** Halfway through practice training, the validation loss
  looked good while every answer was stuck in a loop. Only reading real answers
  showed it. Messy article lists in the practice data had taught the habit.
- **Borrowed memory estimates.** A figure from another project (3.9 GB to train a 0.8B
  model) did not hold here; a two-step test run found the real limits before the
  owner's run.
- **Detectors make two kinds of mistake.** The first date detector missed
  "2 august 2026" (lowercase) and wrongly flagged "Section 6.5.2026"; the
  one-sentence check rejected "Example Ltd. screens CVs." because of the period in
  "Ltd.". An independent reviewer found all three by throwing about 60 odd inputs
  at the code; each now has a test.
- **The law's structure is not uniform.** The first valid-article table, read from
  the Official Journal, gave Article 3 no entries because it has numbered
  definitions rather than paragraphs. A model citing "Art. 3(1)" (the definition of
  an AI system) would have been marked as inventing law. A reviewer caught it.
- **A rulebook's examples can break its own rules.** The labelling guideline passed
  its own tests at once, because the tests checked shape, not consistency.
  Independent reviewers needed seven rounds (10, 8, 3, 4, 3, 1 and 0 serious
  findings) to make every rule precise enough that two careful readers would
  agree. Along the way they showed that the first draft had missed two new bans
  in the 2026 amendment, and that two "unsettled law" examples were in fact
  decidable. Two findings were judgement calls and went to the owner.
- **One case is a smoke test, not a result.** The untrained model read the new
  4,400-token prompt in about five seconds, then wrote `"null"` as text and
  looped on article numbers. After one added line it stopped looping but copied
  the prompt's example record instead. We stopped tuning there: fitting the prompt
  to one case is the same trap as fitting a model to its training data.
- **A list that looks complete misleads as much as a wrong date.** No date in the
  dates table was ever wrong, but the first draft listed only some of the
  high-risk duties without saying so. Reviewers needed three rounds (6, 3 and 0
  serious findings); every high-risk entry now says what it leaves out.
- **The worst bug is silent.** The first version of the gold tools would have
  ignored a label the owner typed if they forgot to switch "accept" to "change".
  Reviewers (5, 1 and 0 serious findings) also showed how ordinary spreadsheet
  habits could lock the owner out. Now every surprise is reported by case id,
  and nothing Claude drafts reaches the owner unless it reads back unchanged.
- **Ten cases say little.** The 10-case practice exam scores 7 of 10, with a 95%
  interval of 40% to 89%. Every number in the report now carries its interval.
- **Time estimates.** Early deadline options suggested months; the honest estimate
  is 15 to 20 hours of the owner's time over two to three weeks.

## Learn along

- `docs/learning/000-the-whole-picture.md`: the whole project in plain English, as a
  six-step story about training a junior colleague. Start here.
- `docs/learning/012-video.html`: a narrated seven-minute film of the ideas behind
  the first fine-tune (open it in a browser).
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
