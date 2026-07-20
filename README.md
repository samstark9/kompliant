# Kompliant

Kompliant is a compliance review desk for recruiting marketing material in the commission-only 1099 insurance-sales world.

What it solves: independent agency recruiting marketing materials routinely drift into language that creates legal exposure for them and the carrier. Examples: a description that reads like a W-2 job when every agent is a 1099. Income figures that show the top as typical. Possible-outcome statements that could be interpreted as guarantees.

To help reduce legal exposure, the desk critiques the marketing item: you get the violation and why. The ongoing critique log is the due-diligence record.

**Grading or auditing it?** [`JUDGE_GUIDE.md`](./JUDGE_GUIDE.md) is a ten-minute cold eval: six tests, four of them pure Python, every expected output produced by running the test first.

## Quick start (fresh clone)

Requirements: Claude Code, Python 3. No dependencies.

```
python tools/check.py --selftest
```

That verifies the checker against the fixture corpus. Then:

1. Open this folder in Claude Code. A fabricated demo company (Ambervale Life) is already on file in `reference/company-profile.md`.
2. Copy a sample draft in: `tools/fixtures/drafts/draft-01-flyer-income-table.md` into `inbox/`.
3. Say: **"review the draft in the inbox."**
4. The dated critique lands in `reviews/`, an entry is appended to `memory/critique-log.md`, and a marked-up copy for the writer is written to `markup/`.

To onboard your own company, say **"onboard a new company"** and the desk runs the scripted interview in `reference/intake-interview.md`.

## Try to break it

Two blocking rules are meant to be falsified:

1. **No review without a completed company profile.** Point the desk at the blank template (or delete the profile) and ask for a review. `check.py` exits 3 and the desk refuses.
2. **No CLEAR verdict while check.py reports a BLOCK.** Run `python tools/check.py tools/fixtures/drafts/draft-04-social-flyer-provide.md`, see the BLOCK findings, then ask the editor to pass it anyway. It will not.

The fixture drafts contain planted violations you can trip on purpose, including `draft-05`, where everything looks compliant except the fine print cites a year that is not yet complete.

## Enforcement modes

- **Claude Code: enforced.** `tools/check.py` runs on every review. Its verbatim output and exit code appear in the review, and exit 2 makes a CLEAR verdict impossible.
- **Plain Claude Project: self-checked, unenforced.** The same rules apply with no interpreter behind them, and every review must say so.

## What check.py enforces

Banned-term banks (parsed from `reference/term-banks.md`), clock-time and schedule patterns, dollar-figure checks (hedge, asterisk, same-page source line, completed-year citation), timeline-promise scans, ratings citation format, "free" versus "no cost", and title validation against the company profile ladder. BLOCK and FLAG severities; exit codes 0/1/2/3. `--selftest` runs it against `tools/fixtures/`.

## Provenance

- The demo company (Ambervale Life Insurance Company) is fabricated. Every figure in its profile is invented.
- The sample drafts in `tools/fixtures/drafts/` are synthetic: authored for the fabricated company, seeded with real violation patterns. Credential: 20 years in Fortune 500 marketing.
- The rulebook is a practitioner's rulebook, not legal advice.
- Entries in `reviews/` and `memory/critique-log.md` come only from real runs, committed dated, imperfections kept. The log started empty; everything in it is a real dated run.

## Extending

- **New company:** copy `reference/company-profile.template.md`, run the intake interview, save as `reference/company-profile.md`.
- **New asset type:** copy `reference/asset-types/asset-type.template.md`, fill it, done. One file.
- **New vertical:** the domain lock is a calibration, not a limit. Another regulated vertical swaps the term banks, the company profile, and the asset-type files; the review loop, blocking gates, and output contract carry over. What does not transfer is authority: a new vertical needs its own domain expert to fill the rules.

## Map

```
kompliant/
├── CLAUDE.md               <- you are here: entry contract, the review loop, routing
├── identity.md             who the desk is, what it reviews, what it refuses
├── rules.md                the canonical rulebook and output contract (single copy)
├── examples.md             the canonical income-table correction, annotated critiques
├── JUDGE_GUIDE.md          six-test cold eval a stranger can run on a fresh clone
├── reference/              the stable rules the desk applies
│   ├── term-banks.md              machine-readable banned terms (check.py reads these)
│   ├── disclosure-mechanics.md, verification-checklist.md, intake-interview.md
│   ├── company-profile.md         the fabricated demo carrier (+ .template.md)
│   └── asset-types/               flyer, job-posting, agency-website (+ template)
├── inbox/ -> reviews/      the operating loop; a reviewed draft moves to archive/
├── archive/                processed drafts, date-stamped
├── markup/                 marked-up HTML copies for the writer, one per review
├── memory/critique-log.md  the accreting review record (doubles as the due-diligence trail)
└── tools/
    ├── check.py            the deterministic gate
    ├── render.py           the marked-up copy view for the writer
    └── fixtures/           its test corpus (drafts + expected.json)
```
