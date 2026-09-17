# Illinois Input Cost Explorer

Independent student prototype prepared September 17, 2026. Open `index.html` in a browser; it has no installation requirements and makes no network requests to run. The source links open only if the user clicks them.

**Data status:** The public webpage still displays the manually verified sample observations below. USDA MyMarketNews report 3195 has an authenticated API, but it cannot be called directly from a public browser. The repository includes a manual diagnostic GitHub Action that can fetch a recent JSON sample after the repository owner adds a personal `USDA_MMN_API_KEY` secret. The sample is kept as a one-day Actions artifact, not committed into the public repository. We will map and validate the actual API fields before enabling automatic updates or labeling the webpage as API-fed.

## Purpose

Display a small number of verified public Illinois input-price observations alongside a transparent sensitivity analysis for the 2027 Central Illinois high-productivity crop budget. This is an exploratory budget scenario, not a yield model, price forecast, agronomic recommendation, or official farmdoc tool.

## Sources

- Gary Schnitkey and Nick Paulson, *2027 Crop Budgets for All Regions*, Table 2 (Central Illinois, high-productivity farmland), original release August 2026: https://farmdoc.illinois.edu/assets/management/crop-budgets/crop_budgets_2026_Aug.pdf
- USDA AMS, *Illinois Production Cost Report*, September 4, 2026: https://www.ams.usda.gov/mnreports/ams_3195.pdf
- Nick Paulson et al., *Fertilizer and Fuel Prices Higher Heading into Fall 2026*, August 11, 2026, for the selected August 7 observations: https://farmdocdaily.illinois.edu/2026/08/fertilizer-and-fuel-prices-higher-heading-into-fall-2026.html

The price series is intentionally sparse: ammonia and diesel have two verified observations, while urea has one. Do not infer a full trend or current market price from these points. The USDA quotations are distributor asking-price averages, not transaction prices paid by a specific farm.

The observation graphic shows separate dots rather than a line because only one or two dates are verified. A separate sensitivity curve is calculated from the published budget across fertilizer-cost changes from −30% to +80%, holding the currently selected fuel and crop-price assumptions fixed. Its lines represent model outputs, not observed returns, estimated probabilities, or forecasts. The horizontal zero line is zero farmer return.

## Budget inputs and formulas

| 2027 Table 2 line item, dollars per acre unless noted | Corn after soybeans | Soybeans after corn |
| --- | ---: | ---: |
| Yield, bushels per acre | 245 | 77 |
| Crop price, dollars per bushel | 5.00 | 12.00 |
| ARC/PLC payment | 17 | 17 |
| Fertilizer | 263 | 77 |
| Fuel and oil | 30 | 26 |
| Total non-land costs | 885 | 534 |
| Land costs | 321 | 321 |
| Farmer return | 36 | 86 |

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

If the research team finds it useful, expand the historical price series via the USDA MyMarketNews API and add its corrected-report handling. Any use of nonpublic FBFM data would require authorization and a separate data-handling plan. The prototype should not be publicly represented as affiliated with the University of Illinois or farmdoc.
