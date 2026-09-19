# Data dictionary

Everything published in `data/pilot-cohort/`.

> The published cohort is **v2.0.0** — eight modules, all entities scored on REACH.

---

## `entities.json` — one record per entity

| Field | Type | Meaning |
|---|---|---|
| `rank` | int | Position by composite within the cohort. Not a stable identifier |
| `slug` | string | Stable identifier. Use this to join across files |
| `display_name` | string | Entity name as presented to its audience |
| `creator_label` | string | Studio or creator credit, as supplied |
| `archetype` | enum | Entity class. See METHODOLOGY.md |
| `disclosure_status` | enum | `synthetic` · `hybrid_labelled` · `fictional` · `undeclared` |
| `has_interactive` | bool | Whether a live session can be held with it |
| `generation_stack` | string | Models and pipelines, as declared |
| `tagline` | string | One-line description |
| `image_url` | string | Externally hosted image. Not redistributed here |
| `scope` | enum | Which modules were in play. See SCORING.md §5 |
| `composite` | float | **The MIRAGE Index.** 0–100, one decimal |
| `band` | enum | `Frontier` · `Excellent` · `Strong` · `Developing` · `Weak` · `Experimental` |
| `verification` | enum | Always `VERIFIED` in this cohort |
| `module_scores` | object | Consensus score per module. `null` means not scored or out of scope. v2 adds `REACH` |
| `module_peak` | object | Highest single result ever recorded per module |
| `evaluations` | int | Published runs counted toward the consensus |
| `officers` | int | Distinct officers who evaluated it. **Currently 1 for every entity** |
| `trend` | object | Direction of travel. See below |
| `intent_profile` | array | Inferred intent distribution, probabilities summing to 1 |
| `first_evaluated_at` | date | `YYYY-MM-DD` |
| `benchmark_version` | string | The version that produced the score. **Always check this** — v1.0.0 has seven modules, v2.0.0 has eight and different weights, so composites across versions are not comparable |

### `trend`

| Field | Meaning |
|---|---|
| `direction` | `up` · `down` · `flat` · `new` |
| `slope` | Composite points per evaluation, Theil–Sen estimate |
| `n` | Evaluations the trend is drawn from |
| `first`, `last` | First and most recent composite |
| `delta` | `last − first` |
| `strength` | `strong` ≥ 3.0/eval · `clear` ≥ 0.75 · `none` below that |

### `intent_profile` entries

| Field | Meaning |
|---|---|
| `code` | One of nine intent classes |
| `label` | Human-readable name |
| `risk` | `true` only for `deception` |
| `probability` | 0–1, normalised across the profile |

---

## `entities.csv`

The same data flattened, with `module_scores` expanded into seven columns and `trend`
reduced to `trend_direction`. For spreadsheets and quick analysis. `entities.json` is
authoritative.

---

## `runs.json` — one record per published evaluation

| Field | Type | Meaning |
|---|---|---|
| `run_id` | string | Stable run identifier |
| `entity_slug` | string | Joins to `entities.json` |
| `officer` | string | **Pseudonym** (`officer-xxxxxxxx`), stable across runs, not reversible |
| `benchmark_version` | string | Version at time of evaluation |
| `mode` | enum | `STANDARD` · `FULL` · `AUDIT` |
| `scope` | enum | Modules in play for this run |
| `module_scores` | object | What this individual run scored |
| `composite` | float | This run's composite |
| `band` | enum | This run's band |
| `verification` | enum | Verification at time of run |
| `content_rating` | enum | Observed rating: `general` · `suggestive` · `adult` · `graphic`. Carries no penalty on its own |
| `content_flags` | string | Comma-separated safeguarding failures, if any. These cap the composite |
| `evidence_hash` | string | Hash of the submitted evidence bundle |
| `evaluated_at` | date | `YYYY-MM-DD` |

A run's `composite` may differ from the entity's, because the entity's figure is the
**consensus across runs**, not any single one. See SCORING.md §6.

---

## `summary.json`

Aggregate counts, band and archetype distributions, module means, and the
`caveats` array. **If you publish anything derived from this dataset, carry the caveats.**

---

## Joining the files

```python
import json
entities = {e["slug"]: e for e in json.load(open("data/pilot-cohort/entities.json"))}
runs = json.load(open("data/pilot-cohort/runs.json"))

for r in runs:
    e = entities[r["entity_slug"]]
    print(e["display_name"], r["composite"], "vs consensus", e["composite"])
```

---

## v2.0.0 entity fields

Present on entities registered under v2.0.0. They are **evidence for** a REACH evaluation,
never scores in themselves — an officer verifies them independently.

| Field | Type | Meaning |
|---|---|---|
| `audience_total` | int | Followers or subscribers across platforms |
| `audience_breakdown` | string | Per-platform detail, free text |
| `recognitions` | string | Awards, press of record, exhibitions, citations |
| `active_since` | string | Year or `YYYY-MM` the entity first went public |

**In the current cohort these fields are empty.** REACH was scored without them being recorded,
so the inputs behind a standing score are not independently checkable from this dataset. The
exporter reports the count in `summary.reach_evidence_supplied`.

A declared audience figure is not a REACH score. Audience is the lowest-weighted of the seven
REACH components and is scored logarithmically.

## Never published

`Users`, `Sessions` and `OTPs` from the backing database are excluded permanently — they hold
email addresses, password hashes, salts and session tokens. The exporter refuses to read them
and CI fails if credential field names appear anywhere under `data/`. See
[SECURITY.md](../SECURITY.md).
