# Economics

Notebooks analyzing macroeconomic indicators, monetary policy, commodities, and financial markets using public data APIs.

## Notebooks

| # | Title | Description | Key Libraries | Data Source |
|---|-------|-------------|---------------|-------------|
| 001 | [FRED Economic Data](001_fred_data.py) | U.S. economic analysis: interest rates, inflation, labor, housing | fredapi, matplotlib, seaborn | FRED API |
| 002 | [Precious Metals](002_metals_prices.py) | Performance analysis of gold, silver, platinum, palladium, copper | yfinance, matplotlib | Yahoo Finance |
| 003 | [Central Bank Balance Sheets](003_central_banking_asset_growth.py) | Animated comparison of Fed, ECB, and BOJ balance sheet growth | fredapi, plotly | FRED API |
| 004 | [World GDP Per Capita](004_world_gdp_per_capita.py) | GDP per capita rankings with country flags | pandas, requests | World Bank API |

## Prerequisites

- **FRED API key** required for notebooks 001 and 003. Get a free key at [fredaccount.stlouisfed.org/apikeys](https://fredaccount.stlouisfed.org/apikeys). Set as `FRED_API_KEY` environment variable or edit directly in the notebook.
- Notebooks 002 and 004 use free public APIs (no key needed).
