#!/usr/bin/env python3
"""Render a reviewed draft as a marked-up document for the writer.

Usage: python tools/render.py <draft.md> <review.md> [out.html]

Reads a draft and the review that critiqued it, anchors the review's
findings to the draft lines they cite, and writes one self-contained HTML
file: the submitted copy shown as a readable document, editorial notes in
the margin on wide screens (note-cards under the offending line on narrow
screens), a verdict banner up top, and a whole-document block for findings
that carry no line anchor. Anchors are never invented: a finding without a
parseable line reference, or one citing a line that does not render, goes
to the whole-document block.

Excluded on purpose: the verbatim check.py output, the runtime-mode line,
log-entry mechanics, and checklist internals. The audience is the writer.

Stdlib only. Default output path: markup/<review-stem>.html.
"""

import html
import os
import re
import sys

# ---------------------------------------------------------------- helpers

def esc(text):
    return html.escape(text)


def norm_quotes(text):
    return text.replace("“", '"').replace("”", '"')


def inline_md(text):
    """Escape, then render the inline markdown the reviews actually use."""
    s = esc(text)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<![\w*])\*([^*\s][^*]*?)\*(?![\w*])", r"<em>\1</em>", s)
    return s


def mark_quotes(text, quotes):
    """Escape draft text, wrapping any cited fragment found in it in <mark>."""
    hits = []
    for q in quotes:
        for candidate in (q, q.rstrip(".")):
            if candidate and candidate in text:
                hits.append(candidate)
                break
    if not hits:
        return esc(text)
    hits = sorted(set(hits), key=len, reverse=True)
    pattern = re.compile("|".join(re.escape(h) for h in hits))
    out, pos = [], 0
    for m in pattern.finditer(text):
        out.append(esc(text[pos:m.start()]))
        out.append("<mark>" + esc(m.group(0)) + "</mark>")
        pos = m.end()
    out.append(esc(text[pos:]))
    return "".join(out)


# ---------------------------------------------------------- draft parsing

def is_separator_row(cells):
    return all(re.fullmatch(r":?-{2,}:?", c) for c in cells) if cells else False


def row_cells(raw):
    return [c.strip() for c in raw.strip().strip("|").split("|")]


def parse_draft(text):
    """Split the draft into blocks, each carrying its 1-indexed source lines."""
    lines = text.splitlines()
    blocks, i, n = [], 0, len(lines)
    while i < n:
        stripped = lines[i].strip()
        if not stripped:
            i += 1
            continue
        if stripped.startswith("|"):
            rows = []
            while i < n and lines[i].strip().startswith("|"):
                rows.append((i + 1, lines[i].strip()))
                i += 1
            blocks.append({"kind": "table", "rows": rows})
            continue
        m = re.match(r"^(#{1,6})\s+(.*)$", stripped)
        if m:
            blocks.append({"kind": "heading", "level": len(m.group(1)),
                           "line": i + 1, "text": m.group(2)})
        else:
            blocks.append({"kind": "para", "line": i + 1, "text": stripped})
        i += 1
    return blocks


def renderable_lines(blocks):
    """Line numbers a note can legitimately anchor to."""
    lines = set()
    for b in blocks:
        if b["kind"] == "table":
            for ln, raw in b["rows"]:
                if not is_separator_row(row_cells(raw)):
                    lines.add(ln)
        else:
            lines.add(b["line"])
    return lines


# --------------------------------------------------------- review parsing

RULE_ID_RE = re.compile(r"\b[ABC]\d{1,2}(?:-adjacent)?\b|\b[ABC](?=[\s,:.])")


def make_note(bullet, section):
    m = re.match(r"^\*\*(.+?)\*\*\s*(.*)$", bullet, re.S)
    if m:
        header, body = m.group(1).strip(), m.group(2).strip()
    else:
        header, body = "", bullet.strip()
    header_n = norm_quotes(header)
    qm = re.search(r'"(.+?)"', header_n)
    quote = qm.group(1).strip() if qm else ""
    hdr = re.sub(r'".*?"', "", header_n)
    lm = re.search(r"\blines?\s+(\d+)\b", hdr, re.I)
    line = int(lm.group(1)) if lm else None
    ids = []
    for rid in RULE_ID_RE.findall(hdr):
        if rid not in ids:
            ids.append(rid)
    title = hdr
    title = re.sub(r"\blines?\s+\d+\b", "", title, flags=re.I)
    for rid in ids:
        title = title.replace(rid, "", 1)
    title = re.sub(r"\b(page level|whole document)\b", "", title, flags=re.I)
    title = re.sub(r"\s*/\s*", "", title)
    title = title.strip(" ,:;./").strip()
    return {"ids": ids, "title": title, "line": line, "quote": quote,
            "body": body, "section": section}


