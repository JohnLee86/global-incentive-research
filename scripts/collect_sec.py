"""Collect candidate filings, never infer compensation fiscal year from filing date."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import time
from urllib.parse import quote

import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]

def rows(columns):
    keys = ("accessionNumber", "filingDate", "form", "primaryDocument")
    lengths = [len(columns.get(k, [])) for k in keys]
    if len(set(lengths)) != 1:
        raise ValueError("Inconsistent SEC submission columns")
    return [dict(zip(keys, values)) for values in zip(*(columns.get(k, []) for k in keys))]

def candidates(columns, start, end, forms):
    return [r for r in rows(columns) if start <= r["filingDate"] <= end and r["form"] in forms]

class Client:
    def __init__(self, user_agent):
        if not re.search(r"[^\s@]+@[^\s@]+\.[^\s@]+", user_agent):
            raise ValueError("Set SEC_USER_AGENT to organization/name and real contact email")
        self.session = requests.Session()
        self.session.headers["User-Agent"] = user_agent

    def get(self, url):
        for attempt in range(4):
            time.sleep(0.25)
            r = self.session.get(url, timeout=60)
            if r.status_code == 429 or r.status_code >= 500:
                if attempt < 3:
                    time.sleep(2 ** attempt)
                    continue
            r.raise_for_status()
            return r
        raise RuntimeError("Request failed")

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--start", default="2025-01-01")
    p.add_argument("--end", default="2026-09-23")
    p.add_argument("--company", help="Optional company id")
    p.add_argument("--output", default="data")
    args = p.parse_args()
    from datetime import date, datetime, timezone
    date.fromisoformat(args.start)
    date.fromisoformat(args.end)
    if args.start > args.end:
        p.error("start must be <= end")
    companies = json.loads((ROOT / "config/companies.json").read_text())
    if args.company:
        companies = [c for c in companies if c["id"] == args.company]
        if not companies:
            p.error("Unknown company id")
    client = Client(os.environ.get("SEC_USER_AGENT", ""))
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    manifest, errors, skipped = [], [], []
    def save():
        (out / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
        (out / "status.json").write_text(json.dumps({"errors": errors, "manual_sources_required": skipped}, ensure_ascii=False, indent=2), encoding="utf-8")
    try:
        mapping = client.get("https://www.sec.gov/files/company_tickers.json").json()
    except Exception:
        errors.append({"stage": "ticker_mapping", "error": "SEC mapping fetch failed"})
        save()
        raise
    by_ticker = {v["ticker"]: v for v in mapping.values()}
    for company in companies:
        if not company["sec_forms"]:
            skipped.append(company["id"])
            continue
        try:
            cik = int(by_ticker[company["ticker"]]["cik_str"])
            sub = client.get(f"https://data.sec.gov/submissions/CIK{cik:010d}.json").json()
            selected = candidates(sub["filings"]["recent"], args.start, args.end, company["sec_forms"])
            for archive in sub["filings"].get("files", []):
                if archive["filingFrom"] <= args.end and archive["filingTo"] >= args.start:
                    older = client.get("https://data.sec.gov/submissions/" + archive["name"]).json()
                    selected.extend(candidates(older, args.start, args.end, company["sec_forms"]))
            if not selected:
                errors.append({"company": company["id"], "error": "No candidate filings found"})
            seen = set()
            for row in selected:
                accession = row["accessionNumber"]
                if accession in seen:
                    continue
                seen.add(accession)
                url = f"https://www.sec.gov/Archives/edgar/data/{cik}/{accession.replace('-', '')}/{quote(row['primaryDocument'], safe='/')}"
                record = {**row, "company_id": company["id"], "cik": cik, "sec_company_name": sub["name"], "source_url": url, "target_fiscal_year": 2025, "fiscal_year_verified": False, "status": "pending"}
                try:
                    folder = out / "raw" / company["id"] / accession
                    folder.mkdir(parents=True, exist_ok=True)
                    raw = folder / "source.html"
                    if not raw.exists():
                        response = client.get(url)
                        payload = response.content
                        soup = BeautifulSoup(payload, "html.parser")
                        if not soup.find("html") or "undeclared automated tool" in soup.get_text().lower():
                            raise ValueError("Response is not an accepted HTML filing")
                        raw.write_bytes(payload)
                    payload = raw.read_bytes()
                    soup = BeautifulSoup(payload, "html.parser")
                    for tag in soup(["script", "style"]):
                        tag.decompose()
                    text_path = folder / "text.txt"
                    text_path.write_text(soup.get_text("\n", strip=True), encoding="utf-8")
                    record.update(status="downloaded", raw_path=str(raw), text_path=str(text_path), sha256=hashlib.sha256(payload).hexdigest(), retrieved_at=datetime.now(timezone.utc).isoformat())
                except Exception as exc:
                    record["status"] = "failed"
                    errors.append({"company": company["id"], "accession": accession, "error": type(exc).__name__})
                manifest.append(record)
                save()
        except Exception as exc:
            errors.append({"company": company["id"], "error": type(exc).__name__})
        save()
    print(json.dumps({"downloaded": sum(r["status"] == "downloaded" for r in manifest), "errors": len(errors), "manual_sources_required": skipped}))
    if errors:
        raise SystemExit(1)

if __name__ == "__main__":
    main()
