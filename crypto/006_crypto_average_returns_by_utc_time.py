# %% [markdown]
# # Crypto Hourly Returns Heatmap Analysis
# 
# This notebook fetches historical OHLCV data for a universe of cryptocurrencies from Binance US and calculates the average log returns for each hour of the day. The results are visualized as a heatmap with green (positive returns) and red (negative returns).

# %%
# Install required packages if needed
# !pip install ccxt pandas numpy matplotlib seaborn

# %%
import numpy as np
import pandas as pd
import ccxt
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import warnings
warnings.filterwarnings('ignore')

print(f"CCXT version: {ccxt.__version__}")
print("Libraries loaded successfully!")

# %% [markdown]
# ## Configuration Parameters
# 
# Adjust these parameters to customize the analysis:

# %%
# =============================================================================
# CONFIGURATION PARAMETERS
# =============================================================================

TIMEFRAME = '1h'
DAYS_BACK = 100

CRYPTO_UNIVERSE = [
    'BTC', 'ETH', 'BNB', 'XRP', 'ADA', 
    'DOGE', 'SOL', 'LTC', 'LINK', 'ATOM'
]

print(f"Timeframe: {TIMEFRAME}")
print(f"Lookback: {DAYS_BACK} days")
print(f"Universe: {len(CRYPTO_UNIVERSE)} cryptocurrencies")
print(f"Symbols: {CRYPTO_UNIVERSE}")

# %% [markdown]
# ## Helper Functions
# 
# Core functions for fetching data and calculating analytics:

# %%
def get_timeframe_ms(timeframe: str) -> int:
    """Get timeframe duration in milliseconds"""
    timeframe_map = {
        '15m': 15 * 60 * 1000,
        '1h': 60 * 60 * 1000,
        '4h': 4 * 60 * 60 * 1000,
        '1d': 24 * 60 * 60 * 1000
    }
    return timeframe_map.get(timeframe, 60 * 60 * 1000)