def clean_section(name):
    name = re.sub(r"^Family \d+:\s*", "", name)
    name = re.sub(r"\s*\(.*?\)\s*$", "", name)
    return name.strip()


def parse_review(text):
    meta, verdict, notes, forms = {}, None, [], []
    h2, h3, bullet, bullet_section = "", "", None, ""

    def flush():
        nonlocal bullet
        if bullet is not None:
            notes.append(make_note(bullet, bullet_section))
            bullet = None

    for raw in text.splitlines():
        line = raw.rstrip()
        m2 = re.match(r"^##\s+(.*)$", line)
        m3 = re.match(r"^###\s+(.*)$", line)
        if m2:
            flush()
            h2, h3 = m2.group(1).strip(), ""
            vm = re.match(r"^Verdict:\s*(.+)$", h2, re.I)
            if vm:
                verdict = vm.group(1).strip()
            continue
        if m3:
            flush()
            h3 = m3.group(1).strip()
            continue
        if re.match(r"^#\s", line):
            flush()
            continue
        if not h2:
            mm = re.match(r"^-\s*([A-Za-z ]+?):\s*(.+)$", line)
            if mm:
                meta[mm.group(1).strip().lower()] = mm.group(2).strip()
            continue
        h2l = h2.lower()
        if h2l.startswith("where the compliant forms"):
            if line.strip():
                forms.append(line.strip())
            continue
        if h2l.startswith("findings") or h2l.startswith("conditions"):
            bm = re.match(r"^(?:-|\d+\.)\s+(.*)$", line)
            if bm:
                flush()
                bullet = bm.group(1)
                bullet_section = clean_section(h3 or h2)
            elif bullet is not None and line.strip():
                bullet += " " + line.strip()
            elif not line.strip():
                flush()
    flush()
    return meta, verdict, notes, forms


# ------------------------------------------------------------------- html

