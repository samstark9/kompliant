---
file-type: checklist
workspace: kompliant
last-updated: 2026-07-20
status: active
---

# Verification checklist

The review order. Every review walks this list top to bottom, whole document first. No sampling, no skimming. C4 in `rules.md`: read the entire document front to back.

## 1. Gate

- [ ] Company profile complete (`reference/company-profile.md`, no `[FILL:]` markers). If not: refuse, offer the intake interview.
- [ ] Asset type identified. Pull the matching file from `reference/asset-types/`.

## 2. Deterministic pass (Claude Code only)

- [ ] Run `python tools/check.py <draft> --profile reference/company-profile.md`.
- [ ] Record exit code and verbatim output. Exit 2 means no CLEAR is possible this round.
- [ ] In a plain Claude Project: state self-checked mode, then walk `reference/term-banks.md` manually.

## 3. Copy pass

- [ ] Employment Implication sweep: provide, job, hire, employee, salary, wages, schedules, clock times.
- [ ] Guarantee sweep: guarantee forms, forever language, passive income, unhedged effort language.
- [ ] Title sweep: every title on the page exists in the profile ladder; management titles carry Agent; no disguise titles.
- [ ] Gray areas: work, part-time, flexibility, stability framing. Flag with reasoning.

## 4. Figures pass

- [ ] Every figure hedged or averaged, asterisked, sourced same-page.
- [ ] Figures compared against the profile income table: outlier-as-typical is a False Claim even when the number is real.
- [ ] Timelines in the "typically" shape and consistent with profile averages.
- [ ] Source line cites a completed year and a named source, includes "not guaranteed."

## 5. Facts pass

- [ ] Every publicly checkable claim (rank, ratings, longevity, in-force, claims paid) verified against the profile facts block and, where possible, live sources.
- [ ] Ratings in rating + title + year form and current.
- [ ] Findings reported in the review whether or not the claim survived.

## 6. Brand and imagery pass

- [ ] Material presents the agency's own name, never the carrier's (A13).
- [ ] Imagery licensed and consistent with brand values (A14).
- [ ] Design professionalism noted if warranted (B7, advisory only).

## 7. Layout flags

- [ ] Small type same page as claims, no smaller than 8pt Arial. Unverifiable in plain text: flag for layout check.

## 8. Close

- [ ] Verdict per the output contract in `rules.md`.
- [ ] Review written to `reviews/` as `YYYY-MM-DD-<draft-name>.md`.
- [ ] Entry appended to `memory/critique-log.md`.
- [ ] Escalate to legal review when warranted; say so in the review.