def get_time_bucket(timestamp: pd.Timestamp, timeframe: str) -> str:
    """Get the time bucket label for a given timestamp"""
    if timeframe == '15m':
        hour = timestamp.hour
        minute_bucket = (timestamp.minute // 15) * 15
        return f"{hour:02d}:{minute_bucket:02d}"
    elif timeframe == '1h':
        return f"{timestamp.hour:02d}:00"
    elif timeframe == '4h':
        hour_bucket = (timestamp.hour // 4) * 4
        return f"{hour_bucket:02d}-{hour_bucket+4:02d}"
    elif timeframe == '1d':
        return timestamp.strftime('%A')
    else:
        return str(timestamp.hour)


def get_all_time_buckets(timeframe: str) -> List[str]:
    """Get all possible time buckets for a timeframe"""
    if timeframe == '15m':
        return [f"{h:02d}:{m:02d}" for h in range(24) for m in [0, 15, 30, 45]]
    elif timeframe == '1h':
        return [f"{h:02d}:00" for h in range(24)]
    elif timeframe == '4h':
        return [f"{h:02d}-{h+4:02d}" for h in range(0, 24, 4)]
    elif timeframe == '1d':
        return ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    else:
        return [f"{h:02d}:00" for h in range(24)]


def calculate_log_returns(prices: np.ndarray) -> np.ndarray:
    """Calculate log returns from price series"""
    return np.log(prices[1:] / prices[:-1])


print("Helper functions defined!")
print(f"Time buckets for {TIMEFRAME}: {len(get_all_time_buckets(TIMEFRAME))} buckets")

# %%
def fetch_ohlcv_data(exchange, symbol: str, timeframe: str, days_back: int) -> Optional[pd.DataFrame]:
    """
    Fetch OHLCV data from Binance US for a given symbol.
    Handles pagination for large data requests.
    """
    try:
        ccxt_symbol = f"{symbol}/USDT"
        
        # Calculate total candles needed
        candles_per_day = {
            '15m': 24 * 4,
            '1h': 24,
            '4h': 6,
            '1d': 1
        }
        total_needed = days_back * candles_per_day.get(timeframe, 24)
        
        # Fetch data in chunks
        all_ohlcv = []
        chunk_size = 1000
        target_start = datetime.now() - timedelta(days=days_back)
        since = int(target_start.timestamp() * 1000)
        
        while len(all_ohlcv) < total_needed:
            try:
                chunk = exchange.fetch_ohlcv(ccxt_symbol, timeframe, since=since, limit=chunk_size)
                
                if not chunk:
                    break
                
                all_ohlcv.extend(chunk)
                
                # Update since to fetch next chunk
                since = chunk[-1][0] + get_timeframe_ms(timeframe)
                
                # Break if we've caught up to current time
                if since > int(datetime.now().timestamp() * 1000):
                    break
                    
            except Exception as e:
                print(f"  Error fetching chunk for {symbol}: {e}")
                break
        
        if not all_ohlcv or len(all_ohlcv) < 10:
            return None
        
        # Create DataFrame
        df = pd.DataFrame(all_ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)
        df.sort_index(inplace=True)
        
        # Remove duplicates
        df = df[~df.index.duplicated(keep='first')]
        
        return df
        
    except Exception as e:
        print(f"  OHLCV fetch failed for {symbol}: {e}")
        return None


print("Data fetching function defined!")

# %%
def calculate_time_analytics(df: pd.DataFrame, timeframe: str, days_back: int) -> Dict[str, Dict]:
    """
    Calculate time-based analytics including average returns per time bucket.
    """
    if df is None or len(df) < 10:
        return {}
    
    try:
        # Filter to lookback period
        cutoff_date = datetime.now() - timedelta(days=days_back)
        df_filtered = df[df.index >= cutoff_date].copy()
        
        if len(df_filtered) < 2:
            return {}
        
        # Calculate log returns
        close_prices = df_filtered['close'].values.astype(float)
        log_returns = calculate_log_returns(close_prices)
        
        # Align returns with timestamps (returns are for period ending at timestamp)
        df_filtered = df_filtered.iloc[1:].copy()
        df_filtered['log_return'] = log_returns
        df_filtered['time_bucket'] = df_filtered.index.map(lambda x: get_time_bucket(x, timeframe))
        
        # Initialize results
        time_buckets_returns = {}
        time_buckets_positive_pct = {}
        
        # Get all time buckets
        all_buckets = get_all_time_buckets(timeframe)
        
        # Calculate metrics for each bucket
        for bucket in all_buckets:
            bucket_data = df_filtered[df_filtered['time_bucket'] == bucket]
            
            if len(bucket_data) > 0:
                time_buckets_returns[bucket] = float(bucket_data['log_return'].mean())
                positive_count = (bucket_data['log_return'] > 0).sum()
                time_buckets_positive_pct[bucket] = float((positive_count / len(bucket_data)) * 100.0)
            else:
                time_buckets_returns[bucket] = 0.0
                time_buckets_positive_pct[bucket] = 50.0
        
        return {
            'time_buckets_returns': time_buckets_returns,
            'time_buckets_positive_pct': time_buckets_positive_pct,
            'total_candles': len(df_filtered)
        }
        
    except Exception as e:
        print(f"  Error in calculate_time_analytics: {e}")
        return {}


print("Analytics calculation function defined!")

# %% [markdown]
# ## Initialize Exchange and Fetch Data
# 
# Connect to Binance US and fetch OHLCV data for all symbols in our universe:

# %%
# Initialize Binance US exchange
exchange = ccxt.binanceus({
    'sandbox': False,
    'enableRateLimit': True,
})

# Load markets
print("Loading markets from Binance US...")
exchange.load_markets()
print(f"Loaded {len(exchange.markets)} markets")

# Check which symbols are available
available_symbols = []
unavailable_symbols = []

for symbol in CRYPTO_UNIVERSE:
    ccxt_symbol = f"{symbol}/USDT"
    if ccxt_symbol in exchange.markets:
        available_symbols.append(symbol)
    else:
        unavailable_symbols.append(symbol)

print(f"\nAvailable symbols: {len(available_symbols)}/{len(CRYPTO_UNIVERSE)}")
if unavailable_symbols:
    print(f"Unavailable on Binance US: {unavailable_symbols}")

# %%
# Fetch data for all available symbols
print(f"\nFetching {TIMEFRAME} data for the past {DAYS_BACK} days...")
print("="*60)

all_analytics = {}
failed_symbols = []

for i, symbol in enumerate(available_symbols):
    print(f"[{i+1}/{len(available_symbols)}] Fetching {symbol}...", end=" ")
    
    df = fetch_ohlcv_data(exchange, symbol, TIMEFRAME, DAYS_BACK)
    
    if df is not None:
        analytics = calculate_time_analytics(df, TIMEFRAME, DAYS_BACK)
        if analytics:
            all_analytics[symbol] = analytics
            print(f"✓ ({analytics['total_candles']} candles)")
        else:
            failed_symbols.append(symbol)
            print("✗ (analytics failed)")
    else:
        failed_symbols.append(symbol)
        print("✗ (no data)")

print("="*60)
print(f"\nSuccessfully processed: {len(all_analytics)}/{len(available_symbols)} symbols")
if failed_symbols:
    print(f"Failed symbols: {failed_symbols}")

# %% [markdown]
# ## Create Returns DataFrame
# 
# Organize the hourly returns data into a DataFrame for visualization:

# %%
# Create DataFrame with returns for each symbol and time bucket
time_buckets = get_all_time_buckets(TIMEFRAME)

# Build returns matrix
returns_data = {}
for symbol, analytics in all_analytics.items():
    returns_data[symbol] = analytics['time_buckets_returns']

# Create DataFrame
returns_df = pd.DataFrame(returns_data)
returns_df.index = time_buckets
returns_df.index.name = 'Hour'

# Convert to percentage for better readability
returns_df_pct = returns_df * 100

print(f"Returns DataFrame shape: {returns_df.shape}")
print(f"\nSample of average hourly returns (in %):")
returns_df_pct.head(10)

# %%
# Calculate average returns across all symbols for each hour
avg_returns_by_hour = returns_df_pct.mean(axis=1)

print("Average Returns by Hour (across all symbols):")
print("="*50)
for hour, ret in avg_returns_by_hour.items():
    direction = "🟢" if ret > 0 else "🔴" if ret < 0 else "⚪"
    print(f"{hour}: {ret:+.4f}% {direction}")

# %% [markdown]
# ## Heatmap Visualization
# 
# Create a red/green heatmap showing average log returns by hour for each cryptocurrency:

# %%
plt.style.use('dark_background')
plt.rcParams['figure.facecolor'] = '#1e1e1e'
plt.rcParams['axes.facecolor'] = '#1e1e1e'
plt.rcParams['savefig.facecolor'] = '#1e1e1e'
plt.rcParams['text.color'] = 'white'
plt.rcParams['axes.labelcolor'] = 'white'
plt.rcParams['xtick.color'] = 'white'
plt.rcParams['ytick.color'] = 'white'

fig, ax = plt.subplots(figsize=(16, 10))
fig.patch.set_facecolor('#1e1e1e')
ax.set_facecolor('#1e1e1e')

from matplotlib.colors import LinearSegmentedColormap
colors_list = ['#8B0000', '#CD5C5C', '#F5F5F5', '#90EE90', '#006400']
cmap = LinearSegmentedColormap.from_list('red_green', colors_list, N=256)

max_abs_val = max(abs(returns_df_pct.values.min()), abs(returns_df_pct.values.max()))
vmin, vmax = -max_abs_val, max_abs_val

annot_labels = returns_df_pct.T.applymap(lambda x: f'{x:.2f}')

heatmap = sns.heatmap(
    returns_df_pct.T,
    cmap=cmap,
    center=0,
    vmin=vmin,
    vmax=vmax,
    annot=annot_labels,
    fmt='',
    linewidths=1,
    linecolor='#1e1e1e',
    cbar_kws={'label': 'Average Log Return (%)', 'shrink': 0.8},
    ax=ax,
    annot_kws={'fontsize': 7, 'fontweight': 'bold', 'color': 'black'}
)

for text in ax.texts:
    text.set_fontweight('bold')
    text.set_fontsize(7)
    text.set_color('black')
    text.set_bbox(dict(boxstyle='round,pad=0.1', facecolor='white', alpha=0.85, edgecolor='none'))

ax.set_title(f'Average Hourly Log Returns Heatmap\n{TIMEFRAME} bars, {DAYS_BACK}-day lookback', 
             fontsize=16, fontweight='bold', pad=20, color='white')
ax.set_xlabel('Hour (UTC)', fontsize=14, color='white')
ax.set_ylabel('Cryptocurrency', fontsize=14, color='white')

cbar = ax.collections[0].colorbar
cbar.ax.yaxis.label.set_color('white')
cbar.ax.tick_params(colors='white')

plt.xticks(rotation=45, ha='right', color='white', fontsize=11)
plt.yticks(rotation=0, color='white', fontsize=11)

plt.tight_layout()
plt.show()

# %%
fig, axes = plt.subplots(1, 2, figsize=(18, 6))
fig.patch.set_facecolor('#1e1e1e')

ax1 = axes[0]
ax1.set_facecolor('#1e1e1e')
avg_returns_matrix = avg_returns_by_hour.values.reshape(1, -1)

from matplotlib.colors import LinearSegmentedColormap
colors_list = ['#8B0000', '#CD5C5C', '#F5F5F5', '#90EE90', '#006400']
cmap = LinearSegmentedColormap.from_list('red_green', colors_list, N=256)

annot_labels_avg = pd.DataFrame(avg_returns_matrix).applymap(lambda x: f'{x:.3f}')

hm1 = sns.heatmap(
    avg_returns_matrix,
    cmap=cmap,
    center=0,
    annot=annot_labels_avg,
    fmt='',
    linewidths=1,
    linecolor='#1e1e1e',
    xticklabels=time_buckets,
    yticklabels=['Avg Return'],
    cbar_kws={'label': 'Return (%)', 'shrink': 0.5},
    ax=ax1,
    annot_kws={'fontsize': 7, 'fontweight': 'bold', 'color': 'black'}
)

for text in ax1.texts:
    text.set_fontweight('bold')
    text.set_fontsize(7)
    text.set_color('black')
    text.set_bbox(dict(boxstyle='round,pad=0.1', facecolor='white', alpha=0.85, edgecolor='none'))

ax1.set_title(f'Average Returns by Hour (All Cryptos)\n{TIMEFRAME} bars, {DAYS_BACK}-day lookback', 
              fontsize=12, fontweight='bold', color='white')
ax1.set_xlabel('Hour (UTC)', color='white')
cbar1 = ax1.collections[0].colorbar
cbar1.ax.yaxis.label.set_color('white')
cbar1.ax.tick_params(colors='white')
plt.sca(ax1)
plt.xticks(rotation=45, ha='right', color='white')
plt.yticks(color='white')

ax2 = axes[1]
ax2.set_facecolor('#1e1e1e')
colors = ['#006400' if x > 0 else '#8B0000' for x in avg_returns_by_hour.values]
ax2.bar(range(len(avg_returns_by_hour)), avg_returns_by_hour.values, color=colors, alpha=0.9, edgecolor='white', linewidth=0.5)
ax2.axhline(y=0, color='white', linestyle='-', linewidth=0.5)
ax2.set_xticks(range(len(time_buckets)))
ax2.set_xticklabels(time_buckets, rotation=45, ha='right', color='white')
ax2.set_xlabel('Hour (UTC)', color='white')
ax2.set_ylabel('Average Log Return (%)', color='white')
ax2.set_title(f'Average Hourly Returns Bar Chart\n{TIMEFRAME} bars, {DAYS_BACK}-day lookback', 
              fontsize=12, fontweight='bold', color='white')
ax2.grid(axis='y', alpha=0.3, color='gray')
ax2.tick_params(colors='white')
ax2.spines['bottom'].set_color('white')
ax2.spines['top'].set_color('#1e1e1e')
ax2.spines['left'].set_color('white')
ax2.spines['right'].set_color('#1e1e1e')

plt.tight_layout()
plt.show()

# %% [markdown]
# ## Statistical Summary
# 
# Key statistics about the hourly return patterns:

# %%
# Summary statistics
print("="*60)
print("HOURLY RETURNS SUMMARY STATISTICS")
print("="*60)

# Best and worst hours
best_hour = avg_returns_by_hour.idxmax()
worst_hour = avg_returns_by_hour.idxmin()

print(f"\n📈 Best Hour:  {best_hour} with {avg_returns_by_hour[best_hour]:+.4f}% avg return")
print(f"📉 Worst Hour: {worst_hour} with {avg_returns_by_hour[worst_hour]:+.4f}% avg return")

# Hours with positive vs negative returns
positive_hours = (avg_returns_by_hour > 0).sum()
negative_hours = (avg_returns_by_hour < 0).sum()

print(f"\n🟢 Hours with positive avg return: {positive_hours}/{len(avg_returns_by_hour)}")
print(f"🔴 Hours with negative avg return: {negative_hours}/{len(avg_returns_by_hour)}")

# Per-symbol statistics
print(f"\n" + "="*60)
print("PER-SYMBOL STATISTICS")
print("="*60)

for symbol in returns_df_pct.columns:
    symbol_returns = returns_df_pct[symbol]
    best = symbol_returns.idxmax()
    worst = symbol_returns.idxmin()
    print(f"\n{symbol}:")
    print(f"  Best hour:  {best} ({symbol_returns[best]:+.4f}%)")
    print(f"  Worst hour: {worst} ({symbol_returns[worst]:+.4f}%)")
    print(f"  Avg return: {symbol_returns.mean():+.4f}%")

# %%
# Create a ranking of best/worst hours
print("\n" + "="*60)
print("HOUR RANKINGS (Best to Worst)")
print("="*60)

ranked_hours = avg_returns_by_hour.sort_values(ascending=False)

for i, (hour, ret) in enumerate(ranked_hours.items(), 1):
    emoji = "🟢" if ret > 0 else "🔴" if ret < 0 else "⚪"
    print(f"{i:2d}. {hour}: {ret:+.4f}% {emoji}")