CSS = """
:root {
  --paper: #fffdf7; --ink: #23211b; --faint: #6b675e; --hairline: #e4dfd1;
  --wash: #fdf3d6; --mark: #ffe9a4; --note-accent: #8a2b2b; --margin-w: 19rem;
}
* { box-sizing: border-box; }
body {
  margin: 0; background: #eeeae1; color: var(--ink);
  font: 16px/1.55 Georgia, "Iowan Old Style", "Times New Roman", serif;
}
.page { max-width: 74rem; margin: 2.25rem auto 0; padding: 0 1.25rem; }
.masthead {
  display: flex; justify-content: space-between; align-items: baseline;
  gap: .75rem 1.5rem; flex-wrap: wrap;
  border-bottom: 3px double #b3ab99; padding-bottom: .7rem; margin-bottom: 1.25rem;
}
.brand { font-variant: small-caps; letter-spacing: .3em; white-space: nowrap; }
.brand .k { font-size: 1.45rem; font-weight: 700; margin-right: .7rem; }
.brand .sub { font-size: .95rem; color: var(--faint); }
.chips { display: flex; gap: .45rem; flex-wrap: wrap; }
.chip {
  display: inline-block; border: 1px solid #cdc5b2; border-radius: 999px;
  background: #faf7ee; padding: .1rem .6rem; font-size: .72rem; color: #56524a;
  font-family: ui-monospace, Menlo, Consolas, monospace; white-space: nowrap;
}
.chip.rule { background: #3a352d; border-color: #3a352d; color: #f3efe4; }
.banner { border-radius: 6px; color: #fff; padding: .95rem 1.25rem; margin-bottom: 1.5rem; }
.banner .verdict { font-size: 1.4rem; font-weight: 700; letter-spacing: .14em; }
.banner .subtitle { opacity: .93; font-size: .95rem; margin-top: .2rem; }
.v-blocked { background: #6e1a1a; }
.v-revise { background: #9c5e07; }
.v-clear { background: #1d6a38; }
.v-other { background: #4b5563; }
.paper {
  background: var(--paper); border: 1px solid var(--hairline);
  box-shadow: 0 1px 4px rgba(0, 0, 0, .14); padding: 3rem 3.25rem;
}
.row { display: grid; grid-template-columns: minmax(0, 1fr) var(--margin-w); column-gap: 2.25rem; }
.paper.no-anchors .row { grid-template-columns: minmax(0, 1fr); }
.copy { min-width: 0; }
.copy h1 { font-size: 1.7rem; line-height: 1.25; margin: .2rem 0 .9rem; }
.copy h2 { font-size: 1.35rem; margin: .4rem 0 .7rem; }
.copy h3, .copy h4, .copy h5, .copy h6 { font-size: 1.1rem; margin: .4rem 0 .6rem; }
.copy p { margin: .55rem 0; }
.copy .hit { background: var(--wash); }
mark { background: var(--mark); padding: 0 .12em; }
sup.m {
  font-family: ui-monospace, Menlo, Consolas, monospace; font-size: .62em;
  font-weight: 700; color: var(--note-accent); margin-left: .18em;
}
table { border-collapse: collapse; width: 100%; margin: .8rem 0; }
th, td { border: 1px solid var(--hairline); padding: .42rem .7rem; text-align: left; }
th { background: #f5f1e4; font-variant: small-caps; letter-spacing: .05em; }
tr.hit th, tr.hit td { background: var(--wash); }
.margin { font-size: .78rem; line-height: 1.5; color: #3e3b33; padding-top: .35rem; }
.mnote { border-left: 2px solid #b3ab99; padding: .05rem 0 .1rem .7rem; margin: 0 0 .95rem; }
.mnote .mhead { margin-bottom: .15rem; }
.mnote .num {
  font-family: ui-monospace, Menlo, Consolas, monospace; font-weight: 700;
  color: var(--note-accent); margin-right: .4rem;
}
.mnote .ntitle { font-weight: 700; margin-top: .25rem; }
.mnote blockquote { margin: .25rem 0 0; font-style: italic; color: #6a3030; }
.mnote .nbody { margin: .25rem 0 0; }
.mnote .ntag { font-size: .68rem; font-style: italic; color: #8f8a7c; margin-top: .3rem; }
.noterow { display: none; }
.noterow td { background: #fbf6e8; }
.wholedoc, .forms { margin-top: 1.9rem; }
.wholedoc h2, .forms h2 {
  font-variant: small-caps; letter-spacing: .16em; font-size: 1rem; font-weight: 700;
  border-bottom: 1px solid #b3ab99; padding-bottom: .3rem; margin: 0 0 .9rem;
}
.notegrid { display: grid; grid-template-columns: repeat(auto-fill, minmax(21rem, 1fr)); gap: .9rem; }
.card {
  background: var(--paper); border: 1px solid var(--hairline);
  border-left: 3px solid #b3ab99; padding: .65rem .8rem;
  font-size: .82rem; line-height: 1.5;
}
.card .ntitle { font-weight: 700; margin-top: .3rem; }
.card blockquote { margin: .3rem 0 0; font-style: italic; color: #6a3030; }
.card .nbody { margin: .3rem 0 0; }
.card .ntag { font-size: .68rem; font-style: italic; color: #8f8a7c; margin-top: .35rem; }
.forms p { font-size: .88rem; margin: .4rem 0; }
@media (max-width: 900px) {
  .page { margin-top: 1.25rem; }
  .paper { padding: 1.4rem 1.1rem; }
  .row { grid-template-columns: minmax(0, 1fr); }
  .margin { padding: 0; }
  .mnote {
    background: #fbf6e8; border: 1px solid #ded6c0;
    border-left: 3px solid var(--note-accent);
    padding: .5rem .7rem; margin: .35rem 0 .85rem;
  }
  .row.tablerow .margin { display: none; }
  .noterow { display: table-row; }
}
@media print {
  body { background: #fff; font-size: 12px; }
  .page { margin: 0; max-width: none; padding: 0; }
  .paper { box-shadow: none; padding: 1.5rem; }
  .paper:not(.no-anchors) .row { grid-template-columns: minmax(0, 1fr) 15rem; }
  .margin { display: block; padding-top: .35rem; }
  .mnote {
    background: none; border: none; border-left: 2px solid #b3ab99;
    padding: .05rem 0 .1rem .7rem; margin: 0 0 .95rem;
  }
  .row.tablerow .margin { display: block; }
  .noterow { display: none; }
  .banner, .chip, th, tr.hit th, tr.hit td, mark, .copy .hit {
    -webkit-print-color-adjust: exact; print-color-adjust: exact;
  }
}
"""

