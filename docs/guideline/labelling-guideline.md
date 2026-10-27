# Labelling guideline

**Version:** v1 (drafted 2026-10-27; awaiting the owner's approval)

This is the rulebook for labelling a description of an AI system under the EU AI
Act. Every gold case is labelled with it, and the model's prompt is generated from
it, so the model and the person marking it follow the same rules. When labelling
shows a gap, the guideline changes, the version goes up, and the change log says
why. Every gold label records the version it was given under.

It classifies **AI systems**, not general-purpose AI models: the obligations for
models in Chapter V are not a tier here. It is a learning project's rulebook, not
legal advice.

## The six labels

Exactly six labels exist. There is no "limited-risk" or "general-purpose" label.

| Label | Definition | Rests on |
|---|---|---|
| `prohibited` | The system carries out a practice the Act bans outright, such as social scoring or emotion recognition at work. | Art. 5(1) |
| `high-risk` | The system is a safety component of, or is itself, a product under the Annex I legislation needing third-party assessment, or it serves an Annex III use and the Article 6(3) exception does not apply. | Art. 6(1); Art. 6(2) |
| `transparency-only` | The system is not prohibited or high-risk, but an Article 50 duty applies, such as telling people they are talking to a machine or marking generated content. | Art. 50(1); Art. 50(2); Art. 50(3); Art. 50(4) |
| `minimal` | The system is an AI system within scope, and no prohibition, high-risk route or Article 50 duty applies, so only voluntary codes of conduct concern it. | Art. 95(1) |
| `out-of-scope` | The thing described is not an AI system under the definition, or the Act excludes it, for example military use or use for scientific research only. | Art. 3(1); Art. 2(3); Art. 2(6) |
| `needs-human-review` | This project's label, not the Act's: the description does not let a careful reader decide the tier, for one of three narrow reasons. | Art. 6(2); Art. 6(3) |

The **Article 50 flag** is separate from the tier (`art50_flag`). A high-risk
recruitment chatbot is `high-risk` with the flag set to `true`. The tier
`transparency-only` is used only when Article 50 is the highest thing that applies.

## Decision order

Ask the questions in this order and stop at the first one that decides the tier.
Question 4 is always answered, because it sets the flag for every tier.

1. **Is it an AI system, and within the Act's scope?** Use the definition in
   Art. 3(1) (a machine-based system that infers from its input how to produce
   outputs such as predictions, content, recommendations or decisions) and the
   exclusions in Art. 2. Fixed rules written by people, with no inference, are not
   an AI system. If no: `out-of-scope`.
2. **Is it a prohibited practice?** Check Art. 5(1). If yes: `prohibited`.
3. **Is it high-risk through Annex I or Annex III, after the Article 6(3) exception?**
   Annex I route: Art. 6(1). Annex III route: Art. 6(2), then the exception in
   Art. 6(3) as set out below. If yes: `high-risk`, with the route recorded.
4. **Do Article 50 duties apply?** Set `art50_flag`. If the tier is still open and
   the answer is yes: `transparency-only`.
5. **Otherwise: minimal.**

At any step, if the step cannot be decided for one of the three reasons in
"When to say needs-human-review", stop with `needs-human-review`.

## When the description is silent

Owner decision D-LS-1 (2026-10-27): **assume the ordinary case.**

- Assume the system is used in the EU, by a professional user, and works as the
  description says.
- Do not invent facts that would change the tier. If the purpose or setting is
  what decides the tier and the description does not give it, the case goes to
  review with `missing-fact`.
- When an assumption mattered, say so in the reason sentence, for example
  "Assuming use in the EU, ...".

## The Article 6(3) exception

Owner decision D-LS-2 (2026-10-27): **the exception must be stated clearly.**

Under Art. 6(3), a system serving an Annex III use is not high-risk when it does
not pose a significant risk of harm, including by not materially influencing a
decision. The Act lists four such cases: a narrow procedural task; improving the
result of a human activity already completed; detecting decision-making patterns
without replacing or influencing the human assessment without proper review; or a
preparatory task. **A system that profiles people is always high-risk**, whatever
its task. The provider must document its assessment before placing the system on
the market (Art. 6(4)).

The rule here:

- The label stays `high-risk` unless the description **clearly** says the task is
  one of the four, **and** it does not say or imply profiling of people.
- Clearly stated and no profiling: decide the tier from the remaining questions,
  usually `minimal`, and cite Art. 6(3) and the Annex III point.
- Where the answer turns on how the Commission will read one of the four cases,
  and the text alone cannot settle it, use `needs-human-review` with
  `unsettled-law`.

Source: Regulation (EU) 2024/1689, Art. 6(3) and 6(4), as amended by Regulation
(EU) 2026/1744 ([official text](https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng),
checked on 2026-10-27). This rule also leans on the **draft Commission guidelines**
on classifying high-risk AI systems under Article 6, open for consultation from
19 May 2026; no adopted version had been found when checked on 2026-10-26. Treat
anything the draft says as provisional.

## When to say needs-human-review

Narrowly. A case goes to review only for one of three reasons, recorded in
`review_reason`:

- `missing-fact`: the description lacks a fact that decides the tier, and the
  ordinary-case assumptions above do not supply it. Example: a tool that ranks
  people, with no purpose or setting given.
- `conflicting-facts`: the description says two things that cannot both be true,
  and the tier depends on which is.
- `unsettled-law`: the legal question the tier depends on is not settled by the
  Act's text, for example a point that depends on the draft Article 6 guidelines.

**A case that is hard but decidable is decided.** Review is not a way to avoid a
difficult call: accuracy bought by refusing hard cases is not accuracy. Each
review answer still sets `art50_flag` and may cite the provisions it could not
decide between.

## The answer record

Every answer, gold or model, is one JSON record with these nine fields, defined
in `lab/records.py` (the single source of truth) and quoted here.

| Field | Type | Rule |
|---|---|---|
| `tier` | one of the six labels | Required |
| `route` | `annex-iii`, `annex-i` or `null` | Required when tier is high-risk, otherwise null |
| `annex_iii_area` | integer 1 to 8 or `null` | Required when route is annex-iii |
| `annex_iii_point` | string such as `4(a)` or `null` | Required when route is annex-iii, and inside that area |
| `annex_i_legislation` | string or `null` | Required when route is annex-i |
| `art50_flag` | `true` or `false` | Required |
| `articles` | list such as `["Art. 6(2)", "Annex III 4(a)"]` | At least one, except for needs-human-review; every citation must exist in the Act |
| `review_reason` | `missing-fact`, `conflicting-facts`, `unsettled-law` or `null` | Required when tier is needs-human-review, otherwise null |
| `reason` | text | One sentence, at most 40 words |

The record never holds a date, deadline or list of duties. Those come from the
dates-and-duties table, which is maintained separately and checked against the
law. An answer that cannot be read as this record counts as a format failure.

Complete example:

```json
{"tier": "high-risk", "route": "annex-iii", "annex_iii_area": 4, "annex_iii_point": "4(a)", "annex_i_legislation": null, "art50_flag": true, "articles": ["Art. 6(2)", "Annex III 4(a)", "Art. 50(1)"], "review_reason": null, "reason": "The system screens job applicants, an Annex III employment use, and it talks to them directly."}
```

## Worked examples

Two or more per label, at least one a **boundary** case: a case close to the line
with another label, with the reason it falls on this side.

### Example PR-1 (prohibited)
A city council uses an AI system to score residents on their behaviour across
public services, such as late library returns and noise complaints, and residents
with low scores wait longer for social housing.

```json
{"tier": "prohibited", "route": null, "annex_iii_area": null, "annex_iii_point": null, "annex_i_legislation": null, "art50_flag": false, "articles": ["Art. 5(1)(c)"], "review_reason": null, "reason": "Scoring residents on social behaviour and treating low scorers worse in an unrelated area is social scoring, which the Act bans."}
```

### Example PR-2 (prohibited) · boundary
A call-centre company runs an AI system on its agents' webcams that infers whether
each agent is bored or stressed, and team leaders see the results during shifts.
*Why boundary:* the same technology aimed at shop customers is high-risk, not
prohibited (see HR-2); the ban covers workplaces and schools, except for medical or
safety reasons.

```json
{"tier": "prohibited", "route": null, "annex_iii_area": null, "annex_iii_point": null, "annex_i_legislation": null, "art50_flag": false, "articles": ["Art. 5(1)(f)"], "review_reason": null, "reason": "Inferring employees' emotions at work, for no medical or safety reason, is a banned practice."}
```

### Example HR-1 (high-risk)
A bank uses an AI system that scores individual applicants for personal loans on
their likelihood of repaying, and loan officers use the score to approve or refuse.

```json
{"tier": "high-risk", "route": "annex-iii", "annex_iii_area": 5, "annex_iii_point": "5(b)", "annex_i_legislation": null, "art50_flag": false, "articles": ["Art. 6(2)", "Annex III 5(b)"], "review_reason": null, "reason": "Assessing the creditworthiness of individual loan applicants is an Annex III use, and nothing suggests a narrow or preparatory task."}
```

### Example HR-2 (high-risk) · boundary
A chain of clothes shops uses cameras with an AI system that infers whether
customers look pleased or frustrated near displays, to rearrange stock. A sign at
the entrance tells customers about it.
*Why boundary:* emotion recognition is banned only at work and in education; for
customers it is a high-risk biometric use, and Article 50 also requires informing
the people exposed.

```json
{"tier": "high-risk", "route": "annex-iii", "annex_iii_area": 1, "annex_iii_point": "1(c)", "annex_i_legislation": null, "art50_flag": true, "articles": ["Art. 6(2)", "Annex III 1(c)", "Art. 50(3)"], "review_reason": null, "reason": "Recognising customers' emotions is an Annex III biometric use outside the workplace ban, and the people exposed must be informed."}
```

### Example HR-3 (high-risk)
Software reads chest X-rays and flags suspected lung nodules for radiologists. It
is sold as a medical device that needs certification by a notified body.

```json
{"tier": "high-risk", "route": "annex-i", "annex_iii_area": null, "annex_iii_point": null, "annex_i_legislation": "Regulation (EU) 2017/745 on medical devices", "art50_flag": false, "articles": ["Art. 6(1)", "Annex I 11"], "review_reason": null, "reason": "The system is a medical device that needs third-party conformity assessment under Annex I legislation, which makes it high-risk."}
```

### Example TO-1 (transparency-only)
An online bike shop runs a chatbot that answers customers' questions about orders,
delivery and returns.

```json
{"tier": "transparency-only", "route": null, "annex_iii_area": null, "annex_iii_point": null, "annex_i_legislation": null, "art50_flag": true, "articles": ["Art. 50(1)"], "review_reason": null, "reason": "A customer-service chatbot is not a listed high-risk use, but people must be told they are talking to a machine."}
```

### Example TO-2 (transparency-only) · boundary
A company's HR department runs a chatbot that answers employees' questions about
the leave policy and the expenses rules. It makes no decisions about anyone and
does not monitor staff.
*Why boundary:* it sits in employment, an Annex III area, but Annex III 4(b) covers
decisions about workers and monitoring them, which this chatbot does not do.

```json
{"tier": "transparency-only", "route": null, "annex_iii_area": null, "annex_iii_point": null, "annex_i_legislation": null, "art50_flag": true, "articles": ["Art. 50(1)", "Annex III 4(b)"], "review_reason": null, "reason": "Answering policy questions makes no decisions about workers and monitors no one, so only the duty to disclose the chatbot applies."}
```

### Example MI-1 (minimal)
A small firm's email system uses a learned spam filter that moves likely junk mail
into a separate folder.

```json
{"tier": "minimal", "route": null, "annex_iii_area": null, "annex_iii_point": null, "annex_i_legislation": null, "art50_flag": false, "articles": ["Art. 95(1)"], "review_reason": null, "reason": "Spam filtering is not banned, not listed as high-risk and triggers no Article 50 duty, so only voluntary codes apply."}
```

### Example MI-2 (minimal) · boundary
A recruitment agency's AI system converts CVs that arrive as scanned documents
into a standard text format with fixed headings. It does not rank, score, filter
or assess candidates, and recruiters read every converted CV.
*Why boundary:* recruitment is an Annex III use, but the description clearly states
a narrow procedural task with no profiling, so the Article 6(3) exception applies.

```json
{"tier": "minimal", "route": null, "annex_iii_area": null, "annex_iii_point": null, "annex_i_legislation": null, "art50_flag": false, "articles": ["Art. 6(3)", "Annex III 4(a)"], "review_reason": null, "reason": "Converting CV formats without assessing candidates is a narrow procedural task under the Article 6(3) exception, so the recruitment use is not high-risk."}
```

### Example OS-1 (out-of-scope) · boundary
An HR team calculates annual bonuses in a spreadsheet with formulas it wrote
itself: a fixed percentage of salary, adjusted by the manager's rating.
*Why boundary:* it decides about workers, which sounds like Annex III, but it infers
nothing; it only applies rules people wrote, so it is not an AI system.

```json
{"tier": "out-of-scope", "route": null, "annex_iii_area": null, "annex_iii_point": null, "annex_i_legislation": null, "art50_flag": false, "articles": ["Art. 3(1)"], "review_reason": null, "reason": "Fixed formulas written by people involve no inference, so the spreadsheet is not an AI system under the definition."}
```

### Example OS-2 (out-of-scope)
A national army uses an AI system, exclusively for military purposes, to support
the planning of supply routes in operations.

```json
{"tier": "out-of-scope", "route": null, "annex_iii_area": null, "annex_iii_point": null, "annex_i_legislation": null, "art50_flag": false, "articles": ["Art. 2(3)"], "review_reason": null, "reason": "Systems used exclusively for military purposes are excluded from the Act's scope."}
```

### Example NR-1 (needs-human-review)
A tool ranks people by a score it computes from the data it is given. Nothing
says who is ranked, for what, or who uses the ranking.

```json
{"tier": "needs-human-review", "route": null, "annex_iii_area": null, "annex_iii_point": null, "annex_i_legislation": null, "art50_flag": false, "articles": [], "review_reason": "missing-fact", "reason": "The tier depends on the purpose and setting of the ranking, which the description does not give."}
```

### Example NR-2 (needs-human-review) · boundary
A recruitment tool "makes the final hiring decision automatically", the vendor
says in one paragraph; in the next, it "only converts CVs into a standard format
and never assesses candidates".
*Why boundary:* either reading alone is decidable (HR or MI-2); together they
conflict on the fact that decides the tier.

```json
{"tier": "needs-human-review", "route": null, "annex_iii_area": null, "annex_iii_point": null, "annex_i_legislation": null, "art50_flag": false, "articles": ["Annex III 4(a)", "Art. 6(3)"], "review_reason": "conflicting-facts", "reason": "The description says both that the tool decides on hiring and that it never assesses candidates, and the tier depends on which is true."}
```

### Example NR-3 (needs-human-review) · boundary
A regional electricity grid operator uses an AI system to forecast next-day
demand. Engineers use the forecast when scheduling power stations; the
description does not say it controls any equipment.
*Why boundary:* whether a forecasting aid counts as a safety component of
critical infrastructure is a question the draft Article 6 guidelines address
but the Act's text alone does not settle.

```json
{"tier": "needs-human-review", "route": null, "annex_iii_area": null, "annex_iii_point": null, "annex_i_legislation": null, "art50_flag": false, "articles": ["Annex III 2", "Art. 3(14)"], "review_reason": "unsettled-law", "reason": "Whether a demand forecast used in scheduling is a safety component of critical infrastructure is not settled by the Act's text."}
```

## The gold set

The 100 hand-checked gold cases live in `data/gold/`. Each records the guideline
version it was labelled under and carries `never_train: true`. The gold set is
never used for training: it is kept apart from all training data, no training
case may paraphrase a gold case, and any model that drafts training data is
checked against it, never shown it.

## Sources

- Regulation (EU) 2024/1689 (the AI Act),
  [official text](https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng), as amended by
  Regulation (EU) 2026/1744,
  [official text](https://eur-lex.europa.eu/eli/reg/2026/1744/oj/eng); both checked on
  2026-10-27. Every citation in this guideline is checked against the
  valid-article table built from them (`data/articles.json`).
- European Commission, guidelines on the definition of an AI system and on
  prohibited AI practices: adopted (February 2025); used for steps 1 and 2.
- European Commission, draft Commission guidelines on classifying high-risk AI
  systems under Article 6: consultation from 19 May 2026; draft status checked on
  2026-10-26. Provisional; used only where this guideline says so.
- James Pustejovsky and Amber Stubbs, *Natural Language Annotation for Machine
  Learning*: write the guideline before labelling, with examples, version it, and
  revise it from disagreements.

## Change log

| Version | Date | Change | Why |
|---|---|---|---|
| v1 | 2026-10-27 | First version: six labels, decision order, owner decisions D-LS-1 (assume the ordinary case) and D-LS-2 (Article 6(3) must be stated clearly), 14 worked examples | Build chunk P2-C01, before any gold case is labelled |
