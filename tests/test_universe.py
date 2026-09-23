import csv
import importlib.util
import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('universe',ROOT/'scripts/build_universe.py')
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class UniverseTests(unittest.TestCase):
    def setUp(self):
        with (ROOT/'config/sp500_securities_2025-12-31.csv').open() as f:
            self.rows=list(csv.DictReader(f))
    def test_reproducible_unique_500_companies(self):
        actual=m.build(self.rows)
        self.assertEqual(actual,json.loads((ROOT/'config/companies.json').read_text()))
        self.assertEqual(sum(len(c['tickers']) for c in actual),503)
        self.assertEqual(len({c['cik'] for c in actual}),500)
        self.assertEqual(sorted(sorted(c['tickers']) for c in actual if len(c['tickers'])>1),[['FOX','FOXA'],['GOOG','GOOGL'],['NWS','NWSA']])
    def test_december_changes_and_exclusions(self):
        tickers={r['ticker'] for r in self.rows}
        self.assertTrue({'ARES','CRH','CVNA','FIX','DAY','HOLX'} <= tickers)
        self.assertFalse(tickers & {'K','LKQ','SOLS','MHK','WHR','TSM','SONY'})
    def test_wrong_date_and_duplicate_fail(self):
        self.rows[0]['as_of']='2026-09-23'
        with self.assertRaises(ValueError): m.build(self.rows)
        self.rows[0]=self.rows[1]
        with self.assertRaises(ValueError): m.build(self.rows)
