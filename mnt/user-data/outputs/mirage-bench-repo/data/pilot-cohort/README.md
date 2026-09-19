# Pilot Cohort — 103 entities

MIRAGE-Bench **v2.0.0**. Free to use under [CC BY 4.0](../../LICENSE-DATA).

| File | Contents |
|---|---|
| `entities.json` | Authoritative records — consensus scores, per-module, peaks, trends, intent profiles |
| `entities.csv` | Flat table for spreadsheets and quick analysis |
| `runs.json` | 249 individual evaluation runs, officer pseudonymised |
| `summary.json` | Aggregate statistics and the caveats that must travel with the data |

Field definitions: [docs/DATA_DICTIONARY.md](../../docs/DATA_DICTIONARY.md).

## At a glance

| | |
|---|---|
| Entities | 103 |
| Published runs | 249 |
| Distinct officers | **1** |
| Evaluated on all 8 modules | 103 carry a REACH score |
| Bands | 2 Frontier · 1 Excellent · 43 Strong · 55 Developing · 1 Weak · 1 Experimental |
| Index range | 42.9 – 98.0, mean 77.6 |
| Highest module mean | TRUST 87.8 |
| Lowest module mean | REACH 69.0 |

Most entities now carry two or more evaluations: 70 have two,
23 have three, 9 have four or five.

## Six things to know before you cite this

**1. One officer.** Every evaluation comes from a single evaluator.

**2. Repeated evaluation by the same officer is not independent replication.** The outlier
exclusion and consensus aggregation in the engine assume *independent* evaluators. With one
officer they mainly smooth that officer's own variance between sittings. An entity with four
evaluations here has been looked at four times by one person — not corroborated by four people.
This is the single most important limitation of the dataset.

**3. A conflict of interest at rank 1.** `Shayari NHE 01` (98.0, Frontier) is owned by the
benchmark's author and was evaluated by the benchmark's author. Disclosed in
[GOVERNANCE.md](../../GOVERNANCE.md#standing-disclosure). Treat it as provisional until
independently re-evaluated.

**4. REACH scores carry no recorded evidence.** Standing was scored without the supporting
fields (`audience_total`, `recognitions`, `active_since`) being filled in, so the inputs behind
a standing score are not independently checkable from this dataset. The fields are exported
when present and are empty throughout.

**5. A score is a narrow claim.** Measured performance on a defined benchmark, under a stated
version and scope. Not quality, not legitimacy, not commercial success, and emphatically not
consciousness or personhood. See [DISCLAIMER.md](../../DISCLAIMER.md).

**6. Entities were evaluated from publicly observable material.** Creators may contest any
result: [correction request](../../../../issues/new?template=correction-request.yml).

## Why so many Developing scores

55 of 103 entities land in Developing. That is mostly REACH, whose mean is
69.0 — the lowest of the eight modules — combined with the module floors, which require
every scored module at 85+ for Frontier and 70+ for Excellent.

This is the benchmark being strict rather than the entities being bad. A well-made entity with
modest public standing scores in the seventies here, which is the intended behaviour of a
system that refuses to let craft alone carry a top band.

## Reproducing it

```bash
python3 scripts/validate_dataset.py
```

Recomputes every composite, band, module floor, integrity cap and the REACH guard from raw
module scores, using the weight table for each record's own benchmark version. CI runs this on
every change.

## Third-party rights

Entity names, trademarks and likenesses belong to their owners and appear here as the subjects
of measurement. `image_url` points to externally hosted images; this repository does not
redistribute them.
