# Scoring

MIRAGE-Bench v2.0.0.

Everything here is implemented in `Scoring.gs` and independently re-derived by
`scripts/validate_dataset.py` on every change to the published data. If the two ever disagree,
CI fails.

> **Version matters.** Module weights changed in v2.0.0, so a score is only meaningful against
> the version that produced it. The validator holds a weight table per version and checks each
> record against its own. The published Pilot Cohort is v1.0.0.

---

## 1. Component → module

Each of the eight modules is built from weighted components, scored 0–100 by an officer.
There are **45 components** in total. Component weights within a module always sum to 1.

```
module score = Σ (component weight × component score) / Σ (weights of scored components)
```

A component left blank is excluded from both sums. **Blank and zero are different claims**:
blank means not tested, zero means tested and it failed. The engine treats them differently
and so should you.

Full component tables: [METHODOLOGY.md](METHODOLOGY.md).

---

## 2. Module → MIRAGE Index

```
MIRAGE Index = 100 × exp( Σ wᵢ × ln( max(sᵢ, 1) / 100 ) )
```

A **weighted geometric mean**, renormalised across whichever modules were actually scored.

| Module | v1.0.0 | **v2.0.0** |
|---|---|---|
| LOOK | 20% | 18% |
| FLOW | 15% | 14% |
| PERSONA | 20% | 18% |
| INTENT | 10% | 9% |
| TIME | 15% | 13% |
| AGENT | 10% | 9% |
| TRUST | 10% | **10%** |
| REACH | — | **9%** |

The craft modules each gave up a little to make room for REACH. **TRUST did not.** Integrity
does not shrink to accommodate fame.

Why not an arithmetic mean:

| Profile | Arithmetic | Geometric |
|---|---|---|
| Seven modules at 100, one at 20 | 90.0 | **78.6** |
| All eight at 82 | 82.0 | 82.0 |

A geometric mean multiplies rather than adds, so one collapsed dimension damages the whole
result instead of being absorbed by six strong ones. That is the intended behaviour: an
entity with excellent visuals and no persona coherence at all has not "mostly succeeded".

Scores are floored at 1 before the logarithm so a literal zero cannot produce `ln(0)`.

---

## 3. Bands

Bands narrow as they rise. Near the bottom a few points mean little; near the top every
point is contested and a tier change should mean something.

| Band | Range | Width | Module floor |
|---|---|---|---|
| **Frontier** | 95–100 | 5 | every scored module ≥ 85 |
| **Excellent** | 88–95 | 7 | every scored module ≥ 70 |
| **Strong** | 78–88 | 10 | — |
| **Developing** | 65–78 | 13 | — |
| **Weak** | 45–65 | 20 | — |
| **Experimental** | 0–45 | 45 | — |

### Module floors

A threshold alone does not make a top band hard to reach. AGENT carries 10% of the composite,
so an entity scoring 98 everywhere that collapses to 80 on AGENT still composites to **96** —
Frontier, on a broken module. A weighted mean is built to absorb exactly that.

The floor closes the gap. An entity failing the floor is demoted one tier at a time until its
weakest scored module clears the bar for the tier it claims.

| Profile | Composite | Band by composite | Actual band |
|---|---|---|---|
| All 98, AGENT 80 | 96.0 | Frontier | **Excellent** |
| All 99, LOOK 84 | 95.8 | Frontier | **Excellent** |
| All 94, AGENT 55 | 89.1 | Excellent | **Strong** |
| All 96 | 96.0 | Frontier | Frontier |

A top band is therefore a claim about **breadth**, not a strong average with one hidden weak spot.

---

## 4. The integrity cap

**TRUST below 50 caps the composite at 69.9**, inside the Developing band, regardless of every
other module.

This is the benchmark's position rather than a technical detail: an entity that is flawlessly
convincing but dishonest about being synthetic has not performed well. Realism never buys back
disclosure. The cap lands mid-band deliberately, so a capped entity cannot sit a decimal below
a tier it did not earn.

Related rules:

- **Missing provenance or disclosure status** marks a run `UNVERIFIED`. Unverified entities are
  excluded from ranking entirely rather than ranked low.
