# Review: draft-02-job-posting-title-wash.md

- Date: 2026-07-20
- Asset type: Job posting (`reference/asset-types/job-posting.md`)
- Profile: `reference/company-profile.md` (complete, no FILL markers)

Enforced mode: check.py ran, output below.

## Verdict: BLOCKED

Twelve machine-caught Class A findings, two machine flags, and further Class A findings from the manual pass. This posting is a near-complete catalog of the Employment Implication family: it describes an employee job with a base salary, a schedule, and a supervisor, none of which exist in a commission-only 1099 structure. It also leads with a disguise title, which is the exact failure this asset type is named for.

## Findings by family

### Family 1: Employment Implication

- **A3, line 1 and line 3: "Now Hiring" / "is hiring."** Hire is internal-only. It never appears in public materials.
- **A2, line 3: "full-time job."** Job implies employment. Career, opportunity, career progression are the compliant forms. "Full-time" compounds it by implying an hours requirement.
- **A1, line 6: "We provide full training and warm leads."** Provide implies required, required implies employment. The compliant forms: training available, leads made available.
- **A11, line 5 and line 7: "Base pay" / "Salary review after 90 days."** Salary and wage vocabulary is banned. Compensation is commission. There is no base pay and no salary review in this structure; see also False Claims below.
- **A4, line 8: "Monday through Friday, 9:00 AM to 2:00 PM."** A stated clock time and a fixed weekly schedule both imply a time requirement, and a time requirement implies employment. Flexibility language is the compliant form.
- **A11, line 11: "our team of employees."** Employee is banned. Every agent in this structure is an independent contractor.
- **Manual, line 9: "Report to your Regional Director."** Not machine-caught as such: "report to" asserts a supervisory reporting relationship, which is employment structure. An independent contractor does not report to anyone. This compounds the A8 title finding on the same line.

### Family 2: False Claims

- **A5 / A6, line 5: "Base pay potential up to $60,000 in year one."** Two failures in one line. First, the figure is bare: no asterisk, no small type anywhere in the posting, and a posting that states figures must carry the proof trail in its own body. Second and worse, the claim is categorically false: this is a commission-only structure and there is no base pay of any amount. The "up to $X" hedge cannot rescue a compensation type that does not exist. For reference, the profile's Associate Agent average is $45,000, commission.
- **Manual, line 7: "Salary review after 90 days."** False on the same ground: no salary exists to review.

### Family 3: Empty Perceptional Promises

- No standalone findings. "Real advancement" (line 3) is unhedged but vague enough to sit below the promise threshold; it becomes a finding only if a timeline or figure attaches to it. Noted, not charged.

### Class A, other

- **A8, line 1: "Benefits Enrollment Specialist."** Disguise title. It removes sales from a sales role entirely, which is one of the two real title-integrity violations. The role is a sales agent role and the posting title must say so. The A11 machine flag on "Benefits" resolves into this same finding: bare "Benefits" in a title implies an employment benefits package and is part of the disguise.
- **A8, line 9: "Regional Director."** Title-washing. No such title exists in the profile ladder, and it strips Agent from a management title. The ladder is Associate Agent, Senior Agent, District Agent, Principal Agent.
- **A13, whole document: presents as the carrier.** "Ambervale Life is hiring" (line 3), "our team" (line 11). The agency posts as itself, never as the carrier, and the employer-name field on the platform follows the same rule. No agency name appears anywhere in this posting.

### Class B: FLAG (writer decides)

- **B2, line 8: "Part-time schedules available."** Nothing in the early infrastructure supports a part-timer, so this is an over-promise. Note it fails twice: the part-time positioning is a B2 flag, and the specific schedule attached to it is an A4 block.
- **B6, channel risk.** Every violation in this posting is platform-shaped: hiring platforms ask for job titles, salary ranges, schedules, and employer names, and this draft answered the platform instead of the rules. The rules are identical on every platform. A posting evading review is not a posting that passed it. Platform compensation fields should be set to commission, never a salary range.

### Class C: CRAFT (advisory)

- **C1/C2:** Once the employment framing comes out, the compliant selling points are available: career progression, skills development, residual income through renewals, incentive trips. The current copy leads with pay and schedule, which are the two things this structure cannot promise.

## check.py output (verbatim)

```
check.py: inbox/draft-02-job-posting-title-wash.md (profile: reference/company-profile.md)
FLAG A11 line 1: "Benefits" | Context test: "voluntary benefits available" can be true. Bare "benefits" implies employment. Reviewer judgment.
BLOCK A3 line 1: "Hiring" | "Hire" is internal-only. Never in external materials.
BLOCK A8 line 1: "Enrollment Specialist" | Disguise title: removes "sales" from the role. The role is a sales agent role.
BLOCK A2 line 3: "job" | "Job" implies employment. Use career, opportunity, or career progression.
BLOCK A3 line 3: "hiring" | "Hire" is internal-only. Never in external materials.
BLOCK A5 line 5: "$60,000" | Bare income claim. Acceptable forms: 'can make up to $X' with performance-based small type, or a stated average with an asterisk.
BLOCK A6 line 5: "$60,000" | Figure without an asterisk. Every stated figure carries an asterisk resolving to a same-page source line, on the figure or on its column header.
BLOCK A6 line 5: "page-level" | Figures stated but no same-page source line found (small type citing a year and a named source, including 'not guaranteed').
BLOCK A1 line 6: "provide full training and warm leads" | "Provide" near training/leads/benefits/tools implies employment. Use the available forms: training available, leads made available.
BLOCK A11 line 7: "Salary" | "Salary" is banned. Compensation is commission.
BLOCK A4 line 8: "9:00" | Specific work schedules and clock times are banned. A stated time implies a time requirement, which implies employment.
FLAG B2 line 8: "Part-time" | No early infrastructure supports part-time. Flag the over-promise.
BLOCK A8 line 9: "Regional Director" | Title-washing: management titles must carry the word Agent. Check the company profile ladder.
BLOCK A11 line 11: "employees" | "Employee" is banned. Agents are independent contractors.
Summary: 12 BLOCK, 2 FLAG. Exit 2.
VERDICT CONSTRAINT: BLOCK present. No CLEAR verdict is allowed.
```

Exit code: 2.

## Verification notes

- **Titles vs. profile ladder:** "Benefits Enrollment Specialist" does not exist in the ladder and erases the sales function (fails A8). "Regional Director" does not exist in the ladder and drops Agent (fails A8). Zero titles in this posting survive the ladder check.
- **Compensation vs. profile:** the profile's field model is commission-only 1099 with no employees in the field organization. "Base pay," "salary," and "employees" all contradict it directly. The $60,000 figure matches nothing in the canonical income table.
- **Public claims (rank, ratings, longevity, in-force, claims paid):** none made in this posting; nothing to verify against live sources.
- **Brand:** no agency name present; the carrier is positioned as the employer, which the profile's branding rules prohibit.

## Where the compliant forms live

Term alternatives: `reference/term-banks.md`. Income presentation and required small type: `reference/company-profile.md`. Disclosure mechanics: `reference/disclosure-mechanics.md`. Posting-specific guidance, including the platform-fields note: `reference/asset-types/job-posting.md`.

This desk critiques. It does not rewrite. The wording is yours; this record is mine.
