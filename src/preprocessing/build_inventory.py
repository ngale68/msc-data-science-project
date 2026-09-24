import csv
import re
from pathlib import Path

from bs4 import BeautifulSoup


INPUT_DIR = Path("data/discovery/batch_01")
OUTPUT_FILE = Path("results/feasibility/filing_inventory.csv")

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

filename_pattern = re.compile(
    r"Prod\d+_\d+_(?P<company>\w+)_(?P<period>\d{8})\.html$"
)

def extract_reporting_period_evidence(text):
    patterns = [
        re.compile(
            r"(?i)"
            r"(?:year|period)\s+ended"
            r".{0,80}?"
            r"(?:"
            r"\d{1,2}\s+"
            r"(?:january|february|march|april|may|june|july|august|"
            r"september|october|november|december)"
            r"\s+\d{4}"
            r"|"
            r"\d{4}-\d{2}-\d{2}"
            r"|"
            r"\d{1,2}/\d{1,2}/\d{4}"
            r")"
        ),
        re.compile(
            r"(?i)"
            r"(?:as\s+at)"
            r".{0,80}?"
            r"(?:"
            r"\d{1,2}\s+"
            r"(?:january|february|march|april|may|june|july|august|"
            r"september|october|november|december)"
            r"\s+\d{4}"
            r"|"
            r"\d{4}-\d{2}-\d{2}"
            r"|"
            r"\d{1,2}/\d{1,2}/\d{4}"
            r")"
        ),
    ]

    for pattern in patterns:
        match = pattern.search(text)

        if match:
            return match.group(0).strip()

    return ""

rows = []

for path in sorted(INPUT_DIR.glob("*.html")):

    match = filename_pattern.match(path.name)

    if not match:
        print(f"Skipping unexpected filename: {path.name}")
        continue

    company_number = match.group("company")
    filename_period = match.group("period")

    with open(path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "xml")

    text = soup.get_text(" ", strip=True)
    lower = text.lower()

    financial_statement_terms = [
        "statement of financial position",
        "statement of comprehensive income",
        "balance sheet",
        "profit and loss account",
        "profit and loss",
    ]

    has_financial_statement_terms = any(
        term in lower for term in financial_statement_terms
    )

    rows.append({
        "filename": path.name,
        "company_number": company_number,
        "filename_period": filename_period,
        "file_size_bytes": path.stat().st_size,
        "visible_text_chars": len(text),
        "table_count": len(soup.find_all("table")),
        "has_year_reference": bool(
            re.search(r"\b20\d{2}\b", text)
        ),
        "has_financial_statement_terms": has_financial_statement_terms,
        "has_reporting_period_phrase": bool(
            re.search(
                r"\b(?:year|period)\s+ended\b|\bas\s+at\b",
                lower
            )
        ),
        "reporting_period_evidence": extract_reporting_period_evidence(text),
    })


fieldnames = [
    "filename",
    "company_number",
    "filename_period",
    "file_size_bytes",
    "visible_text_chars",
    "table_count",
    "has_year_reference",
    "has_financial_statement_terms",
    "has_reporting_period_phrase",
    "reporting_period_evidence",
]

with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"Inventory created for {len(rows)} filings.")
print(f"Saved to: {OUTPUT_FILE}")
