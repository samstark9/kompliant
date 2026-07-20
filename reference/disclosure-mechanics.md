# Disclosure mechanics

The proof-trail requirement from `rules.md` (A5, A6, A7), in mechanical detail. `tools/check.py` enforces the machine-checkable parts.

## The chain

Every stated figure, stat, or fact follows this chain, with no broken links:

1. The claim carries an asterisk at the point of the claim.
2. The asterisk resolves to a source line in the small type.
3. The small type sits on the **same page** as the claim: bottom of page or within the content. Not a different page, not a linked page.
4. Type size is **no smaller than 8pt Arial**.

## Income and achievement figures

- Acceptable forms: "can make up to $X" with performance-based small type, or a stated average with an asterisk. Nothing bare.
- Averages cite the most recently **completed** year. A current, in-progress year is not a completed year and does not qualify.
- The source is named. "Internal sales reporting" is a valid source when that is where the number came from.
- The small type includes "not guaranteed" language. Reference form:

  *Stated averages are per [completed year] end of year internal sales reporting, [Company]. Actual income and time to achieve are based on individual sales and recruiting performance, and are not guaranteed.

- Top-earner figures may accompany averages if labeled as top earner, same convention.
- The asterisk may sit on the column header; a header asterisk covers every figure in that column. "Averages" declared once in the small type covers the page; it does not need repeating beside each figure.

## Public facts and ratings

- Publicly available facts cite the public source in the small type.
- Ratings are cited as rating, rating title, and year: "A.M. Best A (Excellent) Financial Strength Rating, 2025." All three parts, and the rating must be verifiably current.

## What check.py verifies

- Every money figure is covered by an asterisk, on the figure or on its column header.
- A same-page source line exists (a small-type line citing a year and source, containing "not guaranteed").
- The cited year is a completed year.
- Income-context figures carry a hedge ("can make up to" or a stated average).
- Ratings mentions carry rating, title, and year.

Type size and physical placement cannot be verified from a text draft; the editor flags them for the layout check in `reference/verification-checklist.md`.
