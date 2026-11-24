import csv
import unittest

import _paths

T = _paths.ROOT / "templates"


def rows(name):
    with open(T / name, newline="", encoding="utf-8") as f:
        return list(csv.reader(f))


class Templates(unittest.TestCase):
    def test_register_columns_and_sample_rows(self):
        r = rows("exclusion-register.csv")
        self.assertEqual(r[0][:4], ["check_id", "policy_name", "carrier", "policy_period"])
        self.assertGreaterEqual(len(r), 3)
        for row in r[1:]:
            self.assertEqual(len(row), len(r[0]))
            self.assertTrue(row[1].startswith("SAMPLE"), row)
            self.assertTrue(row[2].startswith("SAMPLE"), row)

    def test_register_check_ids_are_real(self):
        for row in rows("exclusion-register.csv")[1:]:
            self.assertIn(int(row[0]), range(1, 29))

    def test_renewal_log_sample_rows(self):
        r = rows("renewal-change-log.csv")
        self.assertGreaterEqual(len(r), 3)
        for row in r[1:]:
            self.assertEqual(len(row), len(r[0]))
            self.assertTrue(row[1].startswith("SAMPLE"), row)

    def test_ai_use_map_sample_rows(self):
        r = rows("ai-use-map.csv")
        for row in r[1:]:
            self.assertEqual(len(row), len(r[0]))
            self.assertTrue(row[0].startswith("SAMPLE"), row)

    def test_broker_list_has_the_three_reel_questions(self):
        text = (T / "broker-question-list.md").read_text().lower()
        self.assertIn("generative", text)
        self.assertIn("in writing", text)
        self.assertIn("sample", text)


if __name__ == "__main__":
    unittest.main()
