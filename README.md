# Illinois Input Cost Explorer

Independent student prototype prepared September 17, 2026. The public `index.html` reads `data/prices.json` generated from USDA AMS. For a portable local copy, open `Illinois_Input_Cost_Explorer_Offline.html` directly in a browser: it embeds the validated USDA price snapshot and needs no server or installation. The offline snapshot does not update itself; rebuild it with `python3 scripts/build_offline.py` after the data file changes.

**Data pipeline:** A GitHub Action fetches the most recent 365 days of USDA MyMarketNews report 3195 on Mondays and Fridays and on manual request. The repository owner stores a personal `USDA_MMN_API_KEY` as an Actions Secret. The key is used only in the Action and is not sent to visitors or stored in the site. `scripts/normalize_usda.py` validates the report section, product class, Illinois location, asking-price basis, unit, distributor category, final report status, and average price before publishing `data/prices.json`. The raw API response is retained as a one-day Actions artifact and is excluded from the public repository.

## Purpose

Display verified public Illinois input-price observations alongside a transparent sensitivity analysis for four published 2027 Illinois crop budgets. This is an exploratory budget scenario, not a yield model, price forecast, agronomic recommendation, or official farmdoc tool.

## Sources

- Gary Schnitkey and Nick Paulson, *2027 Crop Budgets for All Regions*, Tables 1–4, original release August 2026: https://farmdoc.illinois.edu/assets/management/crop-budgets/crop_budgets_2026_Aug.pdf
- USDA AMS, *Illinois Production Cost Report (Bi-weekly)*, report 3195: https://mymarketnews.ams.usda.gov/viewReport/3195
- Nick Paulson et al., *Fertilizer and Fuel Prices Higher Heading into Fall 2026*, August 11, 2026, for the selected August 7 observations: https://farmdocdaily.illinois.edu/2026/08/fertilizer-and-fuel-prices-higher-heading-into-fall-2026.html

The site shows report-dated USDA observations from the last 365 days when the automated data file is available. Its status line states the latest report end date. USDA quotations are distributor asking-price averages, not transaction prices paid by a specific farm. A stale or missing report must not be described as a live farm price.

The observation graphic marks every validated report date, displays price-axis values, and highlights the latest average and change from the prior report. With four or more points, a line connects the observations without estimating unreported dates. A separate sensitivity curve is calculated from the published budget across fertilizer-cost changes from −30% to +80%, holding the currently selected fuel and crop-price assumptions fixed. Its lines represent model outputs, not observed returns, estimated probabilities, or forecasts. The horizontal zero line is zero farmer return. The full budget table can be expanded when a reviewer needs to inspect the arithmetic.

## Budget inputs and formulas

The region selector uses corn after soybeans and soybeans after corn in every table. Northern and Southern Illinois have no productivity subclass in the source.

| Published table and region | Corn baseline farmer return, $/acre | Soybean baseline farmer return, $/acre |
| --- | ---: | ---: |
| Table 1 · Northern Illinois | 38 | 68 |
| Table 2 · Central Illinois, high productivity | 36 | 86 |
| Table 3 · Central Illinois, low productivity | 39 | 74 |
| Table 4 · Southern Illinois | −51 | 18 |

The application stores each region's published yield, crop price, ARC/PLC payment, fertilizer cost, fuel cost, total non-land costs, and land costs. Changing region replaces **all** of these inputs together. The comparison table shows published baseline farmer returns; it does not apply the active slider assumptions across regions.

For each crop, the page computes:

1. Crop revenue = published yield × published crop price × (1 + user crop-price change).
2. Gross revenue = crop revenue + published ARC/PLC payment.
3. Scenario fertilizer cost = published fertilizer line × (1 + user fertilizer-cost change).
4. Scenario fuel cost = published fuel-and-oil line × (1 + user fuel-cost change).
5. Scenario non-land costs = published total non-land costs + change in fertilizer line + change in fuel line.
6. Farmer return = gross revenue − scenario non-land costs − published land costs.

The fertilizer percentage is an assumption about the **whole budget fertilizer line**, not a mechanical pass-through from anhydrous ammonia or urea prices. No physical application rates are inferred from aggregate budget dollars. The crop comparison is between the two specified rotation columns, not a prediction that farmers will switch crops.

The "What drives the change?" table decomposes the return change into crop-price revenue, fertilizer cost, and fuel cost. At selected cost assumptions, the break-even crop price is `(scenario non-land costs + published land costs − published ARC/PLC payment) / published yield`. This is a zero-return threshold in the static budget, not an estimated market price. The observed input quotations and the 2027 budget come from different dates; this prototype does not estimate the timing or magnitude of price pass-through.

## Verification examples

- Baseline: corn gross revenue 245 × 5 + 17 = 1,242; farmer return 1,242 − 885 − 321 = 36. Soybean gross revenue 77 × 12 + 17 = 941; farmer return 941 − 534 − 321 = 86.
- Fertilizer +20%, other changes 0: corn return 36 − (263 × .20) = −16.60; soybean return 86 − (77 × .20) = 70.60.
- Fertilizer +20% and fuel +10%, crop prices unchanged: corn return 36 − 52.60 − 3 = −19.60; soybean return 86 − 15.40 − 2.60 = 68.00.
- Crop prices +5% only: corn return 36 + (245 × 5 × .05) = 97.25; soybean return 86 + (77 × 12 × .05) = 132.20.
- Baseline break-even crop prices: corn (885 + 321 − 17) / 245 ≈ $4.85/bu; soybeans (534 + 321 − 17) / 77 ≈ $10.88/bu.

These checks validate arithmetic only. They do not validate whether any particular shock is likely.

## Possible next step after professor feedback

If the research team finds it useful, extend the archive beyond the current rolling year and add explicit corrected-report monitoring. Any use of nonpublic FBFM data would require authorization and a separate data-handling plan. The prototype should not be publicly represented as affiliated with the University of Illinois or farmdoc.
