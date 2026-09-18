"""Validate and normalize USDA AMS Illinois Production Cost Report prices."""

import json
from datetime import datetime
from pathlib import Path


SOURCE = Path("data/ams_3195_raw.json")
OUTPUT = Path("data/prices.json")
REPORT_URL = "https://mymarketnews.ams.usda.gov/viewReport/3195"
PRODUCTS = {
    "Anhydrous Ammonia": ("ammonia", "Dollars Per Ton"),
    "Urea (46-0-0)": ("urea", "Dollars Per Ton"),
    "No. 2 Diesel (Farm)": ("diesel", "Dollars Per Gallon"),
}


def normalize(payload: object) -> dict:
    if not isinstance(payload, list):
        raise ValueError("USDA response must be a list of report sections")
    sections = {part.get("reportSection"): part for part in payload if isinstance(part, dict)}
    detail = sections.get("Report Details - Prices")
    header = sections.get("Report Header")
    if not isinstance(detail, dict) or not isinstance(header, dict):
        raise ValueError("Expected report header and price details sections")
    rows = detail.get("results")
    headers = header.get("results")
    if not isinstance(rows, list) or not isinstance(headers, list):
        raise ValueError("Report sections have no results array")
    final_dates = {
        row.get("report_end_date")
        for row in headers
        if isinstance(row, dict) and row.get("final_ind") == "Final" and row.get("slug_id") == 3195
    }
    selected = {}
    for row in rows:
        if not isinstance(row, dict) or row.get("slug_id") != 3195:
            continue
        item = PRODUCTS.get(row.get("class"))
        if item is None:
            continue
        product, expected_unit = item
        expected_shipper = "Fuel Distributor" if product == "diesel" else "Distributor"
        if (row.get("price_unit") != expected_unit or row.get("sale_type") != "Ask"
                or row.get("shipping_point") != expected_shipper
                or row.get("market_location_state") != "IL"
                or row.get("report_end_date") not in final_dates):
            raise ValueError(f"Unexpected unit, category, location, or report status for {product}")
        value = row.get("price_avg")
        if not isinstance(value, (int, float)) or isinstance(value, bool) or not 0 < value < 10000:
            raise ValueError(f"Invalid average price for {product}")
        date = datetime.strptime(row["report_end_date"], "%m/%d/%Y").date().isoformat()
        published = datetime.strptime(row["published_date"], "%m/%d/%Y %H:%M:%S")
        key = (product, date)
        if key not in selected or published > selected[key][0]:
            selected[key] = (published, round(float(value), 2))
    series = {name: [] for name in ("ammonia", "urea", "diesel")}
    for (product, date), (published, value) in sorted(selected.items()):
        series[product].append({
            "date": date,
            "value": value,
            "source": REPORT_URL,
            "note": "USDA AMS report 3195",
            "published": published.isoformat(),
        })
    if any(len(points) < 2 for points in series.values()):
        raise ValueError("Too few validated observations for at least one product")
    return {
        "source": "USDA AMS MyMarketNews API",
        "slug_id": 3195,
        "report_url": REPORT_URL,
        "latest_report_date": max(p["date"] for points in series.values() for p in points),
        "latest_published": max(p["published"] for points in series.values() for p in points),
        "series": series,
    }


def main() -> None:
    normalized = normalize(json.loads(SOURCE.read_text(encoding="utf-8")))
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(normalized, indent=2) + "\n", encoding="utf-8")
    print("Validated USDA observations:", {k: len(v) for k, v in normalized["series"].items()})


if __name__ == "__main__":
    main()
