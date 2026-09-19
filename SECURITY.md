# Security and privacy

## Reporting

**Do not open a public issue for a credential exposure or a personal-data leak.**
Use GitHub's private vulnerability reporting on this repository, or contact the maintainers
directly.

For everything else — a bug in the scoring engine, a validation gap — a public issue is fine
and preferred.

## What this repository must never contain

The backing database holds sheets that are permanently excluded from publication:

| Sheet | Why |
|---|---|
| `Users` | Email addresses, password hashes, salts |
| `Sessions` | Session token hashes |
| `OTPs` | One-time codes and their hashes |

Two mechanisms enforce this:

1. `scripts/export_pilot_cohort.py` refuses to read those sheets and prints what it excluded.
2. CI (`.github/workflows/validate.yml`) fails if any credential field name appears under
   `data/`, and `scripts/validate_dataset.py` scans published records for email-shaped strings
   and forbidden field names.

If you regenerate the dataset, do not bypass either.

## Officer identity

Officers are **named on the live site** against runs they publish — attribution is part of
accountability. In the **exported dataset**, officer identity is reduced to a stable
non-reversible pseudonym (`officer-xxxxxxxx`), so the repository does not become a
machine-readable dossier of who evaluated what.

## If you run your own instance

- Set a strong password on the admin account created by `Setup_createOfficer`.
- The server-side pepper lives in Script Properties, not in code. Do not commit it.
- Password hashing is iterated HMAC-SHA256 with a per-user salt plus that pepper. Apps Script
  has no native bcrypt or argon2; this is the strongest stretch that fits the execution limit.
  If you deploy at scale, put a real KDF in front of it.
- Deploy the web app as **Anyone** for public read access. Evaluation is gated by the officer
  role, not by deployment access.
