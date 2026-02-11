# Atlas Research Notebooks

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/atlas-research-io/atlas-research-notebooks)](https://github.com/atlas-research-io/atlas-research-notebooks/stargazers)
[![GitHub last commit](https://img.shields.io/github/last-commit/atlas-research-io/atlas-research-notebooks)](https://github.com/atlas-research-io/atlas-research-notebooks/commits/main)
[![GitHub contributors](https://img.shields.io/github/contributors/atlas-research-io/atlas-research-notebooks)](https://github.com/atlas-research-io/atlas-research-notebooks/graphs/contributors)
[![Jupytext](https://img.shields.io/badge/format-jupytext%20py%3Apercent-blue)](https://jupytext.readthedocs.io/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

Open-source research notebooks covering crypto, economics, geography, machine learning, and more. Built with [Jupytext](https://jupytext.readthedocs.io/) for clean version control and created on the [Atlas Research](https://atlas-research.io) platform.

## Table of Contents

- [Notebooks](#notebooks)
  - [Crypto](#crypto)
  - [Economics](#economics)
  - [Geography](#geography)
  - [Machine Learning](#machine-learning)
  - [Programming](#programming)
- [Coming Soon](#coming-soon)
- [Quick Start](#quick-start)
- [Working with Jupytext](#working-with-jupytext)
- [Running in Google Colab](#running-in-google-colab)
- [API Keys](#api-keys)
- [Contributing](#contributing)

## Notebooks

### Crypto

Research notebooks exploring cryptocurrency markets, trading analysis, and blockchain data.

| # | Notebook | Description | Data Source |
|---|----------|-------------|-------------|
| 001 | [Crypto Correlation](crypto/001_crypto_correlation.py) | Correlation analysis of top 20 cryptocurrencies by volume | CCXT / Binance |
| 002 | [Implied Volatility Surface](crypto/002_implied_volatility_surface_analysis.py) | Options implied volatility surface visualization | CCXT / Deribit |
| 003 | [Volume Profile & Market Regime](crypto/003_volume_profile_market_regime.py) | Volume-based market regime detection for BTC | CCXT / Binance |
| 004 | [Bitcoin Rainbow Chart](crypto/004_bitcoin_log_regression_rainbow.py) | Log regression rainbow chart with halving events | CCXT |
| 005 | [CCXT Documentation](crypto/005_ccxt_documentation.py) | Comprehensive guide to the CCXT library | CCXT |
| 006 | [Hourly Returns Heatmap](crypto/006_crypto_average_returns_by_utc_time.py) | Average returns by hour of day across crypto assets | CCXT / Binance |

### Economics

Notebooks analyzing macroeconomic indicators, monetary policy, and financial markets.

| # | Notebook | Description | Data Source |
|---|----------|-------------|-------------|
| 001 | [FRED Economic Data](economics/001_fred_data.py) | Comprehensive U.S. economic analysis (rates, inflation, labor, housing) | FRED API |
| 002 | [Precious Metals](economics/002_metals_prices.py) | Performance analysis of gold, silver, platinum, palladium, copper | Yahoo Finance |
| 003 | [Central Bank Balance Sheets](economics/003_central_banking_asset_growth.py) | Animated comparison of Fed, ECB, and BOJ balance sheet growth | FRED API |
| 004 | [World GDP Per Capita](economics/004_world_gdp_per_capita.py) | GDP per capita rankings with country flags | World Bank API |

### Geography

Visualizations of geographic data, world statistics, and historical exploration.

| # | Notebook | Description | Data Source |
|---|----------|-------------|-------------|
| 001 | [World Geography Stats](geography/001_world_geography.py) | Interactive exploration of Earth's geographic features and climate extremes | CIA World Factbook |
| 002 | [Magellan's Circumnavigation](geography/002_megallan.py) | Animated globe tracing the first circumnavigation (1519-1522) | Historical data |

### Machine Learning

Implementations of foundational ML papers and algorithms.

| # | Notebook | Description | Key Libraries |
|---|----------|-------------|---------------|
| 001 | [Attention Is All You Need](machine-learning/001_attention_is_all_you_need.py) | Full Transformer architecture implementation (Vaswani et al. 2017) | NumPy, Matplotlib |

### Programming

Tutorials and fundamentals for programming languages and techniques.

| # | Notebook | Description | Topic |
|---|----------|-------------|-------|
| 001 | [Python Fundamentals](programming/001_python_fundamentals.py) | Variables, control flow, functions, data structures, OOP | Python |

## Coming Soon

We're expanding into these research areas -- contributions welcome!

- **Backtesting** -- Trading strategy backtesting frameworks and examples
- **Geopolitics** -- Geopolitical data analysis, political risk modeling
- **Political Data** -- Election data, legislative analysis, polling

## Quick Start

1. **Clone the repository:**
   ```bash
   git clone https://github.com/atlas-research-io/atlas-research-notebooks.git
   cd atlas-research-notebooks
   ```

2. **Set up a virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   .venv\Scripts\activate     # Windows
   ```

3. **Install core dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Open any notebook** -- dependencies are installed automatically via `!pip install` cells at the top of each notebook.

## Working with Jupytext

This repository stores notebooks as Python scripts (`.py` files) using [Jupytext](https://jupytext.readthedocs.io/) percent format instead of `.ipynb` files. This gives us clean git diffs, easy code review, and no merge conflicts from notebook metadata.

### Opening notebooks locally

```bash
# Convert a .py file to .ipynb for use in Jupyter
jupytext --to notebook crypto/001_crypto_correlation.py

# Or open .py files directly in VS Code with the Jupyter extension
# The # %% markers create interactive cells automatically
```

### Exporting from Atlas Research (recommended)

Create and edit notebooks on [atlas-research.io](https://atlas-research.io), then use the **Jupytext export button** in the top toolbar to export as `.py` files.

### Syncing changes

```bash
# After editing an .ipynb locally, sync back to .py
jupytext --sync crypto/001_crypto_correlation.ipynb

# Only commit the .py file -- .ipynb files are gitignored
```

## Running in Google Colab

Since the repo uses Jupytext `.py` files, convert to `.ipynb` first:

```bash
jupytext --to notebook crypto/001_crypto_correlation.py
```

Then upload the generated `.ipynb` file to [Google Colab](https://colab.research.google.com/).

## API Keys

Some notebooks require API keys. Copy `.env.example` to `.env` and fill in your keys:

```bash
cp .env.example .env
```

| API | Notebooks | How to Get |
|-----|-----------|------------|
| FRED | Economics 001, 003 | Free at [fredaccount.stlouisfed.org/apikeys](https://fredaccount.stlouisfed.org/apikeys) |

Most notebooks (crypto via CCXT, geography via World Bank) use **free public APIs** and require no keys.

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for full guidelines. Quick summary:

- Notebooks use **Jupytext `py:percent` format** (not `.ipynb`)
- Follow naming convention: `NNN_descriptive_name.py`
- Include a `!pip install` cell for dependencies
- Use **dark theme** styling (`plt.style.use('dark_background')`)
- Add markdown cells explaining each section
- Test that notebooks run from top to bottom without errors

## License

[MIT](LICENSE)

---

*Start your research journey at [atlas-research.io](https://atlas-research.io)*
