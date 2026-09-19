# Apps Script engine

The scoring engine and web application. Copy these into a Google Apps Script project —
see [../docs/DEPLOYMENT.md](../docs/DEPLOYMENT.md).

## Files

| File | Contains |
|---|---|
| `appsscript.json` | Manifest and OAuth scopes |
| `Config.gs` | Eight modules, 44 component weights, bands, scopes, intent classes, aggregation, trend and REACH constants |
| `Utils.gs` | IDs, hashing, validation, rate limiting, audit log |
| `Database.gs` | Sheets storage layer, schema, setup and migrations |
| `Auth.gs` | Officer provisioning, OTP activation, sessions, password reset |
| `Mailer.gs` | Transactional email |
| `Scoring.gs` | Composite, bands, module floors, integrity cap, REACH guard, audience scaling, consensus aggregation, Theil–Sen trend |
| `Entities.gs` | Entity registration, bulk import, catalogue, hero carousel selection |
| `Runs.gs` | Evaluation execution, bulk evaluation, aggregation, failure lab |
| `Leaderboard.gs` | Rankings, comparison, public insights aggregation |
| `Api.gs` | RPC router, admin actions, challenge cases |
| `Code.gs` | Web app entry points, HTML serving, public REST endpoints |
| `index.html` | The entire front end — browse, leaderboard, profiles, insights, officer console |

Benchmark **v2.0.0** — eight modules, 45 components.

`Config.gs` is the single source of truth for every weight and threshold. `docs/METHODOLOGY.md`
is generated from it, so changing a weight there and regenerating keeps the documentation
honest.

## Where the rules live

| Rule | Function |
|---|---|
| Composite | `compositeIndex_` in `Scoring.gs` |
| REACH guard and audience log-scaling | `applyReachGuard_`, `audienceToScore_` |
| Content safeguarding caps | `applyContentCaps_`, `CONTENT_FLAGS` |
| Bulk evaluation | `run_bulkTemplate`, `validateEvalRow_`, `run_bulkSubmit` in `Runs.gs` |
| Bands and module floors | `bandFor_`, `BANDS` |
| Integrity cap | `compositeIndex_`, `CFG.TRUST_FLOOR` |
| Consensus aggregation | `aggregateSamples_`, `aggregateRuns_` |
| Trend | `trendFrom_` (Theil–Sen) |
| Scope handling | `coverageFor_`, `SCOPES` |
| Officer gate | `requireOfficer_` in `Auth.gs` |
