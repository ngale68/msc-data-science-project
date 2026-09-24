import csv
import re
from pathlib import Path

from bs4 import BeautifulSoup


INPUT_DIR = Path("data/discovery/batch_01")
OUTPUT_FILE = Path("results/feasibility/batch_01_metric_variant_audit.csv")

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)


metric_patterns = {
    "turnover_revenue": [
        r"\bturnover\b",
        r"\brevenue\b",
    ],

    "profit_before_taxation": [
    r"\bprofit\s+before\s+tax\w*\b",
    r"\bprofit\s*/\s*\(\s*loss\s*\)\s+before\s+tax\w*\b",
    r"\bprofit\s+\(\s*loss\s*\)\s+before\s+tax\w*\b",
    ],

    "total_assets": [
        r"\btotal\s+assets\b",
    ],

    "net_assets": [
        r"\bnet\s+assets\b",
    ],
}


rows = []

for path in sorted(INPUT_DIR.glob("*.html")):
    with open(path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "xml")

    text = soup.get_text(" ", strip=True)
    lower = text.lower()

    row = {
        "filename": path.name,
    }

    for metric, patterns in metric_patterns.items():
        count = 0

        for pattern in patterns:
            count += len(re.findall(pattern, lower))

        row[f"{metric}_count"] = count
        row[f"{metric}_present"] = count > 0

    rows.append(row)


fieldnames = ["filename"]

for metric in metric_patterns:
    fieldnames.extend([
        f"{metric}_count",
        f"{metric}_present",
    ])


with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)


print(f"Variant audit created for {len(rows)} filings.")
print(f"Saved to: {OUTPUT_FILE}")

print("\nSummary:")

for metric in metric_patterns:
    count_field = f"{metric}_count"
    present_field = f"{metric}_present"

    filings_with_metric = sum(
        1 for row in rows if row[present_field]
    )

    total_occurrences = sum(
        row[count_field] for row in rows
    )

    print(
        f"  {metric}: "
        f"{filings_with_metric}/{len(rows)} filings, "
        f"{total_occurrences} total occurrences"
    )