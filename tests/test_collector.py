import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location("collector", Path(__file__).resolve().parents[1] / "scripts/collect_sec.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class CollectorTests(unittest.TestCase):
    def test_date_and_form_filter_does_not_select_other_filings(self):
        c = {"accessionNumber":["a","b","c","d"], "filingDate":["2024-12-31","2025-01-01","2026-09-23","2026-09-23"], "form":["DEF 14A","DEF 14A","10-K","8-K"], "primaryDocument":["a.htm"]*4}
        self.assertEqual([r["accessionNumber"] for r in m.candidates(c,"2025-01-01","2026-09-23",["DEF 14A","10-K"])], ["b","c"])
    def test_malformed_columns_fail(self):
        with self.assertRaises(ValueError):
            m.rows({"form":["10-K"]})
    def test_contact_is_required(self):
        with self.assertRaises(ValueError):
            m.Client("")
