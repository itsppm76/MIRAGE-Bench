# Governance

## Who decides what

MIRAGE-Bench is maintained under the **OpenNHE Research Wing**. Day-to-day decisions —
accepting entities, appointing officers, publishing results — sit with the maintainers.
Changes to the *method* do not.

| Decision | Who | Where it happens |
|---|---|---|
| Accepting an entity for evaluation | Any officer | Public issue |
| Scoring an entity | The evaluating officer alone | Published run, signed |
| Appointing an officer | Maintainers | Public issue |
| Revoking an officer | Maintainers | Public, with reason |
| Changing module weights, bands or thresholds | Requires a version bump and a public rationale | Discussion, then CHANGELOG |
| Removing a published score | Only for a rights issue or a demonstrated error | Public, with reason |

**Scores are not negotiable by the entity's owner.** They are contestable by anyone, on
evidence. Those are different things, and the distinction is the point.

---

## Conflicts of interest

An officer does not evaluate an entity they own, work on, or are paid by. Officers declare
conflicts when they apply, and declaring one does not disqualify anyone — it scopes what they
evaluate.

### Standing disclosure

**The highest-ranked entity in the Pilot Cohort, `Shayari NHE 01` (99.1, Frontier), is owned
by the benchmark's author and was evaluated by the benchmark's author.**

This is a conflict of interest. It is stated here, in the README, and in the dataset's own
caveats, because a benchmark that hides this is not worth reading. Three things follow:

1. That score should be treated as provisional until an independent officer re-evaluates it.
2. Re-evaluation of it is explicitly invited, and a lower independent score will be published
   unchanged.
3. Once a second officer is active, the author's self-evaluations are the first candidates
   for audit.

The remedy for this is not a policy. It is a second evaluator.

---

## Version policy

The benchmark version appears on every score, because a score is only meaningful against the
version that produced it.

| Change | Version impact |
|---|---|
| New challenge cases within existing components | Patch — `1.0.x` |
| New components, or re-weighting inside a module | Minor — `1.x.0` |
| New or removed modules, changed module weights, changed bands | Major — `x.0.0` |

v2.0.0 was a major change: it added the REACH module and reweighted the craft modules.
Accordingly the Pilot Cohort stays labelled v1.0.0 and is ranked under the Craft only scope,
and the dataset validator holds a weight table per version so each record is checked against
the rules that produced it.

**Scores are never silently recomputed across a major version.** Results carry the version
they were produced under. Where a rule changes within a version — as when consensus
aggregation replaced best-of — a migration recomputes derived values from the runs already on
record, and the change is documented in [CHANGELOG.md](CHANGELOG.md).

---

## How results are corrected

Anyone may contest any result. The process is in
[CONTRIBUTING.md](CONTRIBUTING.md#contesting-a-result).

A contested score is re-examined, not automatically raised. Outcomes may be higher, lower or
unchanged, and the reasoning is published either way.

Rights issues — an unauthorised likeness, a trademark concern, imagery used without permission —
are handled ahead of scoring disputes and can result in immediate removal pending review.

---

## What would make this benchmark fail

Stated openly so it can be watched for:

- **One evaluator.** A benchmark with a single officer measures one person's judgement. This is
  the current state and the most urgent problem.
- **Unfalsifiable scores.** If a result cannot be checked against observable evidence, it is an
  opinion wearing a number. The current cohort's REACH scores are close to this line: they were
  assigned without the supporting evidence fields being recorded, so a reader cannot check what
  a standing score rests on. Filling `audience_total`, `recognitions` and `active_since` on
  future evaluations is the fix.
- **Owner capture.** If high scores become purchasable, negotiable, or a condition of
  participation, the benchmark is worthless.
- **Silent revision.** Changing scores without a version bump and a public reason.
- **Popularity quietly becoming the score.** REACH is capped at 9%, recognition outweighs raw
  audience roughly six to one, and standing is bounded against craft. If those guards are
  loosened so that a large audience starts deciding rank, the benchmark has become a follower
  count with extra steps.
- **Deception risk becoming a leaderboard.** The moment "most convincing deception" reads as an
  achievement, the benchmark is doing harm.
