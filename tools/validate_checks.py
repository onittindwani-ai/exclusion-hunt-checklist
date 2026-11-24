#!/usr/bin/env python3
"""Check that the kit really holds 28 well formed checks.

Run from the kit folder:  python3 tools/validate_checks.py
Prints OK and the count, or a list of problems (exit code 1).
Standard library only. No network.
"""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import checks_lib as lib  # noqa: E402

SOURCE_ROW = re.compile(r"^\| (\S+) \| ([AB]) \|")
DATE_OK = re.compile(r"^\d{4}-\d{2}-\d{2}$")

# Checks 1 to 3 are the three steps spoken in the Reel. Their meaning is pinned here.
SPOKEN = {
    1: ["broker", "writing", "generative"],
    2: ["everywhere", "uses ai"],
    3: ["person", "checks"],
}


def source_table(docs_dir):
    """Return {id: url} from docs/03-SOURCES.md."""
    path = pathlib.Path(docs_dir) / "03-SOURCES.md"
    out = {}
    if not path.exists():
        return out
    for line in path.read_text(encoding="utf-8").splitlines():
        if SOURCE_ROW.match(line):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) >= 8:
                out[cells[0]] = cells[7]
    return out


def validate(checks_dir=lib.CHECKS_DIR, docs_dir=lib.DOCS_DIR, expected=lib.EXPECTED_COUNT):
    problems = []
    files = lib.check_files(checks_dir)
    if len(files) != expected:
        problems.append("expected %d check files, found %d" % (expected, len(files)))
    sources = source_table(docs_dir)
    if not sources:
        problems.append("docs/03-SOURCES.md has no source rows")
    seen = []
    for path in files:
        name = path.name
        if not lib.valid_file_name(name):
            problems.append("%s: file name must look like 07-short-words.md" % name)
        chk = lib.parse_check(path)
        if chk.number is None:
            problems.append("%s: first line must be '# Check NN: title'" % name)
            continue
        seen.append(chk.number)
        if not name.startswith("%02d-" % chk.number):
            problems.append("%s: number in the file name and the heading differ" % name)
        if not chk.title:
            problems.append("%s: no title" % name)
        if not chk.group:
            problems.append("%s: no Group field" % name)
        if not chk.policy_types:
            problems.append("%s: no Policy types field" % name)
        for h in lib.REQUIRED_HEADINGS:
            if h not in chk.sections or not chk.sections[h].strip():
                problems.append("%s: missing or empty section '%s'" % (name, h))
        if not [p for p in chk.phrases if p.kind == "specific"]:
            problems.append("%s: needs at least one exact word or form number" % name)
        if not chk.sources:
            problems.append("%s: needs at least one source" % name)
        for s in chk.sources:
            for field in ("Title", "URL", "Date read", "Evidence", "Used here for"):
                if not s.get(field):
                    problems.append("%s: source %s has no %s" % (name, s.get("id"), field))
            if s.get("id") not in sources:
                problems.append("%s: source %s is not in docs/03-SOURCES.md" % (name, s.get("id")))
            elif s.get("URL") and sources[s["id"]] != s["URL"]:
                problems.append("%s: URL for source %s differs from docs/03-SOURCES.md" % (name, s.get("id")))
            if s.get("Date read") and not DATE_OK.match(s["Date read"]):
                problems.append("%s: date read must be YYYY-MM-DD" % name)
        prompt = chk.sections.get("Paste-in prompt", "")
        if "FOUND" not in prompt or "Never tell me whether I am covered" not in prompt:
            problems.append("%s: prompt must ask for FOUND / NOT FOUND / UNCLEAR and never give a coverage verdict" % name)
        if "[ ] Pass" not in chk.sections.get("Pass or needs work", ""):
            problems.append("%s: missing the Pass / Needs work field" % name)
        if not chk.sections.get("Ask your broker or carrier", "").strip().startswith(">"):
            problems.append("%s: the broker question must be a quoted line" % name)
        for d in lib.LONG_DASHES:
            if d in chk.text:
                problems.append("%s: contains a long dash character" % name)
    if seen != list(range(1, expected + 1)):
        problems.append("check numbers must run 1 to %d with no gaps, found %s" % (expected, seen))
    by_number = {}
    for path in files:
        c = lib.parse_check(path)
        if c.number is not None:
            by_number[c.number] = c
    for number, words in SPOKEN.items():
        c = by_number.get(number)
        if c is not None:
            low = c.title.lower()
            for w in words:
                if w not in low:
                    problems.append("check %02d title no longer matches the Reel (missing '%s')" % (number, w))
    readme = lib.ROOT / "README.md"
    if readme.exists() and str(expected) not in readme.read_text(encoding="utf-8"):
        problems.append("README.md does not mention the number %d" % expected)
    return problems, len(files)


def main(argv=None):
    problems, count = validate()
    if problems:
        print("PROBLEMS (%d):" % len(problems))
        for p in problems:
            print("  - " + p)
        return 1
    print("OK: %d checks, every field present, every source listed." % count)
    return 0


if __name__ == "__main__":
    sys.exit(main())
