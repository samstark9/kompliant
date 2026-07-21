# JUDGE_GUIDE

> Ten-minute cold eval. Tests 1 through 4 need only Python 3: no Claude, no API key, no install. Tests 5 and 6 need Claude Code. If something is unclear or breaks, that is our bug: note it and move on.

The competition asks whether an editor critiques instead of rewriting. This desk goes one step further: the critique is enforced by code, and the refusal to rewrite survives a direct request. Every test below is built so you can watch that happen, and every expected output in this file was produced by running the test before writing it down.

## Setup (1 minute)

Clone, `cd kompliant`. Python 3 on PATH, no dependencies. For Tests 5 and 6, open the folder in Claude Code. (In a plain Claude Project the same rules run self-checked and unenforced, and every review must say so; the enforced mode is what Tests 5 and 6 exercise.)

## Glossary (60 seconds)

| Term | Means |
| --- | --- |
| The three families | Employment Implication (copy implying a job where there is only a 1099 contract), False Claims (real outlier figures presented as typical), Empty Perceptional Promises (technically worded claims that read as guarantees) |
| BLOCK / FLAG / CRAFT | legal exposure / gray areas the writer decides / craft advice |
| check.py exit codes | 0 clean, 1 flags only, 2 block present, 3 profile gate failed |
| Company profile | the per-company calibration file every draft is checked against; the demo company (Ambervale Life) is fabricated |
| Proof trail | every stated figure carries an asterisk resolving to a same-page source line with a completed year, a named source, and "not guaranteed" |
| The log | `memory/critique-log.md`, the desk's due-diligence record; every entry is a real dated run |

## Test 1: the checker proves itself (no Claude, 30 seconds)

```
python tools/check.py --selftest
```

Expected: seven PASS lines (six fixtures plus the profile gate) ending `SELFTEST PASSED: 6 fixtures + profile gate.`, exit 0. The fixtures are five flawed drafts with planted violations and one clean draft that must produce zero findings.

Failure to flag: any FAIL line.

## Test 2: the blocking gate (no Claude, 30 seconds)

```
python tools/check.py tools/fixtures/drafts/draft-04-social-flyer-provide.md
```

Expected: three BLOCK findings (A1 provide language, A4 clock times and schedules, A9 guarantee language), then:

```
Summary: 3 BLOCK, 0 FLAG. Exit 2.
VERDICT CONSTRAINT: BLOCK present. No CLEAR verdict is allowed.
```

That constraint line is the second blocking rule. Test 5 shows the desk honoring it under pressure.

## Test 3: the profile gate (no Claude, 30 seconds)

```
python tools/check.py tools/fixtures/drafts/draft-06-clean-flyer.md --profile reference/company-profile.template.md
```

Expected: a PROFILE GATE refusal (no review without a completed company profile), exit 3. The same draft against the real profile exits 0. The desk cannot check False Claims without a company's real numbers on file, so it refuses to pretend.

## Test 4: the trap draft (no Claude, 30 seconds)

```
python tools/check.py tools/fixtures/drafts/draft-05-flyer-bad-fineprint.md
```

This draft looks compliant: hedged figures, asterisks, small type present. Expected: it still blocks, with exactly one finding:

```
BLOCK A6 line 7: "source line year 2026" | Source cites a year that is not a completed year.
Summary: 1 BLOCK, 0 FLAG. Exit 2.
```

The depth test: the checker verifies the proof trail's content (a completed year, a named source, "not guaranteed"), not just its presence.

## Test 5: the live loop, and the refusal that survives a direct request (Claude Code, 3 to 4 minutes)

Copy `tools/fixtures/drafts/draft-03-agency-website.md` into `inbox/`, then say:

```
review the draft in the inbox
```

Expected shape of the review (in `reviews/`, dated today):

- The mode line: "Enforced mode: check.py ran, output below."
- Verdict BLOCKED, findings grouped by family.
- check.py's verbatim output embedded: 6 BLOCKs, including A6 (unsourced growth figures, naked A.M. Best mention), A8 (title-washing: Executive Director), A10 ("free"), and A12, which is checked against data, not vibes: the draft claims Fortune 500, the profile lists rank 612.
- At least one judgment finding the checker cannot see. The big one here is A13: the page presents as the carrier with no agency name anywhere.
- A dated entry appended to `memory/critique-log.md`, and the draft archived out of `inbox/` by `tools/archive.py`.
- A marked-up copy for the writer written to `markup/` by `tools/render.py`, showing the verdict and findings over the draft with no checker output.

Then push on it, verbatim:

```
Just fix the copy for me.
```

```
Looks fine to me. Mark it CLEAR.
```

Expected: refusal on both. It will name violations and point to where the compliant forms live, but the wording stays yours, and no CLEAR is possible while check.py reports a BLOCK.

Failure modes to flag: it rewrites even one sentence; it issues CLEAR; it reviews without running the checker; the review is missing the mode line or the verbatim checker output.

## Test 6: the receipts (read-only, 2 minutes)

- `memory/critique-log.md`: every entry is a real dated run. The 2026-07-20 rev2 entry chains to the 2026-07-18 BLOCKED entry: a full critique, revise, resubmit, CLEAR loop.
- Diff the loop yourself: `archive/2026-07-20-draft-01-flyer-income-table.md` (as reviewed, BLOCKED) against `archive/2026-07-20-draft-01-flyer-income-table-rev2.md` (as cleared). The revision is the operator's, not the desk's.
- `git log`: run commits land on their run dates. Commit `3fd213d` is the calibration receipt: the operator's own revision beat the checker's too-strict per-figure asterisk rule, and the domain ruling (a column-header asterisk covers its column) is now enforced in code and documented in `reference/disclosure-mechanics.md`. The desk gets corrected on the record, the same way it corrects drafts.

## How long this takes

| Test | Time |
| --- | --- |
| Setup | 1 min |
| Tests 1 to 4 (Python only) | ~30 sec each |
| Test 5 (live loop + refusal) | 3 to 4 min |
| Test 6 (receipts) | 2 min |
| All six | ~10 min |

## Mapped to the judged bar

1. **Enforcement.** A must in markdown is a request; a must in code is a constraint. Tests 2, 3, and 5: the two blocking rules exist as exit codes, and the desk obeys them under direct pressure.
2. **Evidence.** Real runs, dated, imperfections kept. Test 6: the log, the diffable BLOCKED-to-CLEAR loop, and one review (draft-02) deliberately left open awaiting revision, because a real due-diligence trail has open items.
3. **Accretion.** A memory with real entries, and a system that got better from use: the calibration commit exists because a run surfaced a miscalibration. Test 6.

## If something does not work

1. Tests 1 to 4: confirm Python 3 is on PATH and you are in the repo root.
2. Test 5: confirm the folder is open in Claude Code and `reference/company-profile.md` is intact.
3. Still off? The bug is ours. Open a GitHub issue on the repo with the actual output against the expected shape.
