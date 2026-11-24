"""Whole repo checks: no long dashes, no private links, only the one allowed GitHub link."""
import pathlib
import re
import unittest

import _paths
import checks_lib as lib

ROOT = _paths.ROOT
ALLOWED_GITHUB = "https://github.com/onittindwani-ai/exclusion-hunt-checklist"
SKIP_DIRS = {".git", "__pycache__"}
TEXT_SUFFIXES = {".md", ".txt", ".csv", ".py", ".json", ".yml", ".yaml", ""}


def repo_text_files():
    for p in sorted(ROOT.rglob("*")):
        if not p.is_file():
            continue
        if any(part in SKIP_DIRS for part in p.relative_to(ROOT).parts):
            continue
        if p.name == "test_hygiene.py":
            continue  # this file names the forbidden strings it searches for
        if p.suffix in TEXT_SUFFIXES or p.name in {"LICENSE"}:
            yield p


class Hygiene(unittest.TestCase):
    def test_there_are_files(self):
        self.assertGreater(len(list(repo_text_files())), 50)

    def test_no_long_dashes_anywhere(self):
        for p in repo_text_files():
            text = p.read_text(encoding="utf-8")
            for d in lib.LONG_DASHES:
                self.assertNotIn(d, text, str(p.relative_to(ROOT)))

    def test_no_private_links_paths_or_emails(self):
        forbidden = ["drive." + "google", "docs." + "google", "notion." + "so", "notion." + "site", "/Users" + "/", "file:" + "//", "dropbox." + "com"]
        email = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+\.[A-Za-z]{2,}")
        for p in repo_text_files():
            text = p.read_text(encoding="utf-8")
            rel = str(p.relative_to(ROOT))
            for f in forbidden:
                self.assertNotIn(f, text, "%s contains %s" % (rel, f))
            self.assertIsNone(email.search(text), "%s contains an email address" % rel)

    def test_only_the_allowed_github_link(self):
        rx = re.compile(r"https?://(?:www\.)?github\.com[^\s)>\]\"'`]*")
        for p in repo_text_files():
            for m in rx.finditer(p.read_text(encoding="utf-8")):
                self.assertEqual(m.group(0), ALLOWED_GITHUB, str(p.relative_to(ROOT)))

    def test_license_names_the_owner(self):
        text = (ROOT / "LICENSE").read_text()
        self.assertIn("MIT License", text)
        self.assertIn("Onit Tindwani", text)

    def test_not_advice_note_is_in_the_readme_and_every_check_index(self):
        self.assertIn("not insurance or legal advice", (ROOT / "README.md").read_text().lower())
        self.assertIn("not insurance or legal advice", (ROOT / "checks" / "00-INDEX.md").read_text().lower())

    def test_no_ai_author_credit(self):
        for p in repo_text_files():
            low = p.read_text(encoding="utf-8").lower()
            self.assertNotIn("co-authored", low, str(p))
            self.assertNotIn("generated with", low, str(p))


if __name__ == "__main__":
    unittest.main()