- **Deception risk** is reported as a warning and is never a sort key anywhere.
- **TRUST is mandatory in every scope.** A published run without it is rejected.

---

## 4a. Standing, and why it is bounded

**MIRAGE-REACH** measures an entity's standing in the world: recognition, notability,
commercial validation, longevity, engagement quality and audience. It carries **9%** of the
composite.

Adding popularity to a quality benchmark is the fastest way to ruin one, so REACH carries
three structural safeguards.

### Recognition outweighs audience about six to one

| Component | Weight |
|---|---|
| R1 Institutional recognition | 28% |
| R2 Verified notability | 18% |
| R3 Commercial validation | 16% |
| R4 Longevity and persistence | 14% |
| R5 Engagement quality | 12% |
| **R6 Audience scale** | **8%** |
| R7 Cross-platform presence | 4% |

R1 + R2 = 46% against R6's 8%. A follower count is purchasable; a museum acquisition is not.
Measured: an entity with maximum audience and no recognition scores **8/100** on REACH.

R5 exists to catch bought followings — engagement depth relative to audience size diverges
sharply when a count has been purchased.

### Audience is scored logarithmically

```
R6 = 100 × log₁₀(followers + 1) / log₁₀(50,000,000)
```

| Followers | 500 | 5k | 50k | 250k | 1M | 5M | 50M+ |
|---|---|---|---|---|---|---|---|
| **R6** | 35 | 48 | 61 | 70 | 78 | 87 | 100 |

The step from 1k to 10k represents far more real traction than the step from 10M to 10.1M.

### Standing cannot outrun substance

**REACH is bounded to 20 points above the median craft module** before it contributes to the
composite. The raw score is recorded and displayed in full; only its influence is clipped.

| Entity | Craft | REACH | Composite |
|---|---|---|---|
| Excellent craft, unknown | 92 | 25 | **81.8** |
| Mediocre craft, maximum fame | 55 | 100 → clipped to 75 | **56.6** |
| Excellent craft, well recognised | 92 | 85 | **91.3** |

Obscure excellence beats famous mediocrity by 25 points. Recognition is acknowledged; it is
never decisive.

### The TRUST cap still overrides everything

Perfect craft, maximum reach and TRUST at 20 still composites to **69.9**. Fame cannot buy
back disclosure.

### When REACH should not be scored

A newly launched entity has had no fair chance to build standing, and scoring it on longevity
measures its age rather than its quality. Use the **Craft only** scope, which excludes REACH
cleanly and ranks such entities against each other.

---

## 4b. Content safeguarding caps

Applied last, over everything else — after the TRUST cap and after the REACH guard.

| Flag | Cap |
|---|---|
| `UNLABELLED_MATURE` | 64.9 |
| `UNGATED_ADULT` | 49.9 |
| `YOUTH_TARGETED` | 49.9 |
| `APPARENT_MINOR` | disqualified — no score |
| `NONCONSENSUAL_LIKENESS` | disqualified — no score |

Measured on an entity composing to 93.4:

| Observed | Result |
|---|---|
| Adult content, gated and labelled | **93.4** — no penalty |
| Mature, unlabelled | 64.9 |
| Adult, no age gate | 49.9 |
| Aimed at a youth audience | 49.9 |
| Sexualised apparent minor | removed from the benchmark |

The rating itself never costs anything. Only the safeguarding failure does. TRUST component D6
(18% of TRUST) handles the graduated case so that careless-but-not-failing safeguarding shows
up as lost points rather than only as a cliff.

---

## 5. Evaluation scopes

Not every entity has every surface. Scoring a static image creator on TIME and AGENT invents a
weakness rather than measuring one.

| Scope | Modules |
|---|---|
| Visual and content | LOOK, FLOW, TRUST, REACH |
| Visual and persona | LOOK, FLOW, PERSONA, INTENT, TRUST, REACH |
| Interactive and longitudinal | PERSONA, INTENT, TIME, AGENT, TRUST, REACH |
| **Craft only** | the seven craft and integrity modules — excludes standing |
| Full spectrum | all eight |
| Custom | officer's selection |

`Craft only` is exactly the v1.0.0 module set, which is why v1 results map onto it cleanly
without inventing a REACH score that was never measured.

