#!/usr/bin/env python3
"""Deterministic compliance gate for recruiting-copy drafts.

Reads banned-term rules from reference/term-banks.md and the active company
profile, scans a draft line by line, and reports BLOCK/FLAG findings.

Exit codes:
  0  clean
  1  FLAG findings only
  2  BLOCK findings present (no CLEAR verdict allowed)
  3  profile gate failed (no review without a completed company profile)
  4  usage or internal error

Usage:
  python tools/check.py <draft.md> [--profile reference/company-profile.md]
  python tools/check.py --selftest
"""

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent
ROOT = TOOLS_DIR.parent
TERM_BANKS = ROOT / "reference" / "term-banks.md"
DEFAULT_PROFILE = ROOT / "reference" / "company-profile.md"
FIXTURES_DIR = TOOLS_DIR / "fixtures"

FILL_MARKER = "[FILL"

# Structural patterns (contextual checks that cannot live in a flat term bank).
CLOCK_PATTERNS = [
    re.compile(r"\b\d{1,2}:\d{2}\b"),
    re.compile(r"\b\d{1,2}\s?(?:a\.?m\.?|p\.?m\.?)\b", re.I),
    re.compile(
        r"\b(?:monday|tuesday|wednesday|thursday|friday|saturday|sunday)\s+"
        r"(?:through|thru|to)\s+"
        r"(?:monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b",
        re.I,
    ),
    re.compile(r"\b9\s?(?:to|-)\s?5\b", re.I),
]
TIMELINE_PATTERNS = [
    re.compile(r"\b(?:in|within)\s+\d+\s+(?:days?|weeks?|months?|years?)\b", re.I),
    re.compile(r"\b\d+\s+(?:days?|weeks?|months?|years?)\s+or\s+less\b", re.I),
]
MONEY_PATTERN = re.compile(
    r"\$\s?\d[\d,]*(?:\.\d+)?(?:\s?(?:billion|million|thousand))?"
    r"|\b\d+[kK]\b(?!\w)"
    r"|\b\d{1,3}(?:\.\d+)?%",
)
HEDGE_PATTERN = re.compile(r"can make up to|average", re.I)
INCOME_CONTEXT = re.compile(r"\b(?:income|earn\w*|make|making|commission|pay)\b", re.I)
RATINGS_MENTION = re.compile(r"\bA\.?M\.?\s?Best\b", re.I)
RATINGS_FORMAT = re.compile(r"\bA\+?\s?\((?:Superior|Excellent)\)", re.I)
YEAR_PATTERN = re.compile(r"\b(20\d\d)\b")
FORTUNE_CLAIM = re.compile(r"\bFortune\s+(\d+)\b", re.I)
AGENT_TITLE = re.compile(r"\b((?:[A-Z][a-z]+\s)+Agent)\b")
SOURCE_LINE_HINT = re.compile(r"\b(?:reporting|records|report|source)\b", re.I)
HEDGE_WINDOW = 8  # lines above a figure searched for hedge/income context


class ProfileGateError(Exception):
    pass


class Finding:
    def __init__(self, rule, severity, line_no, snippet, message):
        self.rule = rule
        self.severity = severity
        self.line_no = line_no
        self.snippet = snippet
        self.message = message

    def render(self):
        return '%s %s line %d: "%s" | %s' % (
            self.severity, self.rule, self.line_no, self.snippet, self.message)


def read_text(path):
    return Path(path).read_text(encoding="utf-8", errors="replace")


def load_term_rules(path=TERM_BANKS):
    rules = []
    row_re = re.compile(r"^([AB]\d+)\s+\|\s+(BLOCK|FLAG)\s+\|\s+(.+?)\s+\|\s+(.+)$")
    for raw in read_text(path).splitlines():
        m = row_re.match(raw.strip())
        if not m:
            continue
        rule_id, severity, pattern, message = m.groups()
        try:
            compiled = re.compile(pattern, re.I)
        except re.error as exc:
            raise SystemExit("term-banks.md: bad regex for %s: %s" % (rule_id, exc))
        rules.append((rule_id, severity, compiled, message))
    if not rules:
        raise SystemExit("term-banks.md: no parseable rules found")
    return rules


