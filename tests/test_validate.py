import tempfile
import pathlib
import shutil
import unittest

import _paths  # noqa: F401
import checks_lib as lib
import validate_checks as vc


class RealKit(unittest.TestCase):
    def test_exactly_28_checks_and_no_problems(self):
        problems, count = vc.validate()
        self.assertEqual(problems, [])
        self.assertEqual(count, 28)

    def test_numbers_run_one_to_28(self):
        numbers = [c.number for c in lib.load_checks()]
        self.assertEqual(numbers, list(range(1, 29)))

    def test_every_check_has_specific_words_a_source_and_a_question(self):
        for c in lib.load_checks():
            self.assertTrue([p for p in c.phrases if p.kind == "specific"], c.filename)
            self.assertTrue(c.sources, c.filename)
            self.assertTrue(c.sections["Ask your broker or carrier"].startswith(">"), c.filename)
            self.assertIn("[ ] Pass", c.sections["Pass or needs work"], c.filename)

    def test_first_three_checks_match_the_reel(self):
        by = {c.number: c.title.lower() for c in lib.load_checks()}
        self.assertIn("broker in writing", by[1])
        self.assertIn("generative ai exclusion", by[1])
        self.assertIn("cyber and professional", by[1])
        self.assertIn("everywhere your business uses ai", by[2])
        self.assertIn("a person checks", by[3])

    def test_prompts_never_allow_a_coverage_verdict(self):
        for c in lib.load_checks():
            prompt = c.sections["Paste-in prompt"]
            self.assertIn("FOUND, NOT FOUND or UNCLEAR", prompt)
            self.assertIn("Never tell me whether I am covered", prompt)

    def test_every_source_id_resolves_and_urls_match(self):
        table = vc.source_table(lib.DOCS_DIR)
        for c in lib.load_checks():
            for s in c.sources:
                self.assertIn(s["id"], table)
                self.assertEqual(table[s["id"]], s["URL"])


class BrokenCopies(unittest.TestCase):
    def setUp(self):
        self.tmp = pathlib.Path(tempfile.mkdtemp())
        self.checks = self.tmp / "checks"
        shutil.copytree(lib.CHECKS_DIR, self.checks)

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def test_removing_a_check_is_caught(self):
        victim = sorted(self.checks.glob("28-*.md"))[0]
        victim.unlink()
        problems, count = vc.validate(self.checks, lib.DOCS_DIR)
        self.assertEqual(count, 27)
        self.assertTrue(any("expected 28" in p for p in problems))

    def test_missing_section_is_caught(self):
        f = sorted(self.checks.glob("07-*.md"))[0]
        f.write_text(f.read_text().replace("## Why it matters", "## Something else"))
        problems, _ = vc.validate(self.checks, lib.DOCS_DIR)
        self.assertTrue(any("Why it matters" in p for p in problems))

    def test_unknown_source_is_caught(self):
        f = sorted(self.checks.glob("09-*.md"))[0]
        f.write_text(f.read_text().replace("Source ID: L1", "Source ID: ZZ9", 1))
        problems, _ = vc.validate(self.checks, lib.DOCS_DIR)
        self.assertTrue(any("ZZ9" in p for p in problems))

    def test_a_long_dash_is_caught(self):
        f = sorted(self.checks.glob("10-*.md"))[0]
        f.write_text(f.read_text() + "\nbad " + chr(0x2014) + " dash\n")
        problems, _ = vc.validate(self.checks, lib.DOCS_DIR)
        self.assertTrue(any("long dash" in p for p in problems))


if __name__ == "__main__":
    unittest.main()
