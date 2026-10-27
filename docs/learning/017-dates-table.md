# 017. The dates-and-duties table (P2-C03)

**Step:** build chunk P2-C03, dates table. **Date:** 2026-10-27.

## The lesson before the step

Words first:

- **Application date.** The day a rule starts to bite. The AI Act entered into
  force in 2024, but its parts apply on different, later dates.
- **Duty (obligation).** Something a provider or deployer must do, such as risk
  management (Article 9) or human oversight (Article 14).
- **Provider and deployer.** The provider builds the system or puts it on the
  market under its name; the deployer uses it professionally.
- **Lookup table.** A small file the program reads. Give it a tier, a route and
  the Article 50 flag; it returns the dates and duties. **The model never learns
  dates; the table does.** When the law changes, you edit one file instead of
  retraining a model.
- **Verified.** Every date is read from the Official Journal, the EU's legal
  gazette, not copied from a summary.
- **Stale.** An entry not checked for more than 90 days is flagged.

**What usually goes wrong:** dates copied from blog posts, which were wrong the
moment the July 2026 amendment moved them; and a lookup that returns nothing for
"out of scope", which a reader takes to mean "no rules apply".

## What we did

1. **Checked the plan's dates against the law itself.** Article 113 of the Act
   sets the dates; the 2026 amendment replaced two of its points and added a
   grace period. All four of the plan's dates matched:
   - the two new bans (intimate imagery, child sexual abuse material): 2 December 2026;
   - Annex III high-risk duties: 2 December 2027;
   - Annex I high-risk duties: 2 August 2028;
   - Article 50(2) marking, for generative systems already on the market before
     2 August 2026: 2 December 2026.
2. **Wrote the table** (`data/dates/dates-table.toml`): nine entries, one per
   kind of answer, each with its source link, the date it was checked, who checked
   it, and the plan's value for comparison.
3. **Built the lookup** (`python -m lab.dates lookup`). It refuses to serve the
   table until you approve it, refuses any entry not verified, and marks entries
   older than 90 days as stale. For out-of-scope and needs-human-review it returns
   an explicit entry ("no tier duties; refer to a person"), never an empty answer.

## Things the law says that surprised us

- **Annex I has two kinds of product.** For Section A products (medical devices,
  toys, lifts...) the high-risk duties apply directly. For Section B products
  (cars, aircraft, machinery since 2026) only a few articles apply; the rest comes
  through their own sector law.
- **Old systems get a grace period.** A high-risk system already on the market
  before its date is covered only after a significant change in design; systems
  used by public authorities must comply by 2 August 2030.
- **The impact assessment (Article 27) is narrow.** Only public bodies, private
  firms providing public services, and deployers of credit-scoring or
  insurance-pricing systems must do it, and only for Annex III systems.

## What went wrong and how it was caught

No date was ever wrong. The reviewers (three rounds: 6, 3, then 0 serious
findings) found gaps instead: the first draft listed only some high-risk duties
without saying so, missed two paragraphs that share the new bans' later date,
and gave one duty a date that was an inference, not text. Twice a reviewer
doubted a point it could not read; both times the answer was in the Official
Journal text already read, and the table now quotes it.

## Terms that came up

- **Official Journal.** The EU's gazette; the legally binding text.
- **General date.** 2 August 2026, when most of the Act applies, including
  Article 50.
- **Grace period.** Extra time for systems already on the market.

## What you just learned

1. Facts that change belong in a table with sources, not in a model's weights.
2. A source link and a "checked on" date are what make a date trustworthy.
3. An explicit "no duties, ask a person" is safer than an empty answer.

## Check questions

1. A high-risk CV-screening system: from which date do Articles 9 to 17 apply?
2. Why does the lookup refuse to answer before you approve the table?
3. An entry was last checked on 1 August. On 1 November, is it stale?