SUBTITLES = {
    "BLOCKED": "This copy cannot run as written. Fix the noted lines and resubmit.",
    "REVISE AND RESUBMIT": "Not cleared yet. The notes below need your attention before resubmission.",
    "CLEAR": "No blocking findings. Remaining notes are advisory, and the call is yours.",
}

VERDICT_CLASSES = {
    "BLOCKED": "v-blocked",
    "REVISE AND RESUBMIT": "v-revise",
    "CLEAR": "v-clear",
}

REFUSAL = ("This desk critiques. It does not rewrite. "
           "The wording is yours; this record is mine.")


def note_body_html(note, with_tag=True):
    parts = []
    if note["title"]:
        parts.append('<div class="ntitle">%s</div>' % inline_md(note["title"]))
    if note["quote"]:
        parts.append("<blockquote>“%s”</blockquote>" % esc(note["quote"]))
    if note["body"]:
        parts.append('<p class="nbody">%s</p>' % inline_md(note["body"]))
    if with_tag and note["section"]:
        parts.append('<div class="ntag">%s</div>' % esc(note["section"]))
    return "".join(parts)


def note_chips(note, num=None, show_line=True):
    parts = []
    if num is not None:
        parts.append('<span class="num">%d</span>' % num)
    label = " / ".join(note["ids"]) if note["ids"] else "Note"
    parts.append('<span class="chip rule">%s</span>' % esc(label))
    if show_line and note["line"]:
        parts.append('<span class="chip">line %d</span>' % note["line"])
    return '<div class="mhead">%s</div>' % " ".join(parts)


def margin_note_html(note, num):
    return '<div class="mnote">%s%s</div>' % (
        note_chips(note, num), note_body_html(note))


def card_note_html(note):
    return '<div class="card">%s%s</div>' % (
        note_chips(note, show_line=False), note_body_html(note))


def markers_html(nums):
    if not nums:
        return ""
    return '<sup class="m">%s</sup>' % ", ".join(str(n) for n in nums)


def render_blocks(blocks, notes_by_line):
    """Render draft blocks; return (html, saw_anchor)."""
    out = []
    counter = [0]

    def take(line_no):
        attached = notes_by_line.get(line_no, [])
        numbered = []
        for note in attached:
            counter[0] += 1
            numbered.append((counter[0], note))
        return numbered

    for block in blocks:
        if block["kind"] == "table":
            table_notes = []
            body_rows = []
            all_rows = [(ln, row_cells(raw)) for ln, raw in block["rows"]]
            header_first = len(all_rows) > 1 and is_separator_row(all_rows[1][1])
            width = max(len(c) for _, c in all_rows)
            for idx, (ln, cells) in enumerate(all_rows):
                if is_separator_row(cells):
                    continue
                numbered = take(ln)
                quotes = [n["quote"] for _, n in numbered if n["quote"]]
                tag = "th" if (header_first and idx == 0) else "td"
                rendered = []
                for cell in cells:
                    cell_html = mark_quotes(cell, [q for q in quotes
                                                  if q.rstrip(".") in cell])
                    rendered.append("<%s>%s</%s>" % (tag, cell_html, tag))
                if numbered:
                    first = rendered[0]
                    close = "</%s>" % tag
                    rendered[0] = first[:-len(close)] + \
                        markers_html([n for n, _ in numbered]) + close
                cls = ' class="hit"' if numbered else ""
                body_rows.append("<tr%s>%s</tr>" % (cls, "".join(rendered)))
                for num, note in numbered:
                    table_notes.append((num, note))
                    body_rows.append(
                        '<tr class="noterow"><td colspan="%d">'
                        '<div class="mnote">%s%s</div></td></tr>'
                        % (width, note_chips(note, num), note_body_html(note)))
            margin = "".join(margin_note_html(n, num) for num, n in table_notes)
            out.append(
                '<div class="row tablerow"><div class="copy"><table>%s</table>'
                '</div><aside class="margin">%s</aside></div>'
                % ("".join(body_rows), margin))
        else:
            numbered = take(block["line"])
            quotes = [n["quote"] for _, n in numbered if n["quote"]]
            text_html = mark_quotes(block["text"], quotes)
            text_html += markers_html([n for n, _ in numbered])
            hit = ' class="hit"' if numbered else ""
            if block["kind"] == "heading":
                level = min(block["level"], 6)
                copy = "<h%d%s>%s</h%d>" % (level, hit, text_html, level)
            else:
                copy = "<p%s>%s</p>" % (hit, text_html)
            margin = "".join(margin_note_html(n, num) for num, n in numbered)
            out.append(
                '<div class="row"><div class="copy">%s</div>'
                '<aside class="margin">%s</aside></div>' % (copy, margin))
    return "".join(out), counter[0] > 0


