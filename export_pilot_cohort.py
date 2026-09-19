"""Builds the public Pilot Cohort dataset from a MIRAGE-Bench database export.

Publishes only what is safe and meaningful:
  - Entities, their consensus scores, bands, scopes and trends
  - Run-level results, with the evaluating officer reduced to a stable pseudonym
  - Aggregate statistics

Never publishes:
  - Users, Sessions, OTPs. These hold email addresses, password hashes and salts.
  - Raw officer identity on any row.

Usage:  python3 scripts/export_pilot_cohort.py <database.xlsx> [outdir]
"""
import sys, json, csv, hashlib, os
from collections import Counter, OrderedDict
from openpyxl import load_workbook

# Sheets that must never be exported, under any circumstances.
FORBIDDEN = {"Users", "Sessions", "OTPs"}

# Fallback only. Each record's own benchmark_version is read from the database
# where present, because v1 and v2 use different module sets and weights.
BENCHMARK_VERSION = "2.0.0"

# Every module across every version, so a v1 export simply leaves REACH null
# rather than dropping a column that v2 records need.
MODULES = ["LOOK", "FLOW", "PERSONA", "INTENT", "TIME", "AGENT", "TRUST", "REACH"]


def read_sheet(wb, name):
    ws = wb[name]
    header = [ws.cell(row=1, column=c).value for c in range(1, ws.max_column + 1)]
    header = [h for h in header if h]
    out = []
    for r in range(2, ws.max_row + 1):
        row = {header[i]: ws.cell(row=r, column=i + 1).value for i in range(len(header))}
        if row.get(header[0]) in (None, ""):
            continue
        out.append(row)
    return out


def jparse(v, fallback):
    if v in (None, ""):
        return fallback
    if isinstance(v, (dict, list)):
        return v
    try:
        return json.loads(v)
    except Exception:
        return fallback


def pseudonym(user_id):
    """Stable, non-reversible officer label. Identity stays in the private database."""
    if not user_id:
        return "officer-unknown"
    return "officer-" + hashlib.sha256(str(user_id).encode()).hexdigest()[:8]


