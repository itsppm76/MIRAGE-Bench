# Contributing

Everyone is welcome here — viewers, creators, evaluators, researchers, developers and sceptics.
Nothing costs anything, and no affiliation is required.

---

## Submit an entity

[**Open an entity application →**](../../issues/new?template=entity-application.yml)

You do not need to own an entity to nominate it. Public, observable entities can be submitted
by anyone, in the same way a product can be reviewed by someone who does not make it.

If you **do** own it, say so — owners can supply provenance, and provenance is what makes an
entity rankable. Without it the run is recorded as `UNVERIFIED` and stays out of the
leaderboard.

**What an officer needs from you:** somewhere to observe roughly 20+ posts, or several sessions
for an interactive entity. Thin material produces a thin evaluation.

**What you should expect:** the score that the evidence supports. This repository publishes low
scores. If that is not acceptable, do not submit.

---

## Become an Intent Officer

[**Open an officer application →**](../../issues/new?template=officer-application.yml)

Officers run evaluations and are **named on every result they publish**.

There is no fee, no institutional requirement and no quota. What is required is that you will
score honestly when an honest score is unpopular — including when the entity belongs to
someone who will be annoyed.

This benchmark currently has **one** officer. An independent second evaluator improves it more
than any feature could.

Your application includes a trial evaluation. **Disagreeing with a published score, with
reasoning tied to evidence, is a strong application**, not a rude one.

---

## Contesting a result

[**Open a correction request →**](../../issues/new?template=correction-request.yml)

Anyone may contest any score: the creator, a researcher, or someone who thinks the maths is
wrong. You do not need standing.

What helps:

- The entity slug and the specific module
- What you believe the score should be
- Observable evidence anyone can check

What does not help: insistence, volume, or an appeal to how much work went into the entity.

A contested result is **re-examined, not automatically raised**. It may go up, down or nowhere,
and the reasoning is published.

Rights issues — likeness, trademark, imagery — jump the queue and may be removed pending review.

---

## Improving the benchmark

Arguments about the method belong in [Discussions](../../discussions), in the open.

Particularly wanted:

- **Attacks on the scoring maths.** Find a profile where the composite, the module floors or
  the consensus aggregation produce an absurd result. `scripts/validate_dataset.py` is a good
  place to start.
- **Evidence that a module does not measure what it claims.**
- **Challenge cases** that discriminate better than the existing ones.
- **Re-evaluations** of Pilot Cohort entities, especially the ones ranked highest.

Code contributions: the engine runs on Google Apps Script. See
[docs/DEPLOYMENT.md](docs/DEPLOYMENT.md). Fork it, run your own instance, break it, tell us how.

---

## Ground rules for data

If you contribute or regenerate data:

- **Never commit `Users`, `Sessions` or `OTPs`.** They contain email addresses, password hashes
  and salts. `scripts/export_pilot_cohort.py` refuses to read them and CI fails if credential
  fields appear anywhere under `data/`.
- Officer identity in published runs is a **pseudonym**. Do not undo that.
- Every published score must re-derive from its module values. CI recomputes all of them.

---

## Code of conduct

Be straight with people. Argue with the evidence, not the person. Entities are measured; their
creators are not.

Full text: [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).
