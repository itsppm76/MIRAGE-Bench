# Changelog

Scores carry the benchmark version that produced them. Results are never silently recomputed
across a major version.

---

## [2.0.0] — 2026

Makes the benchmark universal: it now measures not only how well an entity is *made*, but how
much it *matters* — while making structurally certain the second can never be mistaken for the
first.

### Added — MIRAGE-REACH (9% of composite)

Standing & Recognition, across seven components:

| Component | Weight |
|---|---|
| R1 Institutional recognition | 28% |
| R2 Verified notability | 18% |
| R3 Commercial validation | 16% |
| R4 Longevity and persistence | 14% |
| R5 Engagement quality | 12% |
| R6 Audience scale (log-scaled) | 8% |
| R7 Cross-platform presence | 4% |

Three safeguards, because popularity is the easiest thing to fake in a benchmark:

- **Recognition outweighs audience about six to one.** R1+R2 = 46% against R6's 8%. Maximum
  audience with no recognition scores 8/100 on the module.
- **Audience is log-scaled**: 500 → 35, 1M → 78, 50M → 100.
- **REACH is bounded to 20 points above the median craft module.** Standing cannot outrun
  substance. The raw score is displayed in full; only its influence is clipped.

Measured: excellent craft with no audience (81.8) beats mediocre craft with maximum fame (56.6)
by 25 points. TRUST below 50 still caps everything at 69.9 — fame cannot buy back disclosure.

### Changed — module weights

| | LOOK | FLOW | PERSONA | INTENT | TIME | AGENT | TRUST | REACH |
|---|---|---|---|---|---|---|---|---|
| v1.0.0 | 20% | 15% | 20% | 10% | 15% | 10% | 10% | — |
| **v2.0.0** | 18% | 14% | 18% | 9% | 13% | 9% | **10%** | **9%** |

The craft modules each gave up a little. **TRUST did not** — integrity does not shrink to
accommodate fame.

### Added — Craft only scope

Exactly the seven v1.0.0 modules, excluding standing. A newly launched entity has had no fair
chance to build recognition, and scoring it on longevity would measure its age rather than its
quality. v1 results map onto this scope cleanly.

### Added — entity standing fields

`audience_total`, `audience_breakdown`, `recognitions`, `active_since`. Evidence *for* a REACH
evaluation, never scores in themselves; an officer verifies them independently.

### Added — craft-against-standing insight chart

If this benchmark were a popularity chart, that scatter would be a formless cloud.

### Migration

```js
Migrate_syncHeaders()      // adds the standing fields
Migrate_v1_to_v2()         // recomposites; maps existing entities to Craft only
Report_reachCoverage()     // how much of the catalogue has a REACH score
```

**No REACH score is invented for existing entities.** They carry none until an officer actually
evaluates them, and rank under Craft only meanwhile. Existing composites shift by roughly ±0.1
from renormalisation. Per GOVERNANCE.md, runs keep the version they were produced under: a v1
result stays labelled v1 permanently, and the dataset validator holds a weight table per
version so v1 records are checked against v1 weights.

### Published Pilot Cohort

Re-evaluated and republished under v2.0.0: **103 entities, 249 runs**, all scored on all eight
modules. The band distribution shifted markedly — 55 entities now sit in Developing, driven by
a REACH mean of 69.0 and the module floors. That is the benchmark tightening, not the entities
degrading.

Still one officer. Most entities now carry two or more evaluations, but repeated evaluation by
the same officer is not independent replication, and the dataset says so plainly.

---

## [1.0.0] — 2026

First public release, with the Pilot Cohort of 102 evaluated entities.

### Benchmark
- Seven modules — LOOK, FLOW, PERSONA, INTENT, TIME, AGENT, TRUST — across 37 weighted components.
- MIRAGE Index as a weighted geometric mean, so one collapsed module cannot be averaged away.
- Six score bands, narrowing as they rise: Frontier spans 5 points, Experimental spans 45.
- **Module floors** on the top two bands. Frontier requires every scored module at 85+,
  Excellent at 70+, because a weighted mean alone lets a low-weight module collapse unnoticed.
- **Integrity cap**: TRUST below 50 caps the composite at 69.9 regardless of everything else.
- **Evaluation scopes**, so entities without an interactive surface are not scored on memory
  and agency. Out-of-scope modules are reported as such, never as zero.
- Results ranked within their scope; cross-scope composites are not presented as one ranking.

### Aggregation
- Ranked figures are the **consensus** across all published evaluations, not a single run.
- Outliers excluded by median absolute deviation, so a lone sabotage run cannot move a score.
  Superseded an earlier best-of rule, which was outlier-proof but rewarded a single lucky run.
- Two sharply disagreeing evaluations are marked **disputed** and defer to the higher until a
  third breaks the tie.
- **Trend** via the Theil–Sen estimator, so direction of travel survives a sabotage run that
  would flip a least-squares line.
- Peak score reported alongside consensus for context.

### Platform
- Public read access to everything: rankings, score cards, run records, methodology, insights.
  No account, ever.
- Evaluation restricted to Intent Officers, provisioned by administrators. No public sign-up.
- Bulk entity registration and bulk evaluation from spreadsheets, through the same scoring path
  as manual entry.
- Public insights page with eleven charts drawn as inline SVG.
- Shareable 4:5 score cards generated client-side.

### Data
- Pilot Cohort published: 102 verified entities, 139 runs, as JSON and CSV.
- `Users`, `Sessions` and `OTPs` permanently excluded from export; enforced in CI.
- Officer identity pseudonymised in the exported dataset.

### Known state at release
- **One officer.** Every evaluation in the cohort comes from a single evaluator.
- **71 of 102 entities carry one evaluation**, below the threshold where consensus protection
  engages.
- **The top-ranked entity is the author's own and was self-evaluated.** Disclosed in
  GOVERNANCE.md and in the dataset caveats.
