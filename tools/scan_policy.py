#!/usr/bin/env python3
"""Scan a plain text policy for the exact words in the 28 checks.

Usage:
  python3 tools/scan_policy.py policy.txt
  python3 tools/scan_policy.py policy.txt --csv hits.csv
  python3 tools/scan_policy.py policy.txt --json

It reads the words from the check files, so the checks and the scanner always agree.
It runs on your own computer and sends nothing anywhere. Standard library only.

A hit is a place to read, not an answer. No hit does not mean the wording is absent
(scanned text can be wrong). This tool never says whether you are covered.
"""
import argparse
import csv
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import checks_lib as lib  # noqa: E402

FOOTER = ("A hit is a place to read, not an answer. No hit does not mean the wording is absent: "
          "scanned or copied text can be wrong. This tool never says whether you are covered. "
          "Ask your broker. This is not insurance or legal advice.")


def snippet_for(raw_lines, line_no, width=160):
    if 1 <= line_no <= len(raw_lines):
        text = " ".join(raw_lines[line_no - 1].split())
        return text[:width]
    return ""


def scan_text(text, checks=None):
    """Return a list of hit dicts, one per (check, phrase, place)."""
    if checks is None:
        checks = lib.load_checks()
    norm, lines, pages = lib.normalize_with_map(text)
    raw_for_snippet = text.split("\n")
    # collect unique phrases once
    unique = {}
    for c in checks:
        for p in c.phrases:
            key = (p.text.lower(), p.kind, p.common)
            unique.setdefault(key, {"phrase": p, "checks": []})["checks"].append(c)
    hits = []
    for key, info in unique.items():
        rx = lib.phrase_regex(info["phrase"].text)
        for m in rx.finditer(norm):
            start = m.start()
            line_no = lines[start]
            page_no = pages[start]
            snip = snippet_for(raw_for_snippet, line_no)
            for c in info["checks"]:
                hits.append({
                    "check": c.number,
                    "check_title": c.title,
                    "phrase": info["phrase"].text,
                    "kind": info["phrase"].kind,
                    "common": info["phrase"].common,
                    "line": line_no,
                    "page": page_no,
                    "snippet": snip,
                })
    hits.sort(key=lambda h: (h["line"], h["check"], h["phrase"]))
    return hits


def classify(h):
    if h["kind"] == "aid":
        return "aid"
    return "common" if h["common"] else "specific"


def summary_by_check(hits, checks=None):
    if checks is None:
        checks = lib.load_checks()
    rows = []
    for c in checks:
        mine = [h for h in hits if h["check"] == c.number]
        rows.append({
            "check": c.number,
            "title": c.title,
            "specific": sum(1 for h in mine if classify(h) == "specific"),
            "common": sum(1 for h in mine if classify(h) == "common"),
            "aid": sum(1 for h in mine if classify(h) == "aid"),
        })
    return rows


def format_report(hits, rows, has_pages):
    out = []
    spec = [h for h in hits if classify(h) == "specific"]
    out.append("SPECIFIC WORDS FOUND (read these first)")
    seen = set()
    for h in spec:
        key = (h["line"], h["phrase"].lower())
        if key in seen:
            continue
        seen.add(key)
        where = "line %d" % h["line"] + (", page %d" % h["page"] if has_pages else "")
        checks_for = sorted(set(x["check"] for x in spec if (x["line"], x["phrase"].lower()) == key))
        out.append("  %s: [%s] checks %s" % (where, h["phrase"], ", ".join(str(n) for n in checks_for)))
        out.append("      %s" % h["snippet"])
    if not seen:
        out.append("  none")
    com = [h for h in hits if classify(h) == "common"]
    out.append("")
    out.append("COMMON WORDING FOUND (ordinary wording, only meaningful next to AI words)")
    seen = set()
    for h in com:
        key = (h["line"], h["phrase"].lower())
        if key in seen:
            continue
        seen.add(key)
        where = "line %d" % h["line"] + (", page %d" % h["page"] if has_pages else "")
        out.append("  %s: [%s]" % (where, h["phrase"]))
    if not seen:
        out.append("  none")
    aid = [h for h in hits if classify(h) == "aid"]
    out.append("")
    out.append("SEARCH AID WORDS FOUND: %d place(s) (helpers only, not quotes from a form)" % len(set((h["line"], h["phrase"].lower()) for h in aid)))
    out.append("")
    out.append("PER CHECK (hits are places to read)")
    out.append("  check | specific | common | aid | title")
    for r in rows:
        out.append("  %02d    | %8d | %6d | %3d | %s" % (r["check"], r["specific"], r["common"], r["aid"], r["title"][:70]))
    out.append("")
    out.append(FOOTER)
    return "\n".join(out)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Scan a plain text policy for the words in the 28 checks.")
    ap.add_argument("policy", help="path to a plain text file of the policy")
    ap.add_argument("--csv", help="also write every hit to this CSV file")
    ap.add_argument("--json", action="store_true", help="print the hits as JSON instead of the report")
    args = ap.parse_args(argv)
    path = pathlib.Path(args.policy)
    if not path.is_file():
        print("File not found: %s" % args.policy, file=sys.stderr)
        return 2
    text = path.read_text(encoding="utf-8", errors="replace")
    if not text.strip():
        print("The file is empty. If your policy is a scanned PDF, the text cannot be read from it.", file=sys.stderr)
        return 2
    checks = lib.load_checks()
    hits = scan_text(text, checks)
    rows = summary_by_check(hits, checks)
    if args.csv:
        with open(args.csv, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["check", "check_title", "phrase", "kind", "common", "line", "page", "snippet"])
            for h in hits:
                w.writerow([h["check"], h["check_title"], h["phrase"], h["kind"], h["common"], h["line"], h["page"], h["snippet"]])
    if args.json:
        print(json.dumps({"hits": hits, "per_check": rows, "note": FOOTER}, indent=2))
    else:
        print(format_report(hits, rows, "\f" in text))
    return 0


if __name__ == "__main__":
    sys.exit(main())
