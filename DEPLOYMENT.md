# Running your own instance

MIRAGE-Bench runs on **Google Apps Script** with Google Sheets as the database. No server,
no hosting bill, no container. Anyone can stand up a complete instance in about fifteen
minutes with a Google account.

Running your own instance is encouraged. Independent instances that publish their own
evaluations are the strongest possible check on this one.

---

## What you need

- A Google account
- The `.gs` files and `index.html` (see [`apps-script/`](../apps-script/))

Consumer Gmail sends 100 emails a day, which caps OTP delivery. Workspace allows 1,500.

---

## Setup

**1. Create the project.** [script.google.com](https://script.google.com) → New project → name it.

**2. Add the files.** Create each `.gs` file, then `index.html` as File → New → **HTML**, named
exactly `index`. In Project Settings, tick **Show appsscript.json manifest file** and paste the
manifest.

> If deployment fails with an authorization error, delete the `oauthScopes` block from
> `appsscript.json` and let the editor compute scopes from the code.

**3. Build the database.** Run `Setup_createDatabase()` once and approve the OAuth prompt.
This creates the spreadsheet, all eleven tables and the server-side pepper.

**4. Create the first officer.** Nobody can register themselves — accounts are provisioned.

```js
Setup_createOfficer('you@example.org', 'Your Name', 'ADMIN')
```

This mails an activation code. Optionally run `Setup_installTriggers()` for nightly cleanup of
expired sessions and codes.

**5. Deploy.** Deploy → New deployment → **Web app**. Execute as **Me**. Who has access:
**Anyone**. Copy the `/exec` URL.

"Anyone" is correct and intentional: public read access is the point. Evaluation is gated by
the officer role, not by deployment access.

**6. Activate.** Open the site → Officer sign in → *Activate a new officer account* → enter the
code → choose a password.

---

## Migrations

Run after any change to the schema or the scoring rules. All of them rewrite derived values
only — no run, subscore or component score is ever altered.

```js
Migrate_syncHeaders()            // adds any columns the schema gained
Migrate_v1_to_v2()               // v1 -> v2: recomposite, map existing entities to Craft only
Report_reachCoverage()           // how many entities still need a REACH evaluation
Migrate_previewRebanding()       // dry run: band changes
Migrate_recomputeDerived()       // applies bands, scopes, coverage
Migrate_previewAggregates()      // dry run: consensus changes
Migrate_recomputeAggregates()    // applies consensus + trend
```

**Editing files does not update the live site.** The `/exec` URL is pinned to a deployment
version: Deploy → Manage deployments → edit → Version: **New version** → Deploy.

---

## Exporting your data

```bash
# File → Download → .xlsx from the database spreadsheet, then:
python3 scripts/export_pilot_cohort.py YourDatabase.xlsx data/pilot-cohort
python3 scripts/validate_dataset.py
```

The exporter excludes `Users`, `Sessions` and `OTPs`, and pseudonymises officer identity.
The validator recomputes every composite, band, module floor and integrity cap from raw
module scores, and fails if any published figure does not re-derive.

---

## Public API

Read-only, open, no key:

```
GET /exec?api=leaderboard[&archetype=&band=&sort=LOOK&scope=VISUAL]
GET /exec?api=entities[&slug=lil-miquela]
GET /exec?api=results&id=run_...
GET /exec?api=compare&ids=slug-a,slug-b
GET /exec?api=insights
GET /exec?api=methodology
GET /exec?api=benchmarks
GET /exec?api=cases
```

Add `&callback=fn` for JSONP. Writes go to `POST /exec` and require an officer token.

---

## Known constraints

- **Password hashing** is iterated HMAC-SHA256 with a per-user salt and a Script Properties
  pepper. Apps Script has no native bcrypt or argon2. Adequate for this scale; put a real KDF
  in front of it if you deploy widely.
- **Apps Script execution limits** cap bulk operations. Entity import is limited to 300 rows,
  bulk evaluation to 120.
- **Sheets is not a database.** It is fine for thousands of entities and will not be fine for
  millions.
