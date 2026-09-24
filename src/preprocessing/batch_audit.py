import csv
from pathlib import Path

from bs4 import BeautifulSoup


INPUT_DIR = Path("data/discovery/batch_01")
OUTPUT_FILE = Path("results/feasibility/batch_01_audit.csv")

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

metrics = [
    "turnover",
    "profit before tax",
    "total assets",
    "net assets",
]

rows = []

for path in sorted(INPUT_DIR.glob("*.html")):
    with open(path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "xml")

    text = soup.get_text(" ", strip=True)
    lower = text.lower()

    tables = soup.find_all("table")

    record = {
        "filing": path.name,
        "file_size_bytes": path.stat().st_size,
        "visible_text_chars": len(text),
        "table_count": len(tables),
    }

    for metric in metrics:
        record[f"{metric.replace(' ', '_')}_occurrences"] = lower.count(metric)

    rows.append(record)


fieldnames = list(rows[0].keys())

with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"Audited {len(rows)} filings.")
print(f"Saved results to: {OUTPUT_FILE}")

print("\nSummary:")
for metric in metrics:
    column = f"{metric.replace(' ', '_')}_occurrences"
    present = sum(row[column] > 0 for row in rows)
    total = sum(row[column] for row in rows)

    print(
        f"  {metric}: "
        f"{present}/{len(rows)} filings contain the phrase; "
        f"{total} total occurrences"
    )
