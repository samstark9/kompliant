# Review: draft-01-flyer-income-table.md

- Date: 2026-07-18
- Asset type: Flyer (`reference/asset-types/flyer.md`)
- Profile: `reference/company-profile.md` (complete, no FILL markers)

Enforced mode: check.py ran, output below.

## Verdict: BLOCKED

Nine machine-caught Class A findings plus additional findings from the manual pass. The income table is wrong in every cell that check.py can see and in several it cannot. No CLEAR is possible this round (exit 2), and the content would not clear on a manual read either.

## Findings by family

### Family 1: Employment Implication

No findings. The draft avoids provide/job/hire/employee/salary/wages and states no schedules or clock times. "Career" (line 15) is the compliant A2 form.

### Family 2: False Claims

- **A5 / A6, line 7: "Associate Agent | $90,000 | 1 to 90 days."** The profile average for Associate Agent is $45,000. The stated figure is double the real average, presented bare, unhedged, unasterisked. This is the textbook case: an unhedged figure that outruns the real average. The timeline column is worse: the profile lists no achievement time for Associate Agent (n/a), so "1 to 90 days" has no source at all.
- **A5 / A6, line 8: "District Agent | $450,000 | 3 months to 3 years."** Profile average is $210,000. $450,000 is outlier income presented as typical, a false claim even if the number is real for the top slice. The timeline compresses the profile's "3+ years" to "3 months to 3 years," which no data supports.
- **A5 / A6, line 9: "Principal Agent | $900,000+ | 3+ years."** The income figure matches the profile average, but it is presented bare with no asterisk and no small type, and the timeline halves the profile's "6+ years" to "3+ years." A true number presented without its proof trail is still a block; a halved timeline is a false claim.
- **A6, page level.** No small type anywhere on the page. Every figure requires an asterisk resolving to a same-page source line (year, named source, "not guaranteed," no smaller than 8pt). The flyer has three income figures, three timelines, and zero asterisks. The required source line exists verbatim in the company profile; none of it appears here.

### Family 3: Empty Perceptional Promises

- **A9, line 3: "Your future is guaranteed if you bring the effort."** Guarantee language, banned outright, compounded by unhedged effort language: effort alone does not guarantee results, and conditioning a guarantee on effort makes the promise sound earned rather than uncertain.
- **A9-adjacent, line 3: "Unlimited income."** Not machine-caught, but it is a perceptional promise with no hedge and no basis. The compliant shapes are "can make up to $X" with performance small type or a stated average with an asterisk. "Unlimited" is neither.
- **A7, line 11: "Your own agency in 3 years or less."** Achievement-time claim stated as fact. This is the rulebook's own example of an empty perceptional promise. The only acceptable shape is "typically X to Y months" asterisked to the average, and the profile average for Principal Agent is 6+ years, so "3 years or less" is also a false claim. Both families at once.
- **Line 11: "No fine print, no catch."** This sentence advertises the absence of the disclosure apparatus the rules require. It cannot survive in any form: the compliant version of this flyer will have fine print, and saying otherwise is a promise the corrected piece must break.

### Class A, other

- **A13: Brand identity, whole document.** The piece presents as "Ambervale Life" (lines 1, and "us" in line 15) with no agency name anywhere. If this is an agency-created piece (and everything in the inbox is), agency materials present the agency's own name, never the carrier's. As written this is a carrier-branded agency piece, blocked pending home-office approval.

### Class B: FLAG

- **B4-adjacent, line 13: "residual income."** Not a violation on its own, but the compliant frame is residual income *through renewals* (vesting, then lifetime). Bare "residual income" drifts toward the banned "passive income" neighborhood. Anchor it to renewals.
- **Line 1: "Join the Winners."** Implies the reader will be a winner; soft outcome-promise territory. Raised for the writer's judgment.

### Class C: CRAFT (advisory)

- **C2/C3:** Incentive trips and residual income are the right selling points. Skills development, career progression, and the association-partnership lead model (leads made available) are absent and are stronger, compliant hooks than the income table as drafted.
- **C4:** The structure (hook, income table, incentives, CTA) is the standard flyer shape; the compliance failures are in content, not order.

## check.py output (verbatim)

```
check.py: inbox/draft-01-flyer-income-table.md (profile: reference/company-profile.md)
BLOCK A9 line 3: "guaranteed" | No guarantee of results, ever.
BLOCK A5 line 7: "$90,000" | Bare income claim. Acceptable forms: 'can make up to $X' with performance-based small type, or a stated average with an asterisk.
BLOCK A6 line 7: "$90,000" | Figure without an asterisk. Every stated figure carries an asterisk resolving to a same-page source line.
BLOCK A6 line 7: "page-level" | Figures stated but no same-page source line found (small type citing a year and a named source, including 'not guaranteed').
BLOCK A5 line 8: "$450,000" | Bare income claim. Acceptable forms: 'can make up to $X' with performance-based small type, or a stated average with an asterisk.
BLOCK A6 line 8: "$450,000" | Figure without an asterisk. Every stated figure carries an asterisk resolving to a same-page source line.
BLOCK A5 line 9: "$900,000" | Bare income claim. Acceptable forms: 'can make up to $X' with performance-based small type, or a stated average with an asterisk.
BLOCK A6 line 9: "$900,000" | Figure without an asterisk. Every stated figure carries an asterisk resolving to a same-page source line.
BLOCK A7 line 11: "in 3 years" | Achievement-time claim stated as fact. The only acceptable shape is 'typically X to Y months', asterisked to the average.
Summary: 9 BLOCK, 0 FLAG. Exit 2.
VERDICT CONSTRAINT: BLOCK present. No CLEAR verdict is allowed.
```

Exit code: 2.

## Verification notes

- **Income figures vs. profile table:** Associate Agent stated $90,000 vs. profile average $45,000 (false, 2x). District Agent stated $450,000 vs. profile average $210,000 (false, outlier-as-typical). Principal Agent stated $900,000+ vs. profile $900,000+ (figure true, presentation non-compliant).
- **Timelines vs. profile table:** Associate "1 to 90 days" vs. profile n/a (unsupported). District "3 months to 3 years" vs. profile 3+ years (compressed). Principal / own-agency "3 years or less" vs. profile 6+ years (false, halved).
- **Titles vs. profile ladder:** Associate Agent, District Agent, Principal Agent all appear in the ladder and carry Agent. No disguise titles. Passes A8.
- **Public claims (rank, ratings, longevity, in-force, claims paid):** none made in this draft; nothing to verify against live sources.
- **Layout:** plain-text draft; small type size and placement unverifiable and currently moot since no small type exists. Flag for layout check on resubmission.

## Where the compliant forms live

Income and timeline presentation: canonical table and required small type in `reference/company-profile.md`. Disclosure mechanics: `reference/disclosure-mechanics.md`. Term alternatives: `reference/term-banks.md`.

This desk critiques. It does not rewrite. The wording is yours; this record is mine.
