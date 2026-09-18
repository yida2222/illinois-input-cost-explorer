"""Build a self-contained HTML copy with the published USDA price snapshot."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "index.html"
PRICES = ROOT / "data/prices.json"
OUTPUT = ROOT / "Illinois_Input_Cost_Explorer_Offline.html"


def main() -> None:
    page = SOURCE.read_text(encoding="utf-8")
    data = json.loads(PRICES.read_text(encoding="utf-8"))
    if data.get("slug_id") != 3195 or not data.get("series"):
        raise SystemExit("Missing validated USDA price snapshot")
    payload = json.dumps(data, separators=(",", ":")).replace("<", "\\u003c")
    marker = "<script>\nconst budgets="
    if page.count(marker) != 1:
        raise SystemExit("Could not find the application script marker")
    page = page.replace(marker, f'<script type="application/json" id="embedded-prices">{payload}</script>\n{marker}')
    OUTPUT.write_text(page, encoding="utf-8")
    print(f"Built {OUTPUT.name}; latest USDA report: {data['latest_report_date']}")


if __name__ == "__main__":
    main()
