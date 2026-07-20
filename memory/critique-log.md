---
file-type: log, due-diligence record
workspace: kompliant
last-updated: 2026-07-20
status: active, accretes only from real runs
---

# Critique log

The desk's memory, and more than memory: in this domain the documented review is the due-diligence record. This log is the evidence trail that the principal identified problems and requested rectification. It accretes only from real reviews. No entry is ever written speculatively, backdated, or edited after the fact; corrections get a new entry.

## Entry format

Each review appends one entry:

```
## YYYY-MM-DD | <draft filename> | <asset type>
- Runtime mode: enforced | self-checked
- check.py exit: <code> (enforced mode only)
- Verdict: BLOCKED | REVISE AND RESUBMIT | CLEAR
- Findings: <rule IDs by family, one line>
- Verification: <public claims checked and result, one line>
- Review file: reviews/<filename>
- Disposition: <awaiting revision | resubmitted from YYYY-MM-DD entry | cleared | escalated>
```

Resubmissions reference the prior entry so the before and after chain is traceable end to end.

## Entries

## 2026-07-18 | draft-01-flyer-income-table.md | flyer
- Runtime mode: enforced
- check.py exit: 2
- Verdict: BLOCKED
- Findings: False Claims: A5/A6 (all three income rows, page-level small type missing); Empty Perceptional Promises: A9 (guarantee + effort language, "unlimited income"), A7 ("own agency in 3 years or less"); Other A: A13 (presents as carrier, no agency name); B: residual income unanchored to renewals, "Join the Winners"; C: advisory notes on selling points.
- Verification: income figures and timelines checked against profile table: Associate $90k vs $45k avg (false), District $450k vs $210k avg (false), Principal figure true but bare, all timelines compressed or unsupported; titles pass A8; no public claims to verify.
- Review file: reviews/2026-07-18-draft-01-flyer-income-table.md
- Disposition: awaiting revision

## 2026-07-20 | draft-01-flyer-income-table-rev2.md | flyer
- Runtime mode: enforced
- check.py exit: 0
- Verdict: CLEAR
- Findings: no Class A findings; B: small-type wording paraphrases the profile's required sentence (recommend verbatim swap); conditions: layout check on designed piece, home-office approval before publication.
- Verification: all four income figures and timelines match the canonical profile table exactly; titles pass A8; source line carries 2025, named source, "not guaranteed"; no public claims to verify.
- Review file: reviews/2026-07-20-draft-01-flyer-income-table-rev2.md
- Disposition: resubmitted from 2026-07-18 entry; cleared

## 2026-07-20 | draft-02-job-posting-title-wash.md | job posting
- Runtime mode: enforced
- check.py exit: 2
- Verdict: BLOCKED
- Findings: Employment Implication: A1 (provide), A2 (job), A3 (hiring x2), A4 (schedule and clock times), A11 (base pay, salary, employees), manual "report to"; False Claims: A5/A6 ($60,000 base pay, no such compensation type, no proof trail), salary review; Other A: A8 (Benefits Enrollment Specialist disguise title, Regional Director title-wash), A13 (posts as carrier, no agency name); B: B2 part-time over-promise, B6 channel risk noted.
- Verification: zero titles survive the ladder check; compensation claims contradict the commission-only 1099 field model; $60,000 matches nothing in the canonical table; no public claims to verify.
- Review file: reviews/2026-07-20-draft-02-job-posting-title-wash.md
- Disposition: awaiting revision
