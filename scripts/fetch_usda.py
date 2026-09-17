"""Fetch a small authenticated sample of USDA AMS report 3195.

This diagnostic step keeps the personal API key out of the public website and
lets us inspect the report's actual JSON structure before mapping price fields.
"""

import base64
import json
import os
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


URL = "https://marsapi.ams.usda.gov/services/v1.2/reports/3195?lastDays=90&allSections=true"
OUTPUT = Path("data/ams_3195_sample.json")


def main() -> None:
    key = os.environ.get("USDA_MMN_API_KEY", "").strip()
    if not key:
        raise SystemExit("USDA_MMN_API_KEY is required; obtain a personal key from MyMarketNews.")
    encoded = base64.b64encode(f"{key}:".encode()).decode()
    request = Request(
        URL,
        headers={"Authorization": f"Basic {encoded}", "Accept": "application/json"},
    )
    try:
        with urlopen(request, timeout=30) as response:
            body = response.read(5_000_001)
    except HTTPError as exc:
        raise SystemExit(f"USDA API returned HTTP {exc.code}; key or endpoint may need review.") from None
    except URLError:
        raise SystemExit("Could not reach the USDA API.") from None
    if len(body) > 5_000_000:
        raise SystemExit("USDA API response exceeded the 5 MB inspection limit.")
    try:
        payload = json.loads(body)
    except ValueError:
        raise SystemExit("USDA API returned a non-JSON response.") from None
    if not isinstance(payload, (dict, list)):
        raise SystemExit("USDA API returned an unexpected JSON root.")
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"Saved published report sample to {OUTPUT}; API key was not saved.")


if __name__ == "__main__":
    main()
