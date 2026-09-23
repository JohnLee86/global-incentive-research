"""Rebuild the fixed company universe from the checked-in security snapshot."""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def build(rows):
    if len(rows) != 503 or len({r['ticker'] for r in rows}) != 503:
        raise ValueError('Expected 503 unique securities')
    groups = {}
    for r in rows:
        if r['as_of'] != '2025-12-31' or not r['cik'].isdigit() or int(r['cik']) <= 0:
            raise ValueError('Invalid snapshot date or CIK')
        cik = str(int(r['cik'])).zfill(10)
        c = groups.setdefault(cik, dict(id='cik_'+cik, cik=cik, name=r['name'], ticker=r['ticker'], tickers=[], sector=r['sector'], universe_as_of='2025-12-31', target_fiscal_year=2025, sec_forms=['DEF 14A','DEF 14A/A','10-K','10-K/A','20-F','20-F/A']))
        c['tickers'].append(r['ticker'])
    if len(groups) != 500:
        raise ValueError('Expected 500 issuers after CIK deduplication')
    return sorted(groups.values(), key=lambda c: c['id'])

def main():
    with (ROOT/'config/sp500_securities_2025-12-31.csv').open() as f:
        companies = build(list(csv.DictReader(f)))
    (ROOT/'config/companies.json').write_text(json.dumps(companies,ensure_ascii=False,indent=2)+'\n')
    with (ROOT/'research/search_queue.csv').open('w') as f:
        w=csv.writer(f); w.writerow(['company_id','query','status'])
        for c in companies:
            w.writerow([c['id'],c['name']+' compensation performance management total rewards interview bonus pool','pending'])
    print(f'503 securities -> {len(companies)} companies')

if __name__ == '__main__':
    main()
