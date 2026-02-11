# Crypto

Research notebooks exploring cryptocurrency markets, trading analysis, and blockchain data. All notebooks use the [CCXT](https://github.com/ccxt/ccxt) library to fetch live data from exchanges.

## Notebooks

| # | Title | Description | Key Libraries |
|---|-------|-------------|---------------|
| 001 | [Crypto Correlation](001_crypto_correlation.py) | Price correlation matrix of top 20 cryptos by volume | ccxt, seaborn |
| 002 | [Implied Volatility Surface](002_implied_volatility_surface_analysis.py) | Options IV surface analysis for Bitcoin | ccxt, matplotlib |
| 003 | [Volume Profile & Market Regime](003_volume_profile_market_regime.py) | Volume-based market regime detection for BTC/USDT | ccxt, numpy |
| 004 | [Bitcoin Rainbow Chart](004_bitcoin_log_regression_rainbow.py) | Log regression rainbow chart with halving events | ccxt, scipy |
| 005 | [CCXT Documentation](005_ccxt_documentation.py) | Comprehensive guide to the CCXT library | ccxt, mplfinance |
| 006 | [Hourly Returns Heatmap](006_crypto_average_returns_by_utc_time.py) | Average log returns by UTC hour across crypto assets | ccxt, seaborn |

## Prerequisites

- No API keys required (uses public exchange endpoints via CCXT)
- Internet connection required for live data fetching
