import sys
from bs4 import BeautifulSoup

if len(sys.argv) != 2:
    raise SystemExit("Usage: python src/preprocessing/inspect_filing.py <path-to-html>")

path = sys.argv[1]

with open(path, "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f.read(), "xml")

text = soup.get_text(" ", strip=True)

tables = soup.find_all("table")
headings = soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])

print(f"HTML characters: {len(str(soup)):,}")
print(f"Tables: {len(tables):,}")
print(f"Headings: {len(headings):,}")
print(f"Visible text characters: {len(text):,}")

print("\nMetric occurrences:")
for metric in ["turnover", "profit before tax", "total assets", "net assets"]:
    print(f"  {metric}: {text.lower().count(metric)}")

print("\nFirst 10 tables:")
for i, table in enumerate(tables[:10]):
    rows = table.find_all("tr")
    print(f"  Table {i}: {len(rows)} rows")