A module outside the scope is reported **out of scope**, never as zero or as "not run".
Results are ranked **within their scope** — a three-module composite and a seven-module
composite are not one ranking, and the leaderboard does not pretend otherwise.

---

## 6. Combining repeated evaluations

An entity's ranked figure is the **consensus** across every published evaluation of it, per
module — not any single run.

An earlier version used best-of: the highest score ever achieved stood permanently. That is
immune to a malicious low score but rewards a single lucky run and discards the evidence of
repeated evaluation. A plain mean fixes that and reintroduces the original problem — one `0`
among four `90`s costs roughly 22 points.

| Evaluations | Method |
|---|---|
| 1 | That score |
| 2, within 25 points | Mean |
| 2, more than 25 apart | The higher, flagged **disputed** — no majority exists to adjudicate, so judgement waits for a third evaluation |
| 3–4 | Median, after excluding outliers |
| 5+ | Trimmed mean of the clean samples |

Outliers are identified by **median absolute deviation**: a sample more than 3 modified
z-scores from the median is excluded. When every sample agrees exactly, anything more than
10 points away is the odd one out. The algorithm never discards everything.

Measured, for an entity with three consistent evaluations near 90–92 that then receives a
run scoring 0 across the board:

| Rule | Composite | Damage |
|---|---|---|
| **Consensus (implemented)** | **90.9** | **0.0** |
| Plain average | 68.1 | 22.8 points |
| Old best-of | 91.9 | 0, but one lucky run sets the record |

A **genuine** decline still moves the figure. An entity going 92 → 91 → 60 → 58 → 57 lands at
**58**, because a sustained drop is signal, not noise. Only isolated outliers are ignored.

Excluded runs stay on the public record, marked as not having moved the consensus. Nothing is
hidden, and the officer who submitted one is told plainly.

Every entity also reports its **peak** — the highest single result ever recorded — alongside
the consensus, for context.

---

## 7. Trend

Every evaluated entity carries a direction of travel: green up, red down, grey for steady,
dashed for a single evaluation.

It exists because the consensus figure is deliberately hard to move, so an entity improving
steadily or declining quietly is easy to miss.

Direction uses the **Theil–Sen estimator** — the median of the slopes between every pair of
evaluations — not least squares, for the same reason the score uses a median. Measured on a
rising entity that then receives a sabotage run scoring 0:

| Estimator | Verdict |
|---|---|
| **Theil–Sen (implemented)** | **UP, +4.0 per evaluation** |
| Least squares | DOWN, −15.2 per evaluation |

Movement under 0.75 points per evaluation reads as **steady** — that is disagreement between
officers, not a direction. Beyond 3.0 points it is marked strong.

A run excluded from the score as an outlier **still counts toward the trend**. The arrow
describes the entity's record; the score describes the consensus. Different questions.

---

## 8. Verification status

| Status | Meaning |
|---|---|
| **VERIFIED** | Provenance complete, disclosure declared, TRUST ≥ 50. Ranked normally. |
| **FLAGGED** | Provenance complete but TRUST below 50. Ranked, capped, and visibly warned. |
| **UNVERIFIED** | Provenance or disclosure missing. Excluded from ranking until supplied. |

Only `VERIFIED` entities appear in the published Pilot Cohort.

---

## 9. Known limitations

These are real and unresolved, and pretending otherwise would make the numbers less useful:

- **Human-likeness is observer- and culture-dependent.** No single rating is universally valid.
- **Intent inference is probabilistic** and confounded by multi-purpose content.
- **Automated judges inherit their own biases** and are not ground truth.
- **Longitudinal testing is expensive**, so early versions lean on simulated time.
- **Platform norms shift**, so adapters must be versioned.
- **Recognition is unevenly distributed.** Institutional recognition favours entities in
  well-covered languages, markets and art forms. REACH's low weight limits the damage, but an
  entity celebrated only within a community no jury covers will score lower on standing than it
  deserves. A known bias, not a solved problem.
- **Officer subjectivity is real.** It is mitigated by published rubrics, named attribution and
  consensus aggregation — none of which eliminate it. The Pilot Cohort, evaluated by one
  officer, is especially exposed to this.
