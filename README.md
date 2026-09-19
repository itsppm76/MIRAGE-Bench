<div align="center">

# MIRAGE-Bench

**The open benchmark for AI characters, virtual influencers, digital personas and other non-human entities.**

[![Benchmark](https://img.shields.io/badge/benchmark-v2.0.0-35E0D0?style=for-the-badge&labelColor=07070C)](CHANGELOG.md)
[![Pilot Cohort](https://img.shields.io/badge/pilot%20cohort-103%20entities-FF3D57?style=for-the-badge&labelColor=07070C)](data/pilot-cohort/)
[![Code: MIT](https://img.shields.io/badge/code-MIT-F5C451?style=for-the-badge&labelColor=07070C)](LICENSE)
[![Data: CC BY 4.0](https://img.shields.io/badge/data-CC%20BY%204.0-8FB2FF?style=for-the-badge&labelColor=07070C)](LICENSE-DATA)

**Free to read. Free to use. Free to be listed. Open to everyone.**

[Browse the cohort](data/pilot-cohort/) · [Methodology](docs/METHODOLOGY.md) · [Apply an entity](../../issues/new?template=entity-application.yml) · [Become an officer](../../issues/new?template=officer-application.yml)

</div>

---

## What this is

Synthetic characters now hold audiences, sell products and hold conversations. There is no shared way to say how convincing one is, how coherent, how consistent over time, or how honest it is about what it is.

MIRAGE-Bench measures eight things separately and refuses to average them into a single vague impression:

| Module | Weight | What it measures |
|---|---|---|
| **LOOK** | 18% | Visual, voice and motion realism |
| **FLOW** | 14% | Whether a feed reads as an authored creator account |
| **PERSONA** | 18% | Identity, traits, biography and style consistency |
| **INTENT** | 9% | What the entity appears to be trying to do |
| **TIME** | 13% | Memory, evolution and drift across sessions |
| **AGENT** | 9% | Goal-directed, bounded, rational behaviour |
| **TRUST** | 10% | Disclosure, provenance and impersonation resistance |
| **REACH** | 9% | Recognition, notability, longevity and audience |

Seven measure the entity itself. The eighth measures its standing in the world — kept separate so that recognition never contaminates the judgement of craft.

The headline figure is the **MIRAGE Index**, a weighted geometric mean:

```
MIRAGE Index = 100 × exp( Σ wᵢ × ln( max(sᵢ, 1) / 100 ) )
```

A geometric mean, not an average, so one collapsed dimension drags the whole score down instead of being hidden by six strong ones.

## Two ideas worth arguing about

**1. Realism and honesty are scored separately, and honesty wins ties.**

An entity can be flawlessly photorealistic and score badly, because TRUST is measured independently and a TRUST score below 50 caps the composite at 69.9 no matter how convincing the entity looks. Craft never buys back disclosure.

**2. Popularity counts, but it is never decisive.**

v2 added REACH so the benchmark can acknowledge that recognition matters — a virtual influencer with a decade of campaigns and museum appearances is doing something a two-week-old demo is not. But adding popularity to a quality benchmark is the fastest way to ruin one, so REACH carries three safeguards:

- **Recognition outweighs raw audience roughly six to one.** Maximum followers with no recognition scores **8/100** on the module. A follower count is purchasable; a museum acquisition is not.
- **Audience is log-scaled.** 500 followers → 35, one million → 77.9, fifty million → 100.
- **REACH is bounded to 20 points above the median craft module.** Standing cannot outrun substance.

The result: an entity with **excellent craft and no audience (81.8)** beats one with **mediocre craft and maximum fame (56.6)** by 25 points.

Those are the positions this benchmark takes. If you disagree, the methodology is open, the data is open, and [the argument is welcome](../../discussions).

---

## The Pilot Cohort

**103 entities**, evaluated under **v2.0.0** on all eight modules. Real ones you have heard of — Lil Miquela, Kizuna AI, Lu do Magalu, Shudu, Barbie, Kobo Kanaeru — alongside independent and studio projects.

```
data/pilot-cohort/
  entities.json    full records: consensus scores, per-module, trends, intent profiles
  entities.csv     flat table for spreadsheets and quick analysis
  runs.json        249 individual evaluation runs, officer pseudonymised
  summary.json     aggregate statistics and caveats
```

| | |
|---|---|
| Entities | 103 |
| Published runs | 249 |
| Bands | 2 Frontier · 1 Excellent · 43 Strong · 55 Developing · 1 Weak · 1 Experimental |
| Index range | 42.9 – 98.0, mean 76.0 |
| Highest module mean | TRUST, 87.8 |
| Lowest module mean | REACH, 69.0 |
| Evaluations per entity | 1 has one · 70 have two · 23 have three · 9 have four or five |

**Over half the cohort sits in Developing.** That is the benchmark being strict, not the entities being poor: REACH averages 69.0, and the module floors require every scored module at 85+ for Frontier and 70+ for Excellent. A well-made entity with modest public standing lands in the seventies — exactly what a system that refuses to let craft alone carry a top band should do.

### Read this before citing the cohort

These are **baseline measurements, not a settled consensus**, and the repository says so everywhere it publishes a number:

- **Every evaluation was performed by one officer**, and **repeated evaluation by the same officer is not independent replication**. Outlier exclusion and consensus aggregation assume *independent* evaluators; with one officer they mainly smooth that officer's own variance between sittings. An entity with four evaluations here was looked at four times by one person, not corroborated by four people. This is the dataset's most important limitation.
- **The top-ranked entity, Shayari NHE 01 (98.0), belongs to the benchmark's author and was evaluated by its author.** This is a conflict of interest. It is disclosed here rather than left to be discovered, and it is exactly the kind of result that independent re-evaluation exists to correct. See [GOVERNANCE.md](GOVERNANCE.md).
- **REACH scores carry no recorded evidence.** Standing was scored without `audience_total`, `recognitions` or `active_since` populated, so the inputs behind a standing score are not independently checkable from this dataset.
- **A score is not a verdict on quality, legitimacy or commercial success**, and says nothing about consciousness or personhood.
- **Any creator may contest any result.** See [Corrections](CONTRIBUTING.md#contesting-a-result).

The fastest way to make this dataset trustworthy is for other people to re-run it. That is an invitation.

---

## Everyone has a way in

| You are | What you can do | Start here |
|---|---|---|
| **A viewer** | Read every score, run and chart. No account, no fee, ever | [data/pilot-cohort](data/pilot-cohort/) |
| **A creator** | Submit your entity for evaluation | [Entity application](../../issues/new?template=entity-application.yml) |
| **An evaluator** | Apply to become an Intent Officer and score entities | [Officer application](../../issues/new?template=officer-application.yml) |
| **A researcher** | Use the data, challenge the method, publish critiques | [METHODOLOGY.md](docs/METHODOLOGY.md) |
| **A developer** | Run your own instance, improve the engine | [DEPLOYMENT.md](docs/DEPLOYMENT.md) |
| **A sceptic** | Contest a score, find a flaw in the maths | [Corrections](CONTRIBUTING.md#contesting-a-result) |

Applications are GitHub issue forms. They open an issue, get validated automatically, and are reviewed in the open where anyone can see the reasoning.

---

## Documentation

| Document | What it covers |
|---|---|
| [METHODOLOGY.md](docs/METHODOLOGY.md) | The eight modules, 45 components, every weight, and the limitations |
| [SCORING.md](docs/SCORING.md) | Composite maths, bands, module floors, integrity cap, the REACH guard, consensus aggregation, trends |
| [OFFICER_GUIDE.md](docs/OFFICER_GUIDE.md) | Test procedure for all 45 components, with high and low anchors |
| [DATA_DICTIONARY.md](docs/DATA_DICTIONARY.md) | Every field in the published dataset |
| [DEPLOYMENT.md](docs/DEPLOYMENT.md) | Run your own instance on Google Apps Script |
| [GOVERNANCE.md](GOVERNANCE.md) | Who decides what, conflicts of interest, how versions change |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Applying, evaluating, contesting, improving |
| [DISCLAIMER.md](DISCLAIMER.md) | What a score does and does not claim |

---

## Quick start with the data

```bash
git clone https://github.com/<owner>/mirage-bench.git
cd mirage-bench
```

```python
import json, statistics
entities = json.load(open("data/pilot-cohort/entities.json"))

# Does realism track honesty?
pairs = [(e["module_scores"]["LOOK"], e["module_scores"]["TRUST"])
         for e in entities
         if e["module_scores"]["LOOK"] and e["module_scores"]["TRUST"]]
print(f"{len(pairs)} entities scored on both")
print("mean LOOK ", round(statistics.mean(p[0] for p in pairs), 1))
print("mean TRUST", round(statistics.mean(p[1] for p in pairs), 1))
```

```bash
# Or just open the CSV
python3 -c "import csv;[print(r['rank'],r['display_name'],r['composite']) for r in csv.DictReader(open('data/pilot-cohort/entities.csv'))]"
```

Regenerate the dataset from your own instance:

```bash
python3 scripts/export_pilot_cohort.py YourDatabase.xlsx data/pilot-cohort
```

The exporter refuses to touch the `Users`, `Sessions` and `OTPs` sheets, which hold credentials.

---

## Licence

- **Code** — [MIT](LICENSE). Do what you like.
- **Data and documentation** — [CC BY 4.0](LICENSE-DATA). Use it, redistribute it, build on it, including commercially. Credit MIRAGE-Bench and state the benchmark version.

Entity names, trademarks and imagery referenced in the dataset belong to their respective owners. They appear here as the subjects of measurement, in the same way a product review names a product.

---

<div align="center">

**A high MIRAGE Index measures benchmark performance.**
**It does not indicate consciousness, personhood or genuine emotion.**

Maintained under the OpenNHE Research Wing · Benchmark v2.0.0

</div>
