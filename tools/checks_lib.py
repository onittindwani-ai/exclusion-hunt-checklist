"""Shared reader for the Exclusion Hunt Checklist.

Standard library only. It reads the numbered files in checks/ and turns the
"Exact words to look for" lists into patterns the scanner can use. Both tools
use this one reader, so the checks and the scanner cannot drift apart.
"""
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
CHECKS_DIR = ROOT / "checks"
DOCS_DIR = ROOT / "docs"
EXPECTED_COUNT = 28

REQUIRED_HEADINGS = [
    "Exact words to look for",
    "Where it hides in a policy",
    "Why it matters",
    "Source",
    "What you do",
    "Ask your broker or carrier",
    "Paste-in prompt",
    "Pass or needs work",
]

# Dash characters that must never appear in this kit (written as escapes on purpose).
LONG_DASHES = ["\u2012", "\u2013", "\u2014", "\u2015", "\u2212"]

# Unicode hyphens and quotes that policy text from a PDF may contain.
_DASH_MAP = {c: "-" for c in ["\u2010", "\u2011", "\u2012", "\u2013", "\u2014", "\u2015", "\u2212"]}
_QUOTE_MAP = {"\u2018": "'", "\u2019": "'", "\u201c": '"', "\u201d": '"'}

_FORM_NUMBER = re.compile(r"^[A-Za-z]{2,3} \d{2} \d{2}$|^[A-Za-z]{2} \d{5}$")
_FILE_NAME = re.compile(r"^(\d{2})-[a-z0-9\-]+\.md$")


class Phrase(object):
    def __init__(self, text, kind, common=False):
        self.text = text
        self.kind = kind          # "specific" or "aid"
        self.common = common      # ordinary wording that proves nothing alone

    def __repr__(self):
        return "Phrase(%r, %r, common=%r)" % (self.text, self.kind, self.common)


class Check(object):
    def __init__(self, number, title, filename, group, policy_types, sections, phrases, sources, text):
        self.number = number
        self.title = title
        self.filename = filename
        self.group = group
        self.policy_types = policy_types
        self.sections = sections
        self.phrases = phrases
        self.sources = sources
        self.text = text


def _split_sections(text):
    sections = {}
    current = None
    buf = []
    for line in text.splitlines():
        if line.startswith("## "):
            if current is not None:
                sections[current] = "\n".join(buf).strip()
            current = line[3:].strip()
            buf = []
        else:
            buf.append(line)
    if current is not None:
        sections[current] = "\n".join(buf).strip()
    return sections


def _parse_phrases(block):
    phrases = []
    kind = "specific"
    for line in block.splitlines():
        stripped = line.strip()
        if stripped.lower().startswith("search aid words"):
            kind = "aid"
            continue
        m = re.match(r"^- `([^`]+)`(\s*\[common\])?\s*$", stripped)
        if m:
            phrases.append(Phrase(m.group(1), kind, bool(m.group(2))))
    return phrases


def _parse_sources(block):
    sources = []
    current = None
    for line in block.splitlines():
        m = re.match(r"^- Source ID:\s*(\S+)\s*$", line)
        if m:
            current = {"id": m.group(1)}
            sources.append(current)
            continue
        m = re.match(r"^\s+- (Title|URL|Date read|Evidence|Used here for):\s*(.*)$", line)
        if m and current is not None:
            current[m.group(1)] = m.group(2).strip()
    return sources


def _field(text, name):
    m = re.search(r"^- %s:\s*(.*)$" % re.escape(name), text, re.M)
    return m.group(1).strip() if m else ""


def parse_check(path):
    path = pathlib.Path(path)
    text = path.read_text(encoding="utf-8")
    title_m = re.match(r"^# Check (\d{2}): (.+)$", text.splitlines()[0] if text else "")
    number = int(title_m.group(1)) if title_m else None
    title = title_m.group(2).strip() if title_m else ""
    sections = _split_sections(text)
    phrases = _parse_phrases(sections.get("Exact words to look for", ""))
    sources = _parse_sources(sections.get("Source", ""))
    return Check(number, title, path.name, _field(text, "Group"), _field(text, "Policy types"),
                 sections, phrases, sources, text)


def check_files(checks_dir=CHECKS_DIR):
    files = []
    for p in sorted(pathlib.Path(checks_dir).glob("*.md")):
        if p.name.startswith("00-"):
            continue
        files.append(p)
    return files


def load_checks(checks_dir=CHECKS_DIR):
    return [parse_check(p) for p in check_files(checks_dir)]


def valid_file_name(name):
    return bool(_FILE_NAME.match(name))


# ---------------------------------------------------------------- text normalizing

def normalize_with_map(text):
    """Return (normalized, lines, pages).

    normalized is lower case, whitespace is one space, a hyphen that ends a line is
    joined to the next word (machine-<newline>based becomes machine-based), curly
    quotes and long dashes become plain ones. lines[i] and pages[i] give the 1 based
    line and page (form feeds start a new page) of normalized[i].
    """
    out = []
    lines = []
    pages = []
    line = 1
    page = 1
    i = 0
    n = len(text)
    pending_space = False
    while i < n:
        ch = text[i]
        if ch == "\f":
            page += 1
            pending_space = True
            i += 1
            continue
        if ch == "\n":
            line += 1
            pending_space = True
            i += 1
            continue
        if ch.isspace():
            pending_space = True
            i += 1
            continue
        ch = _DASH_MAP.get(ch, ch)
        ch = _QUOTE_MAP.get(ch, ch)
        if pending_space and out:
            out.append(" ")
            lines.append(line)
            pages.append(page)
        pending_space = False
        out.append(ch.lower())
        lines.append(line)
        pages.append(page)
        if ch == "-":
            # a hyphen at the end of a line: join to the next word
            j = i + 1
            while j < n and text[j] in " \t\r":
                j += 1
            if j < n and text[j] == "\n":
                k = j
                new_lines = 0
                while k < n and text[k].isspace():
                    if text[k] == "\n":
                        new_lines += 1
                    k += 1
                if k < n and text[k].isalpha() and new_lines == 1:
                    line += new_lines
                    i = k
                    continue
        i += 1
    return "".join(out), lines, pages


def phrase_regex(text):
    """Build a regular expression for one phrase from a check file."""
    norm = text.strip()
    tokens = norm.lower().split()
    if _FORM_NUMBER.match(norm):
        body = r"\s*".join(re.escape(t) for t in tokens)
        return re.compile(r"(?<![a-z0-9])" + body + r"(?!\d)")
    body = r"\s+".join(re.escape(t) for t in tokens)
    return re.compile(r"(?<![a-z0-9])" + body + r"(?![a-z0-9])")
