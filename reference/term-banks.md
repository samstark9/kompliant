---
file-type: machine-readable rules
workspace: kompliant
last-updated: 2026-07-20
status: active, parsed by tools/check.py
---

# Term banks (machine readable)

`tools/check.py` parses this file. Every line of the form below is a live rule; everything else is ignored by the parser.

Format: `RULE | SEVERITY | PATTERN | MESSAGE`

Patterns are Python regexes, applied case-insensitive, line by line against the draft. Severity is BLOCK or FLAG. Rule IDs map to `rules.md`. Edit a row and the checker behavior changes; that is the point.

## Employment implication

A1 | BLOCK | \bprovid\w*\b[^.\n]*\b(training|leads?|benefits|tools|equipment|materials)\b | "Provide" near training/leads/benefits/tools implies employment. Use the available forms: training available, leads made available.
A1 | BLOCK | \b(training|leads?|benefits|tools|equipment|materials)\b[^.\n]*\bprovid\w*\b | "Provide" near training/leads/benefits/tools implies employment. Use the available forms.
A2 | BLOCK | \bjobs?\b | "Job" implies employment. Use career, opportunity, or career progression.
A3 | BLOCK | \bhir(e|es|ed|ing)\b | "Hire" is internal-only. Never in external materials.
A11 | BLOCK | \bemployees?\b | "Employee" is banned. Agents are independent contractors.
A11 | BLOCK | \bsalar(y|ies)\b | "Salary" is banned. Compensation is commission.
A11 | BLOCK | \bwages?\b | "Wages" is banned. Compensation is commission.
A11 | FLAG | (?<!voluntary )\bbenefits\b | Context test: "voluntary benefits available" can be true. Bare "benefits" implies employment. Reviewer judgment.

## Guarantees and promises

A9 | BLOCK | (?<!not )(?<!no )\bguarantee[ds]?\b | No guarantee of results, ever.
A9 | BLOCK | \bget paid forever\b | Banned. The compliant frame is residual income through renewals.
A9 | BLOCK | \bpassive income\b | Banned. Use residual income through renewals.
A9 | FLAG | \beffort\b | Effort language handled with care: effort alone does not guarantee results.
A10 | BLOCK | \bfree\b | "Free" is banned. Always "no cost."

## Titles

A8 | BLOCK | \b(benefits|enrollment)\s+(representative|specialist|rep)\b | Disguise title: removes "sales" from the role. The role is a sales agent role.
A8 | BLOCK | \b((managing|regional|executive|senior|national)\s+)?(director|partner)\b | Title-washing: management titles must carry the word Agent. Check the company profile ladder.
A8 | FLAG | \b(vice\s+)?president\b | Possible title-washing if used as a field management title. May be a legitimate corporate-officer reference. Reviewer judgment.

## Gray areas

B1 | FLAG | \bwork\b | Gray: "do work you really love" can pass. Flag with reasoning; writer decides.
B2 | FLAG | \bpart[- ]?time\b | No early infrastructure supports part-time. Flag the over-promise.
B4 | FLAG | \b(income|job)\s+(stability|security)\b | Stability framing is company-only. Never income or job stability.
B4 | FLAG | \bstable\s+(income|job)\b | Stability framing is company-only. Never income or job stability.