def build_html(draft_name, blocks, meta, verdict, notes, forms):
    verdict_key = (verdict or "").upper().strip()
    banner_class = VERDICT_CLASSES.get(verdict_key, "v-other")
    subtitle = SUBTITLES.get(verdict_key, "See the notes below.")

    anchorable = renderable_lines(blocks)
    notes_by_line, page_notes = {}, []
    for note in notes:
        if note["line"] and note["line"] in anchorable:
            notes_by_line.setdefault(note["line"], []).append(note)
        else:
            page_notes.append(note)

    body_html, saw_anchor = render_blocks(blocks, notes_by_line)
    paper_class = "paper" if saw_anchor else "paper no-anchors"

    chips = []
    if meta.get("date"):
        chips.append("Reviewed %s" % meta["date"])
    asset = meta.get("asset type", "")
    am = re.match(r"^([^(]+?)\s*\(", asset)
    if am:
        asset = am.group(1)
    if asset:
        chips.append(asset)
    chips.append(draft_name)
    if meta.get("resubmission of"):
        chips.append("Resubmission")
    chips_html = "".join('<span class="chip">%s</span>' % esc(c) for c in chips)

    parts = []
    parts.append("<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n"
                 "<meta charset=\"utf-8\">\n"
                 "<meta name=\"viewport\" content=\"width=device-width, "
                 "initial-scale=1\">\n"
                 "<title>Marked-up copy: %s</title>\n"
                 "<style>%s</style>\n</head>\n<body>\n" % (esc(draft_name), CSS))
    parts.append('<div class="page">')
    parts.append(
        '<header class="masthead"><div class="brand">'
        '<span class="k">Kompliant</span><span class="sub">Review Desk</span>'
        '</div><div class="chips">%s</div></header>' % chips_html)
    parts.append(
        '<section class="banner %s"><div class="verdict">%s</div>'
        '<div class="subtitle">%s</div></section>'
        % (banner_class, esc(verdict_key or "NO VERDICT FOUND"), esc(subtitle)))
    parts.append('<article class="%s">%s</article>' % (paper_class, body_html))
    if page_notes:
        cards = "".join(card_note_html(n) for n in page_notes)
        parts.append(
            '<section class="wholedoc"><h2>Whole-document notes</h2>'
            '<div class="notegrid">%s</div></section>' % cards)
    forms = [p for p in forms if p != REFUSAL]
    if forms:
        paragraphs = "".join("<p>%s</p>" % inline_md(p) for p in forms)
        parts.append(
            '<section class="forms"><h2>Where the compliant forms live</h2>'
            '%s</section>' % paragraphs)
    parts.append("</div>\n</body>\n</html>\n")
    return "".join(parts)


# ------------------------------------------------------------------- main

def main(argv):
    if len(argv) < 3 or len(argv) > 4:
        print(__doc__.strip().splitlines()[2].strip(), file=sys.stderr)
        return 64
    draft_path, review_path = argv[1], argv[2]
    for path in (draft_path, review_path):
        if not os.path.isfile(path):
            print("render.py: not a file: %s" % path, file=sys.stderr)
            return 66
    with open(draft_path, encoding="utf-8") as f:
        draft_text = f.read()
    with open(review_path, encoding="utf-8") as f:
        review_text = f.read()

    blocks = parse_draft(draft_text)
    meta, verdict, notes, forms = parse_review(review_text)
    anchorable = renderable_lines(blocks)

    if len(argv) == 4:
        out_path = argv[3]
    else:
        stem = os.path.splitext(os.path.basename(review_path))[0]
        out_path = os.path.join("markup", stem + ".html")
    out_dir = os.path.dirname(out_path)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    draft_name = os.path.basename(draft_path)
    page = build_html(draft_name, blocks, meta, verdict, notes, forms)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(page)

    anchored = sum(1 for n in notes if n["line"] and n["line"] in anchorable)
    print("render.py: wrote %s (%s, %d notes: %d line-anchored, %d whole-document)"
          % (out_path, verdict or "no verdict", len(notes),
             anchored, len(notes) - anchored))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
