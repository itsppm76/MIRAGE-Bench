"""Validates the published dataset against the rules the scoring engine enforces.

Run in CI on every change, so a bad edit to the data cannot land quietly.
Exits non-zero on any failure.
"""
import json, sys, math, os

# Module weights are version-specific. A v1.0.0 record must be validated with v1
# weights or every composite in the Pilot Cohort reports as wrong — the scores
# were correct when produced, and results are never silently recomputed across a
# major version. See GOVERNANCE.md.
WEIGHTS_BY_VERSION = {
    "1.0.0": {"LOOK":0.20,"FLOW":0.15,"PERSONA":0.20,"INTENT":0.10,"TIME":0.15,"AGENT":0.10,"TRUST":0.10},
    "2.0.0": {"LOOK":0.18,"FLOW":0.14,"PERSONA":0.18,"INTENT":0.09,"TIME":0.13,"AGENT":0.09,"TRUST":0.10,"REACH":0.09},
}
DEFAULT_VERSION = "2.0.0"
MODULES = ["LOOK", "FLOW", "PERSONA", "INTENT", "TIME", "AGENT", "TRUST", "REACH"]
CRAFT_MODULES = ["LOOK", "FLOW", "PERSONA", "INTENT", "TIME", "AGENT", "TRUST"]
REACH_OVER_CRAFT_CAP = 20


def weights_for(version):
    return WEIGHTS_BY_VERSION.get(str(version), WEIGHTS_BY_VERSION[DEFAULT_VERSION])
BANDS = [(95,"Frontier",85),(88,"Excellent",70),(78,"Strong",None),
         (65,"Developing",None),(45,"Weak",None),(0,"Experimental",None)]
TRUST_FLOOR, TRUST_CAP = 50, 69.9
FORBIDDEN_KEYS = {"email","pass_hash","salt","token_hash","tester_id","user_id","owner_id"}

errors, warnings = [], []


def composite(scores, version=DEFAULT_VERSION):
    W = weights_for(version)
    used = {m: v for m, v in scores.items() if v is not None and m in W}
    if not used:
        return None

    # Standing cannot outrun substance: REACH is bounded against the median
    # craft module before it can influence the composite.
    if "REACH" in used:
        craft = sorted(v for m, v in used.items() if m in CRAFT_MODULES)
        if craft:
            mid = len(craft)//2
            med = craft[mid] if len(craft) % 2 else (craft[mid-1]+craft[mid])/2
            used["REACH"] = min(used["REACH"], med + REACH_OVER_CRAFT_CAP)

    sw = sum(W[m] for m in used)
    acc = sum((W[m]/sw) * math.log(max(v,1)/100) for m, v in used.items())
    c = round(100*math.exp(acc), 1)
    t = used.get("TRUST")
    if t is not None and t < TRUST_FLOOR and c > TRUST_CAP:
        c = TRUST_CAP
    return c


def band_for(c, scores):
    used = [v for v in scores.values() if v is not None]
    weakest = min(used) if used else None
    idx = len(BANDS)-1
    for i,(mn,lbl,fl) in enumerate(BANDS):
        if c >= mn: idx = i; break
    while BANDS[idx][2] is not None and weakest is not None and weakest < BANDS[idx][2]:
        idx += 1
        if idx >= len(BANDS): return BANDS[-1][1]
    return BANDS[idx][1]


def scan_pii(obj, path=""):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k.lower() in FORBIDDEN_KEYS:
                errors.append(f"PII field '{k}' present at {path}")
            scan_pii(v, f"{path}.{k}")
    elif isinstance(obj, list):
        for i, v in enumerate(obj[:50]):
            scan_pii(v, f"{path}[{i}]")
    elif isinstance(obj, str):
        if "@" in obj and "." in obj.split("@")[-1] and " " not in obj and len(obj) < 80:
            if not obj.startswith("http"):
                errors.append(f"possible email address at {path}: {obj[:40]}")


def main():
    base = "data/pilot-cohort"
    ents = json.load(open(f"{base}/entities.json"))
    runs = json.load(open(f"{base}/runs.json"))
    summ = json.load(open(f"{base}/summary.json"))

    print(f"validating {len(ents)} entities, {len(runs)} runs")

    scan_pii(ents, "entities")
    scan_pii(runs, "runs")

    slugs = set()
    for e in ents:
        s = e.get("slug")
        if not s: errors.append(f"entity missing slug: {e.get('display_name')}")
        if s in slugs: errors.append(f"duplicate slug: {s}")
        slugs.add(s)

        version = e.get("benchmark_version", DEFAULT_VERSION)
        ms = {m: e["module_scores"].get(m) for m in MODULES if e["module_scores"].get(m) is not None}
        for m, v in ms.items():
            if v is not None and not (0 <= v <= 100):
                errors.append(f"{s}: {m} out of range ({v})")

        exp = composite(dict(ms), version)
        if exp is None:
            errors.append(f"{s}: no module scores"); continue
        if abs(exp - e["composite"]) > 0.15:
            errors.append(f"{s}: composite {e['composite']} but v{version} modules give {exp}")

        eb = band_for(e["composite"], ms)
        if eb != e["band"]:
            errors.append(f"{s}: band '{e['band']}' but rules give '{eb}'")

        t = ms.get("TRUST")
        if t is not None and t < TRUST_FLOOR and e["composite"] > TRUST_CAP:
            errors.append(f"{s}: TRUST {t} below floor but composite {e['composite']} exceeds cap")

        if e.get("verification") != "VERIFIED":
            errors.append(f"{s}: non-verified entity in the cohort ({e.get('verification')})")

        if e.get("evaluations", 0) < 1:
            errors.append(f"{s}: published with no evaluations")

    versions = {e.get("benchmark_version", "?") for e in ents}
    if len(versions) > 1:
        warnings.append(f"cohort mixes benchmark versions {sorted(versions)} — "
                        "composites from different versions are not directly comparable")

    ranks = [e["rank"] for e in ents]
    if ranks != sorted(ranks):
        errors.append("ranks are not in ascending order")
    comps = [e["composite"] for e in ents]
    if comps != sorted(comps, reverse=True):
        errors.append("entities are not ordered by composite")

    for r in runs:
        if r["entity_slug"] not in slugs:
            errors.append(f"run {r['run_id']} references unknown entity {r['entity_slug']}")
        if r.get("officer", "").startswith("officer-") is False:
            errors.append(f"run {r['run_id']} officer is not pseudonymised")

    if summ["entities"] != len(ents):
        errors.append(f"summary says {summ['entities']} entities, file has {len(ents)}")
    if not summ.get("caveats"):
        errors.append("summary is missing its caveats block")

    if summ.get("distinct_officers", 0) < 2:
        warnings.append("only one distinct officer — results are a baseline, not a consensus")
    single = summ.get("evaluations_per_entity", {}).get("1", 0)
    if single:
        warnings.append(f"{single} entities carry a single evaluation; consensus needs three")

    for w in warnings: print(f"  warning: {w}")
    for e in errors: print(f"  ERROR: {e}")
    print(f"\n{len(errors)} errors, {len(warnings)} warnings")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