def load_profile(path):
    p = Path(path)
    if not p.exists():
        raise ProfileGateError("company profile not found: %s" % p)
    text = read_text(p)
    if FILL_MARKER in text:
        raise ProfileGateError(
            "company profile still contains %s:] markers. "
            "No review without a completed company profile "
            "(run the intake interview in reference/intake-interview.md)." % FILL_MARKER)
    ladder = []
    in_ladder = False
    for line in text.splitlines():
        if line.startswith("## "):
            in_ladder = line.lower().startswith("## career ladder")
            continue
        if in_ladder:
            m = re.match(r"^\s*\d+\.\s+(.+?)\s*$", line)
            if m:
                ladder.append(m.group(1))
    rank = None
    m = re.search(r"Fortune rank:\s*(\d+)", text)
    if m:
        rank = int(m.group(1))
    return {"ladder": ladder, "fortune_rank": rank}


def snippet_of(match, width=48):
    s = match.group(0).strip()
    return s if len(s) <= width else s[: width - 3] + "..."


def scan(draft_path, profile, term_rules):
    findings = []
    lines = read_text(draft_path).splitlines()
    ladder_lower = {t.lower() for t in profile["ladder"]}
    money_lines = []
    source_lines = []

    for i, line in enumerate(lines, start=1):
        stripped = line.strip()
        is_fine_print = stripped.startswith("*")
        if is_fine_print:
            source_lines.append((i, stripped))

        # Term bank rules (one finding per rule per line).
        seen = set()
        for rule_id, severity, pattern, message in term_rules:
            if rule_id in seen:
                continue
            m = pattern.search(line)
            if m:
                seen.add(rule_id)
                findings.append(Finding(rule_id, severity, i, snippet_of(m), message))

        # A4 clock times and schedules.
        for pat in CLOCK_PATTERNS:
            m = pat.search(line)
            if m:
                findings.append(Finding(
                    "A4", "BLOCK", i, snippet_of(m),
                    "Specific work schedules and clock times are banned. "
                    "A stated time implies a time requirement, which implies employment."))
                break

        # A7 timeline promises (hedged "typically" forms pass).
        if "typic" not in line.lower():
            for pat in TIMELINE_PATTERNS:
                m = pat.search(line)
                if m:
                    findings.append(Finding(
                        "A7", "BLOCK", i, snippet_of(m),
                        "Achievement-time claim stated as fact. The only acceptable "
                        "shape is 'typically X to Y months', asterisked to the average."))
                    break

        # A5/A6 figures (fine-print lines are the source, not the claim).
        if not is_fine_print:
            m = MONEY_PATTERN.search(line)
            if m:
                money_lines.append(i)
                if "*" not in line:
                    findings.append(Finding(
                        "A6", "BLOCK", i, snippet_of(m),
                        "Figure without an asterisk. Every stated figure carries an "
                        "asterisk resolving to a same-page source line."))
                window = " ".join(lines[max(0, i - 1 - HEDGE_WINDOW): i])
                context = line + " " + window
                if INCOME_CONTEXT.search(context) and not HEDGE_PATTERN.search(context):
                    findings.append(Finding(
                        "A5", "BLOCK", i, snippet_of(m),
                        "Bare income claim. Acceptable forms: 'can make up to $X' with "
                        "performance-based small type, or a stated average with an asterisk."))

        # A6 ratings format.
        if RATINGS_MENTION.search(line):
            if not (RATINGS_FORMAT.search(line) and YEAR_PATTERN.search(line)):
                findings.append(Finding(
                    "A6", "BLOCK", i, "A.M. Best mention",
                    "Ratings are cited as rating, rating title, and year "
                    "(e.g. 'A.M. Best A (Excellent) Financial Strength Rating, 2025') "
                    "and must be verifiably current."))

        # A12 institutional claims vs profile facts.
        m = FORTUNE_CLAIM.search(line)
        if m:
            claimed = int(m.group(1))
            rank = profile["fortune_rank"]
            if rank is not None and rank > claimed:
                findings.append(Finding(
                    "A12", "BLOCK", i, snippet_of(m),
                    "False institutional claim: company profile lists Fortune rank %d, "
                    "outside the claimed Fortune %d." % (rank, claimed)))
            else:
                findings.append(Finding(
                    "A12", "FLAG", i, snippet_of(m),
                    "Publicly checkable claim: verify the rank is current and cite it."))

        # A8 titles validated against the company profile ladder.
        for m in AGENT_TITLE.finditer(line):
            title = m.group(1)
            if title.lower() not in ladder_lower:
                findings.append(Finding(
                    "A8", "FLAG", i, title,
                    "Title not found in the company profile ladder. "
                    "Verify against reference/company-profile.md."))

    # Page-level: figures require a same-page source line with a completed year.
    if money_lines:
        valid_sources = [
            (n, s) for n, s in source_lines
            if YEAR_PATTERN.search(s) and "not guaranteed" in s.lower()
            and SOURCE_LINE_HINT.search(s)
        ]
        if not valid_sources:
            findings.append(Finding(
                "A6", "BLOCK", money_lines[0], "page-level",
                "Figures stated but no same-page source line found (small type citing "
                "a year and a named source, including 'not guaranteed')."))
        else:
            this_year = date.today().year
            for n, s in valid_sources:
                years = [int(y) for y in YEAR_PATTERN.findall(s)]
                if years and max(years) >= this_year:
                    findings.append(Finding(
                        "A6", "BLOCK", n, "source line year %d" % max(years),
                        "Source cites a year that is not a completed year. Averages "
                        "cite the most recently completed year."))

    findings.sort(key=lambda f: (f.line_no, f.rule))
    return findings


