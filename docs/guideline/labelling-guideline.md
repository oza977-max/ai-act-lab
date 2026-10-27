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

All citations are to Regulation (EU) 2024/1689 as amended by Regulation (EU)
2026/1744 ([Act](https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng),
[amendment](https://eur-lex.europa.eu/eli/reg/2026/1744/oj/eng)). The Act was
read on 2026-10-27; the status of Commission guidance was checked on 2026-10-26,
during the requirements phase.

## The six labels

Exactly six labels exist. There is no "limited-risk" or "general-purpose" label.

| Label | Definition | Rests on |
|---|---|---|
| `prohibited` | The system carries out a practice the Act bans outright, such as social scoring, emotion recognition at work, or generating non-consensual intimate images. | Art. 5(1) |
| `high-risk` | The system is a safety component of, or is itself, a product under the Annex I legislation that needs third-party assessment, or it serves an Annex III use and the Article 6(3) exception does not apply. | Art. 6(1); Art. 6(2) |
| `transparency-only` | The system is not prohibited or high-risk, but an Article 50 duty applies, such as telling people they are talking to a machine or marking generated content. | Art. 50(1); Art. 50(2); Art. 50(3); Art. 50(4) |
| `minimal` | The system is an AI system within scope, and no prohibition, high-risk route or Article 50 duty applies. | Art. 95(1) |
| `out-of-scope` | The thing described is not an AI system under the definition, or the Act excludes it, for example military use or use for scientific research only. | Art. 3(1); Art. 2(3); Art. 2(6) |
| `needs-human-review` | This project's label, not the Act's: the description does not let a careful reader decide the tier, for one of three narrow reasons. | none: a project label |

The **Article 50 flag** is separate from the tier (`art50_flag`). A high-risk
recruitment chatbot is `high-risk` with the flag set to `true`. The tier
`transparency-only` is used only when Article 50 is the highest thing that applies.

Measures that providers and deployers of every AI system take whatever its tier,
such as supporting their staff's AI literacy (Art. 4(1)), are not a tier and are not
recorded. Citing Art. 95(1) (voluntary codes of conduct) for `minimal` is this
project's convention: the Act has no article that creates a minimal tier.

Source: Art. 2 to 6, 50 and 95 of the amended Act
([official text](https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng), checked on
2026-10-27).

## Decision order

Ask questions 1 to 3 and 5 in order and stop at the first one that decides the
tier. Question 4 sets the flag for every tier except `prohibited` and
`out-of-scope`, whose flag is always `false`, because Article 50 is never reached.

1. **Is it an AI system, and within the Act's scope?** An AI system is a
   machine-based system, designed to operate with some autonomy, that infers from
   its input how to produce outputs such as predictions, content, recommendations
   or decisions that can influence its environment (Art. 3(1)). Rules written by
   people, simple heuristics and basic data processing infer nothing, so they are
   not AI systems. Then check the exclusions:
   - used exclusively for military, defence or national-security purposes (Art. 2(3));
     a system also used for civilian purposes stays in scope;
   - developed and put into service for the sole purpose of scientific research and
     development (Art. 2(6));
   - research, testing or development before it is placed on the market or put into
     service, except testing in real-world conditions (Art. 2(8));
   - released under a free and open-source licence (Art. 2(12)), but only if it
     would not otherwise be prohibited, high-risk or an Article 50 system. This is
     the one exception to stopping early: check steps 2 to 4 first, and if none of
     them applies, the answer is `out-of-scope`.

   Personal use is **not** an exclusion of the system: Art. 2(10) only frees a person
   using AI for a purely personal, non-professional activity from the deployer's
   duties. The system and its provider stay in scope, so label the system.

   If it is not an AI system, or an exclusion applies: `out-of-scope`.
2. **Is it a prohibited practice?** Check every point of Art. 5(1), including
   points (ba) and (bb) added in 2026: generating non-consensual intimate images of
   an identifiable person without their explicit consent, and generating child
   sexual abuse material (unless a "without right" defence applies under national
   law). For these two:
   - a **provider's** system is prohibited when generating that material is its
     intended purpose, or when it can foreseeably and reproducibly do so without
     significant modification and lacks adequate safeguards to prevent it
     (Art. 5(1a), point (a));
   - a **deployer's** use is prohibited when they use the system for that purpose
     (Art. 5(1a), point (b));
   - editing that does not increase the exposure of intimate parts, or change the
     nature of a sexual act depicted, is not manipulation (Art. 5(1b)).

   Safeguards count only if they **reliably** prevent the output and misuse that is
   reported gets corrected. If the description says users can get round the
   safeguards and nothing was done about it, the provider's system is prohibited.
   If a general image or video tool's description says nothing about safeguards,
   assume the ordinary case (working safeguards) and carry on. If yes: `prohibited`.
3. **Is it high-risk through Annex I or Annex III, after the Article 6(3) exception?**
   - Annex I route (Art. 6(1)): the AI system is a safety component of a product, or
     is itself a product, covered by legislation listed in Annex I, and that product
     needs a third-party conformity assessment. Since 2026, a system used only for
     non-safety aspects such as user assistance, performance optimisation, service
     efficiency, convenience or quality control is not a safety component
     (Art. 6(1a)), unless its failure would endanger health and safety (Art. 6(1b)).
     A product that needs third-party assessment only for risks other than health
     and safety, such as radio-spectrum interference, does not count (Art. 6(1c)).
   - Annex I is numbered straight through: Section A is points 2 to 12 (point 1 was
     deleted in 2026) and Section B is points 13 to 21 (machinery moved there as
     point 21). So "Annex I 4" can only mean lifts. A Section B product classified
     under Art. 6(1) is still labelled `high-risk` on the `annex-i` route, even though
     only a few of the Act's provisions apply to it directly (Art. 2(2)); which
     duties apply is a matter for the dates-and-duties table, not the record.
   - Annex III route (Art. 6(2)): the system serves one of the uses listed in
     Annex III, unless the Article 6(3) exception applies (see below).

   If yes: `high-risk`, with the route recorded.
4. **Do Article 50 duties apply?** Set `art50_flag` using "Article 50 in short"
   below. If the tier is still open and the answer is yes: `transparency-only`.
5. **Otherwise: minimal.**

At any step, if the step cannot be decided for one of the three reasons in
"When to say needs-human-review", stop with `needs-human-review`.

Source: Art. 2, 3(1), 5, 6(1) to 6(3), 50 and Annex I and III of the amended Act
([official text](https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng), checked on
2026-10-27); Commission guidelines on the AI system definition and on prohibited
practices (adopted, February 2025).

## Article 50 in short

The flag records that a duty **applies**, not whether it was met: a sign or a
disclaimer in the description does not change it.

- **50(1), interaction.** A system meant to interact directly with people, such as a
  chatbot or voice assistant: flag `true`, unless the description says it is obvious
  to people that they are dealing with a machine. Treat a chatbot as not obvious by
  default.
- **50(2), generated content.** A system whose purpose is to generate synthetic
  audio, images, video or text as new content, such as an image generator, a voice
  clone or a text writer: flag `true`. This guideline reads the Act's exception
  (assisting standard editing, or not substantially altering the input or its
  meaning) to cover summaries, extracts and format conversions of documents the
  user supplies: those alone do not set the flag. This reading is provisional and
  will be revisited if Commission guidance on Article 50 says otherwise. A chatbot is flagged and cited
  under 50(1); add 50(2) only if it also generates images, audio or video.
- **50(3), emotion recognition or biometric categorisation.** The deployer must tell
  the people exposed: flag `true` whenever such a system is used and is not
  prohibited. Categorisation that is only ancillary to another service, such as a
  try-on filter that needs to find a face, is not biometric categorisation.
- **50(4), deep fakes and public-interest text.** The deployer must disclose deep
  fakes, and AI-generated text published to inform the public on matters of public
  interest, unless a person
  reviewed it and holds editorial responsibility: flag `true`. For evidently
  artistic, satirical or fictional work the disclosure is lighter, but the flag is
  still `true`.
- Systems authorised by law for detecting or investigating crime have exceptions;
  a gold case that turns on them is not used in v1.

Source: Art. 50(1) to 50(4)
([official text](https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng), checked on
2026-10-27).

## When the description is silent

Owner decision D-LS-1 (2026-10-27): **assume the ordinary case.**

- Assume the system is placed on the market or used in the EU, and works as the
  description says.
- Do not invent facts that would change the tier. If the purpose or setting is
  what decides the tier and the description does not give it, the case goes to
  review with `missing-fact`.
- When an assumption mattered, say so in the reason sentence, for example
  "Assuming use in the EU, ...".

Source: territorial scope and exclusions, Art. 2(1) and 2(10)
([official text](https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng), checked on
2026-10-27).

## The Article 6(3) exception

Owner decision D-LS-2 (2026-10-27): **the exception must be stated clearly.**

Under Art. 6(3), a system serving an Annex III use is not high-risk when it does
not pose a significant risk of harm, including by not materially influencing a
decision. The Act lists four cases: a narrow procedural task; improving the result
of a human activity already completed; detecting decision-making patterns without
replacing or influencing the human assessment without proper review; or a
preparatory task. **A system that profiles people is always high-risk**, whatever
its task. Profiling means automated evaluation of personal aspects of a person,
such as their work performance, economic situation, health, preferences,
reliability, behaviour, location or movements (Art. 3(52), which points to the
GDPR's definition). The provider must document its assessment before placing the
system on the market (Art. 6(4)); that duty is not recorded (no duties in the
record).

The rule here, the owner's simplification of the "no significant risk" test:

- The exception applies only on the Annex III route, never on the Annex I route.
- **First, is the Annex III use established?** A system that does a task inside
  one of the Annex III processes (for example any step of recruitment) is treated
  as serving that use; this is this guideline's convention, so whether a small
  task "counts" is never a reason for review. If the process itself is not given,
  that is `missing-fact`.
- **The "clearly stated" test, the one test to apply.** Both must hold:
  1. the description names the task, and it is plainly one of the four (for
     example "converts formats", "transcribes recordings", "checks spelling after
     the decision is made"); and
  2. nothing in the description says or implies that the system assesses, ranks,
     scores or filters people.
  This is the owner's simplification: it is stricter than the Act's profiling rule
  (filtering by objective criteria is not profiling, but fails point 2 here).
- **Not clearly stated means high-risk.** If either point fails, the label stays
  `high-risk`.
- Clearly stated: decide the tier from the remaining questions, usually `minimal`,
  and cite Art. 6(3) and the Annex III point (not Art. 95(1)).
- `unsettled-law` is only for a task that **is** clearly described, where whether
  that task counts as one of the four is something the Act's text does not settle.

Source: Art. 3(52), 6(3) and 6(4) of the amended Act
([official text](https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng), checked on
2026-10-27). This rule also leans on the **draft Commission guidelines** on
classifying high-risk AI systems under Article 6, open for consultation from
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
- `unsettled-law`: the facts are clear, but the legal question the tier depends on
  is not settled by the Act's text, for example a point that depends on the draft
  Article 6 guidelines or on wording new in 2026.

**A case that is hard but decidable is decided.** Review is not a way to avoid a
difficult call: accuracy bought by refusing hard cases is not accuracy. A review
answer sets `art50_flag` when the description decides it, and otherwise `false`.

Source: the requirement LS-6 of this project; the provisions in doubt are cited
in each record ([official text](https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng),
checked on 2026-10-27).

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

**What goes in `articles`:** the provisions that decide the tier, plus the
Article 50 paragraph or paragraphs when the flag is `true` (and only then). For a high-risk case, Art. 6(1) or
6(2) and the Annex point. For an Article 6(3) result, Art. 6(3) and the Annex III
point, and nothing else. For any other `minimal` case, Art. 95(1). For a review case, the provisions in doubt, or
none. Provisions that were considered and do not apply are not cited.

The record never holds a date, deadline or list of duties. Those come from the
dates-and-duties table, which is maintained separately and checked against the
law. An answer that cannot be read as this record counts as a format failure.

Complete example:

```json
{"tier": "high-risk", "route": "annex-iii", "annex_iii_area": 4, "annex_iii_point": "4(a)", "annex_i_legislation": null, "art50_flag": true, "articles": ["Art. 6(2)", "Annex III 4(a)", "Art. 50(1)"], "review_reason": null, "reason": "The system screens job applicants, an Annex III employment use, and it talks to them directly."}
```

Source: requirements LS-2 to LS-4, LS-9 and LS-10 of this project; citations
checked against `data/articles.json`, built from the
[official text](https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng), checked on 2026-10-27.

## Worked examples

Two or more per label, at least one a **boundary** case: a case close to the line
with another label, with the reason it falls on this side. The descriptions are
fictional. Every citation is checked against `data/articles.json`.

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

### Example PR-3 (prohibited)
A mobile app is advertised as turning any uploaded photo of a real, identifiable
person into a nude image of them. It does not ask whether the person shown has consented.

```json
{"tier": "prohibited", "route": null, "annex_iii_area": null, "annex_iii_point": null, "annex_i_legislation": null, "art50_flag": false, "articles": ["Art. 5(1)(ba)", "Art. 5(1a)"], "review_reason": null, "reason": "Generating nude images of identifiable people without their consent is the app's intended purpose, which the Act bans."}
```

### Example HR-1 (high-risk)
A bank uses an AI system that scores individual applicants for personal loans on
their likelihood of repaying, and loan officers use the score to approve or refuse.

```json
{"tier": "high-risk", "route": "annex-iii", "annex_iii_area": 5, "annex_iii_point": "5(b)", "annex_i_legislation": null, "art50_flag": false, "articles": ["Art. 6(2)", "Annex III 5(b)"], "review_reason": null, "reason": "Assessing the creditworthiness of individual loan applicants is an Annex III use, and nothing suggests a narrow or preparatory task."}
```

### Example HR-2 (high-risk) · boundary
A chain of clothes shops uses cameras with an AI system that infers whether
customers look pleased or frustrated near displays, to rearrange stock.
*Why boundary:* emotion recognition is banned only at work and in education; for
customers it is a high-risk biometric use, and Article 50 also requires informing
the people exposed. A sign at the entrance would not change the flag.

```json
{"tier": "high-risk", "route": "annex-iii", "annex_iii_area": 1, "annex_iii_point": "1(c)", "annex_i_legislation": null, "art50_flag": true, "articles": ["Art. 6(2)", "Annex III 1(c)", "Art. 50(3)"], "review_reason": null, "reason": "Recognising customers' emotions is an Annex III biometric use outside the workplace ban, and the people exposed must be informed."}
```

### Example HR-3 (high-risk)
Software reads chest X-rays and flags suspected lung nodules for radiologists. It
is sold as a medical device that needs certification by a notified body.
*Note:* medical devices are point 11 of Annex I, Section A; the 2026 amendment
deleted point 1 without renumbering the rest.

```json
{"tier": "high-risk", "route": "annex-i", "annex_iii_area": null, "annex_iii_point": null, "annex_i_legislation": "Regulation (EU) 2017/745 on medical devices", "art50_flag": false, "articles": ["Art. 6(1)", "Annex I 11"], "review_reason": null, "reason": "The system is a medical device that needs third-party conformity assessment under Annex I legislation, which makes it high-risk."}
```

### Example HR-4 (high-risk) · boundary
A recruitment platform's AI system writes a short summary of each applicant's CV,
highlighting relevant experience, and recruiters read the summaries before
deciding whom to shortlist.
*Why boundary:* summarising may sound preparatory, but choosing which experience
is "relevant" assesses candidates, so point 2 of the "clearly stated" test fails
and the exception is not applied. A summary of
a supplied document does not set the Article 50 flag.

```json
{"tier": "high-risk", "route": "annex-iii", "annex_iii_area": 4, "annex_iii_point": "4(a)", "annex_i_legislation": null, "art50_flag": false, "articles": ["Art. 6(2)", "Annex III 4(a)"], "review_reason": null, "reason": "Summarising applicants for shortlisting is a recruitment use, and the description does not clearly state a narrow or preparatory task, so it stays high-risk."}
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
{"tier": "transparency-only", "route": null, "annex_iii_area": null, "annex_iii_point": null, "annex_i_legislation": null, "art50_flag": true, "articles": ["Art. 50(1)"], "review_reason": null, "reason": "Answering policy questions makes no decisions about workers and monitors no one, so only the duty to disclose the chatbot applies."}
```

### Example TO-3 (transparency-only)
A design studio offers an online tool that generates product photos from a text
prompt, for customers' marketing material.

```json
{"tier": "transparency-only", "route": null, "annex_iii_area": null, "annex_iii_point": null, "annex_i_legislation": null, "art50_flag": true, "articles": ["Art. 50(2)"], "review_reason": null, "reason": "Generating synthetic images is not a listed high-risk use, but the output must be marked as artificially generated."}
```

### Example MI-1 (minimal)
A small firm's email system uses a learned spam filter that moves likely junk mail
into a separate folder.

```json
{"tier": "minimal", "route": null, "annex_iii_area": null, "annex_iii_point": null, "annex_i_legislation": null, "art50_flag": false, "articles": ["Art. 95(1)"], "review_reason": null, "reason": "Spam filtering is not banned, not listed as high-risk and triggers no Article 50 duty, so no tier applies beyond minimal."}
```

### Example MI-2 (minimal) · boundary
A recruitment agency's AI system converts CVs that arrive as scanned documents
into a standard text format with fixed headings. It does not rank, score, filter
or assess candidates, and recruiters read every converted CV.
*Why boundary:* recruitment is an Annex III use, but the description clearly states
a narrow procedural task with no profiling, so the Article 6(3) exception applies.
Compare HR-4, where the test fails. By this guideline's convention, a step inside
recruitment is treated as the recruitment use, so the record cites Art. 6(3) and
Annex III 4(a).

```json
{"tier": "minimal", "route": null, "annex_iii_area": null, "annex_iii_point": null, "annex_i_legislation": null, "art50_flag": false, "articles": ["Art. 6(3)", "Annex III 4(a)"], "review_reason": null, "reason": "Converting CV formats without assessing candidates is a narrow procedural task under the Article 6(3) exception, so the recruitment use is not high-risk."}
```

### Example MI-3 (minimal) · boundary
A recruitment agency uses an AI system that transcribes recorded job interviews
into text, which the interviewers then read alongside their own notes.
*Why boundary:* the description names a narrow procedural task (transcription) and
says nothing suggesting the system assesses, ranks, scores or filters
candidates, so the "clearly stated" test passes without an explicit denial.

```json
{"tier": "minimal", "route": null, "annex_iii_area": null, "annex_iii_point": null, "annex_i_legislation": null, "art50_flag": false, "articles": ["Art. 6(3)", "Annex III 4(a)"], "review_reason": null, "reason": "Transcribing recruitment interviews is a narrow procedural task that assesses no one, so the Article 6(3) exception takes it out of high-risk."}
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
A vendor's brochure says its tool "uses a machine-learning model trained on past
hires" to screen job applicants. The technical annex of the same brochure says the
tool "applies only the fixed rules your HR team writes, with no learning or
inference".
*Why boundary:* either statement alone is decidable: a trained screening model is
high-risk (Annex III 4(a)), while fixed rules written by people are not an AI
system. Together they conflict on the fact that decides the tier.

```json
{"tier": "needs-human-review", "route": null, "annex_iii_area": null, "annex_iii_point": null, "annex_i_legislation": null, "art50_flag": false, "articles": ["Art. 3(1)", "Annex III 4(a)"], "review_reason": "conflicting-facts", "reason": "The description says both that the tool uses a trained model and that it applies only fixed human rules, and the tier depends on which is true."}
```

### Example NR-3 (needs-human-review) · boundary
A bank's AI system gives each personal-loan application a fraud-risk score from
the applicant's documents and transaction history. Applications above a set score
are refused automatically, and no one checks the applicant's ability to repay
for those.
*Why boundary:* creditworthiness assessment is high-risk (HR-1), but Annex III 5(b)
excludes systems used to detect financial fraud. The facts are clear; whether a
fraud score that alone decides access to credit falls inside that exclusion is a
question the text does not settle.

```json
{"tier": "needs-human-review", "route": null, "annex_iii_area": null, "annex_iii_point": null, "annex_i_legislation": null, "art50_flag": false, "articles": ["Annex III 5(b)"], "review_reason": "unsettled-law", "reason": "Whether a fraud score that alone decides who gets a loan is excluded fraud detection or a creditworthiness assessment is not settled by the text."}
```

## The gold set

The 100 hand-checked gold cases live in `data/gold/`. Each records the guideline
version it was labelled under and carries `never_train: true`. The gold set is
never used for training: it is kept apart from all training data, no training
case may paraphrase a gold case, and any model that drafts training data is
checked against it, never shown it.

Source: requirements GS-6 and LS-7 of this project.

## Sources

- Regulation (EU) 2024/1689 (the AI Act),
  [official text](https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng), as amended by
  Regulation (EU) 2026/1744,
  [official text](https://eur-lex.europa.eu/eli/reg/2026/1744/oj/eng); both checked on
  2026-10-27, including the amended Art. 4, 5, 6 and Annex I. Every citation in
  this guideline is checked against the valid-article table built from them
  (`data/articles.json`).
- European Commission, guidelines on the definition of an AI system and on
  prohibited AI practices: adopted (February 2025), before the 2026 amendment; used
  for steps 1 and 2. Where they differ from the amended text, the text wins.
- European Commission, draft Commission guidelines on classifying high-risk AI
  systems under Article 6: consultation from 19 May 2026; draft status checked on
  2026-10-26. Provisional; used only where this guideline says so.
- James Pustejovsky and Amber Stubbs, *Natural Language Annotation for Machine
  Learning*: write the guideline before labelling, with examples, version it, and
  revise it from disagreements.

## Change log

| Version | Date | Change | Why |
|---|---|---|---|
| v1 | 2026-10-27 | First version: six labels, decision order, Article 50 rules, owner decisions D-LS-1 (assume the ordinary case) and D-LS-2 (Article 6(3) must be stated clearly), 18 worked examples | Build chunk P2-C01, before any gold case is labelled |
