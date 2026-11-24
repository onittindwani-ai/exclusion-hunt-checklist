import json
import unittest

import _paths
import checks_lib as lib
import scan_policy as sp

FAKE = (_paths.FIXTURES / "synthetic_policy.txt").read_text()
CLEAN = (_paths.FIXTURES / "clean_policy.txt").read_text()


def find(hits, phrase, kind=None):
    return [h for h in hits if h["phrase"].lower() == phrase.lower() and (kind is None or sp.classify(h) == kind)]


class KnownHits(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.hits = sp.scan_text(FAKE)

    def test_form_number_with_odd_spacing_is_found_on_line_7(self):
        h = find(self.hits, "CG 40 47")
        self.assertTrue(h)
        self.assertEqual({(x["line"], x["page"]) for x in h}, {(7, 1)})

    def test_form_number_without_edition_is_found_on_line_8(self):
        h = find(self.hits, "CG 40 48")
        self.assertEqual({(x["line"], x["page"]) for x in h}, {(8, 1)})

    def test_phrase_split_across_lines_reports_its_first_line(self):
        h = find(self.hits, "generative artificial intelligence")
        self.assertIn((13, 2), {(x["line"], x["page"]) for x in h})

    def test_hyphen_at_line_end_is_joined(self):
        h = find(self.hits, "machine-based learning system or model")
        self.assertEqual({(x["line"], x["page"]) for x in h}, {(14, 2)})

    def test_reported_absolute_wording_is_found_on_page_3(self):
        h = find(self.hits, "any actual or alleged use, deployment, or development of artificial intelligence")
        self.assertEqual({(x["line"], x["page"]) for x in h}, {(19, 3)})
        h = find(self.hits, "based upon, arising out of, or attributable to")
        self.assertEqual({(x["line"], x["page"]) for x in h}, {(18, 3)})
        h = find(self.hits, "in any way involving")
        self.assertEqual({(x["line"], x["page"]) for x in h}, {(20, 3)})

    def test_capital_letters_do_not_matter(self):
        self.assertTrue(find(self.hits, "artificial intelligence", "specific"))

    def test_common_wording_is_kept_apart(self):
        self.assertTrue(find(self.hits, "arising out of", "common"))
        self.assertFalse(find(self.hits, "arising out of", "specific"))

    def test_no_hit_for_a_form_that_is_not_in_the_text(self):
        self.assertFalse(find(self.hits, "CG 35 08"))

    def test_word_boundaries_hold(self):
        text = "The bakery maintains its ovens. Training day."
        hits = sp.scan_text(text)
        self.assertFalse([h for h in hits if h["phrase"].lower() == "ai"])


class NegativeControl(unittest.TestCase):
    def test_clean_policy_has_zero_specific_hits(self):
        hits = sp.scan_text(CLEAN)
        self.assertEqual([h for h in hits if sp.classify(h) == "specific"], [])
        self.assertEqual([h for h in hits if sp.classify(h) == "aid"], [])

    def test_clean_policy_report_says_none_and_gives_no_verdict(self):
        hits = sp.scan_text(CLEAN)
        report = sp.format_report(hits, sp.summary_by_check(hits), False)
        self.assertIn("none", report)
        self.assertIn("never says whether you are covered", report.lower())
        # the per check table repeats the check titles, so look only at the findings and the footer
        findings = report.split("PER CHECK")[0]
        footer = report.split("PER CHECK")[1].split("\n\n")[-1].lower()
        for text in (findings.lower(), footer.replace("whether you are covered", "")):
            self.assertNotIn("you are covered", text)
            self.assertNotIn("not covered", text)


class Tool(unittest.TestCase):
    def test_every_check_has_a_row(self):
        hits = sp.scan_text(FAKE)
        rows = sp.summary_by_check(hits)
        self.assertEqual([r["check"] for r in rows], list(range(1, 29)))

    def test_csv_and_json_outputs(self):
        import tempfile, csv, io, contextlib, os
        d = tempfile.mkdtemp()
        out = os.path.join(d, "hits.csv")
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = sp.main([str(_paths.FIXTURES / "synthetic_policy.txt"), "--csv", out, "--json"])
        self.assertEqual(code, 0)
        data = json.loads(buf.getvalue())
        self.assertTrue(data["hits"])
        rows = list(csv.DictReader(open(out)))
        self.assertTrue(rows)
        self.assertEqual(set(rows[0].keys()), {"check", "check_title", "phrase", "kind", "common", "line", "page", "snippet"})

    def test_missing_file_and_empty_file(self):
        import tempfile, os, io, contextlib
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            self.assertEqual(sp.main(["/no/such/file.txt"]), 2)
        d = tempfile.mkdtemp()
        p = os.path.join(d, "empty.txt")
        open(p, "w").write("  \n")
        with contextlib.redirect_stderr(err):
            self.assertEqual(sp.main([p]), 2)


class Normalizer(unittest.TestCase):
    def test_curly_quotes_and_long_dashes_are_plain(self):
        text = "insured" + chr(0x2019) + "s " + "machine" + chr(0x2013) + "based"
        norm, _, _ = lib.normalize_with_map(text)
        self.assertEqual(norm, "insured's machine-based")

    def test_form_feed_starts_a_new_page(self):
        norm, lines, pages = lib.normalize_with_map("a\fb")
        self.assertEqual(norm, "a b")
        self.assertEqual(pages[-1], 2)


if __name__ == "__main__":
    unittest.main()