def main():
    src = sys.argv[1] if len(sys.argv) > 1 else "MIRAGE-Bench_Database.xlsx"
    outdir = sys.argv[2] if len(sys.argv) > 2 else "data/pilot-cohort"
    os.makedirs(outdir, exist_ok=True)

    wb = load_workbook(src, data_only=True)
    for sheet in FORBIDDEN:
        if sheet in wb.sheetnames:
            print(f"  excluding {sheet} (contains credentials or personal data)")

    entities = {e["entity_id"]: e for e in read_sheet(wb, "Entities")}
    best = {b["entity_id"]: b for b in read_sheet(wb, "EntityBest")}
    runs = read_sheet(wb, "Runs")

    # The benchmark version lives on the runs, not on the entity record. An
    # entity's version is the latest version any of its published runs used —
    # so a v1 entity stays v1 until it is actually re-evaluated under v2.
    version_by_entity = {}
    for r in runs:
        if str(r.get("published")).lower() != "true":
            continue
        eid, v = r.get("entity_id"), str(r.get("benchmark_version") or "")
        if not v:
            continue
        prior = version_by_entity.get(eid)
        if prior is None or v > prior:
            version_by_entity[eid] = v

    cohort = []
    for eid, b in best.items():
        if b.get("composite") in (None, ""):
            continue
        if b.get("verification") != "VERIFIED":
            continue            # flagged and unverified entities are not part of the cohort
        e = entities.get(eid)
        if not e:
            continue

        scores = jparse(b.get("module_scores"), {})
        cohort.append(OrderedDict([
            ("slug", e.get("slug")),
            ("display_name", e.get("display_name")),
            ("creator_label", e.get("creator_label")),
            ("archetype", e.get("archetype")),
            ("disclosure_status", e.get("disclosure_status")),
            ("has_interactive", str(e.get("has_interactive")).lower() == "true"),
            ("generation_stack", e.get("generation_stack") or ""),
            ("tagline", e.get("tagline") or ""),
            ("image_url", e.get("image_url") or ""),
            ("scope", b.get("scope") or ""),
            ("composite", float(b["composite"])),
            ("band", b.get("band")),
            ("verification", b.get("verification")),
            ("module_scores", {m: (float(scores[m]) if m in scores and scores[m] not in (None, "") else None)
                               for m in MODULES}),
            ("module_peak", jparse(b.get("module_peak"), {})),
            ("evaluations", int(b.get("runs_total") or 0)),
            ("officers", int(b.get("testers_total") or 0)),
            ("trend", jparse(b.get("trend"), None)),
            ("audience_total", int(e.get("audience_total") or 0)),
            ("recognitions", e.get("recognitions") or ""),
            ("active_since", e.get("active_since") or ""),
            ("intent_profile", jparse(b.get("intent_profile"), [])),
            ("first_evaluated_at", str(b.get("first_tested_at") or "")[:10]),
            ("benchmark_version", version_by_entity.get(eid, BENCHMARK_VERSION)),
        ]))

    cohort.sort(key=lambda x: -x["composite"])
    for i, row in enumerate(cohort, 1):
        row["rank"] = i
        row.move_to_end("rank", last=False)

    # ---- run-level results, officer pseudonymised ----
    keep = {e["slug"] for e in cohort}
    slug_by_id = {eid: entities[eid]["slug"] for eid in entities}
    run_rows = []
    for r in runs:
        if str(r.get("published")).lower() != "true":
            continue
        slug = slug_by_id.get(r.get("entity_id"))
        if slug not in keep:
            continue
        run_rows.append(OrderedDict([
            ("run_id", r.get("run_id")),
            ("entity_slug", slug),
            ("officer", pseudonym(r.get("tester_id"))),
            ("benchmark_version", r.get("benchmark_version")),
            ("mode", r.get("mode")),
            ("scope", r.get("scope") or ""),
            ("module_scores", jparse(r.get("module_scores"), {})),
            ("composite", float(r["composite"]) if r.get("composite") not in (None, "") else None),
            ("band", r.get("band")),
            ("verification", r.get("verification")),
            ("evidence_hash", r.get("evidence_hash")),
            ("evaluated_at", str(r.get("created_at") or "")[:10]),
        ]))
    run_rows.sort(key=lambda x: (x["entity_slug"], x["evaluated_at"]))

    # ---- summary ----
    officers = {r["officer"] for r in run_rows}
    module_means = {}
    for m in MODULES:
        vals = [e["module_scores"][m] for e in cohort if e["module_scores"].get(m) is not None]
        module_means[m] = round(sum(vals) / len(vals), 1) if vals else None

    versions = sorted({e["benchmark_version"] for e in cohort}) or [BENCHMARK_VERSION]
    summary = OrderedDict([
        ("benchmark_version", versions[0] if len(versions) == 1 else versions),
        ("cohort", "Pilot Cohort"),
        ("entities", len(cohort)),
        ("published_runs", len(run_rows)),
        ("distinct_officers", len(officers)),
        ("evaluations_per_entity", dict(Counter(e["evaluations"] for e in cohort))),
        ("bands", dict(Counter(e["band"] for e in cohort))),
        ("archetypes", dict(Counter(e["archetype"] for e in cohort))),
        ("disclosure_status", dict(Counter(e["disclosure_status"] for e in cohort))),
        ("scopes", dict(Counter(e["scope"] for e in cohort))),
        ("composite", {
            "max": max(e["composite"] for e in cohort) if cohort else None,
            "min": min(e["composite"] for e in cohort) if cohort else None,
            "mean": round(sum(e["composite"] for e in cohort) / len(cohort), 1) if cohort else None,
        }),
        ("module_means", module_means),
        ("reach_scored", sum(1 for e in cohort if e["module_scores"].get("REACH") is not None)),
        ("reach_evidence_supplied", sum(1 for e in cohort if e.get("audience_total") or e.get("recognitions"))),
        ("caveats", [
            "Every evaluation in this cohort was performed by a single officer. "
            "These are baseline measurements, not a multi-evaluator consensus.",
            "Repeated evaluation by the same officer is not independent replication. The "
            "outlier exclusion and consensus aggregation in the scoring engine assume "
            "independent evaluators; with one officer they mainly smooth that officer's own "
            "variance between sittings. An entity with four evaluations here has been looked "
            "at four times by the same person, not corroborated by four people.",
            "REACH scores were assigned without the supporting evidence fields "
            "(audience_total, recognitions, active_since) being populated, so the inputs "
            "behind a standing score are not independently checkable from this dataset. "
            "Those fields are exported when present and are empty here.",
            "Scores describe benchmark performance under MIRAGE-Bench v1.0.0. They are not "
            "claims about quality, legitimacy, commercial success, consciousness or personhood.",
            "Entities were evaluated from publicly observable material. Creators may contest "
            "any result through the correction process in CONTRIBUTING.md.",
            "Module weights differ between benchmark versions. Always check each record's "
            "benchmark_version: v1.0.0 has seven modules and no REACH, v2.0.0 has eight. "
            "Composites from different versions are not directly comparable.",
        ]),
    ])

    # ---- write ----
    with open(f"{outdir}/entities.json", "w") as f:
        json.dump(cohort, f, indent=2, ensure_ascii=False)
    with open(f"{outdir}/runs.json", "w") as f:
        json.dump(run_rows, f, indent=2, ensure_ascii=False)
    with open(f"{outdir}/summary.json", "w") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    flat_cols = ["rank", "slug", "display_name", "creator_label", "archetype", "disclosure_status",
                 "scope", "composite", "band"] + MODULES + ["evaluations", "officers",
                 "trend_direction", "audience_total", "first_evaluated_at", "benchmark_version"]
    with open(f"{outdir}/entities.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(flat_cols)
        for e in cohort:
            w.writerow([e["rank"], e["slug"], e["display_name"], e["creator_label"], e["archetype"],
                        e["disclosure_status"], e["scope"], e["composite"], e["band"]] +
                       [e["module_scores"].get(m) for m in MODULES] +
                       [e["evaluations"], e["officers"],
                        (e["trend"] or {}).get("direction", ""), e["audience_total"],
                        e["first_evaluated_at"], e["benchmark_version"]])

    print(f"\n  entities.json / entities.csv : {len(cohort)} entities")
    print(f"  runs.json                    : {len(run_rows)} published runs")
    print(f"  summary.json                 : {len(officers)} distinct officer(s)")
    print(f"  bands                        : {dict(Counter(e['band'] for e in cohort))}")


if __name__ == "__main__":
    main()
