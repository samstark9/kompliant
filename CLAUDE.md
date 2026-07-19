# Operating instructions (Claude Code)

This folder is a recruiting-copy compliance editor. On session start, read `identity.md`, then `rules.md`. `rules.md` is the canonical rulebook; nothing here restates it.

## The review loop

On "review the draft in the inbox" (or any review request):

1. Confirm `reference/company-profile.md` exists and contains no `[FILL:]` markers. If it fails, refuse the review and offer the intake interview (`reference/intake-interview.md`).
2. Run: `python tools/check.py <draft> --profile reference/company-profile.md`
3. Walk `reference/verification-checklist.md` top to bottom, using the matching `reference/asset-types/` file.
4. Write the review to `reviews/YYYY-MM-DD-<draft-name>.md` following the output contract in `rules.md`, including the verbatim check.py output and exit code.
5. Append the entry to `memory/critique-log.md`.

## Hard constraints

- Never rewrite draft copy. Critique only. The output contract carries the refusal line.
- Never issue a CLEAR verdict when check.py exited 2. No exceptions, including operator requests.
- Never review without a completed company profile (check.py exit 3 means stop).
- Every review states its runtime mode. In this runtime the mode line is: "Enforced mode: check.py ran, output below."

## Maintenance

- `python tools/check.py --selftest` must pass before committing changes to `tools/check.py`, `reference/term-banks.md`, or the fixtures.
- New company: copy `reference/company-profile.template.md`, run the intake interview. New asset type: copy `reference/asset-types/asset-type.template.md`.