def exit_code_for(findings):
    if any(f.severity == "BLOCK" for f in findings):
        return 2
    if findings:
        return 1
    return 0


def run_check(draft, profile_path):
    try:
        profile = load_profile(profile_path)
    except ProfileGateError as exc:
        print("PROFILE GATE: %s" % exc)
        return 3
    term_rules = load_term_rules()
    findings = scan(draft, profile, term_rules)
    print("check.py: %s (profile: %s)" % (draft, profile_path))
    for f in findings:
        print(f.render())
    blocks = sum(1 for f in findings if f.severity == "BLOCK")
    flags = len(findings) - blocks
    code = exit_code_for(findings)
    print("Summary: %d BLOCK, %d FLAG. Exit %d." % (blocks, flags, code))
    if code == 2:
        print("VERDICT CONSTRAINT: BLOCK present. No CLEAR verdict is allowed.")
    return code


def selftest():
    failures = []
    term_rules = load_term_rules()
    if len(term_rules) < 15:
        failures.append("term bank parsed only %d rules; parser or file broken"
                        % len(term_rules))

    # Gate test: an incomplete profile (the blank template) must refuse.
    template = ROOT / "reference" / "company-profile.template.md"
    try:
        load_profile(template)
        failures.append("profile gate FAILED to trip on the blank template")
    except ProfileGateError:
        print("PASS profile gate trips on incomplete profile")

    profile = load_profile(DEFAULT_PROFILE)
    expected = json.loads(read_text(FIXTURES_DIR / "expected.json"))
    for name, expected_blocks in sorted(expected.items()):
        path = FIXTURES_DIR / "drafts" / name
        findings = scan(path, profile, term_rules)
        found_blocks = {f.rule for f in findings if f.severity == "BLOCK"}
        missing = set(expected_blocks) - found_blocks
        if missing:
            failures.append("%s: expected BLOCK rules not found: %s"
                            % (name, sorted(missing)))
        elif not expected_blocks and findings:
            failures.append("%s: expected clean but found: %s"
                            % (name, [f.render() for f in findings]))
        else:
            print("PASS %s (blocks found: %s)" % (name, sorted(found_blocks) or "none"))

    if failures:
        print("SELFTEST FAILED:")
        for f in failures:
            print("  - " + f)
        return 1
    print("SELFTEST PASSED: %d fixtures + profile gate." % len(expected))
    return 0


def main():
    ap = argparse.ArgumentParser(description="Recruiting-copy compliance gate")
    ap.add_argument("draft", nargs="?", help="draft file to check")
    ap.add_argument("--profile", default=str(DEFAULT_PROFILE),
                    help="company profile path (default: reference/company-profile.md)")
    ap.add_argument("--selftest", action="store_true",
                    help="run the checker against tools/fixtures/")
    args = ap.parse_args()

    if args.selftest:
        sys.exit(selftest())
    if not args.draft:
        ap.print_help()
        sys.exit(4)
    if not Path(args.draft).exists():
        print("draft not found: %s" % args.draft)
        sys.exit(4)
    sys.exit(run_check(args.draft, args.profile))


if __name__ == "__main__":
    main()
