# %% [markdown]
# Economic Data Analysis: A Comprehensive Story from FRED
# 
# This notebook fetches real-time economic data from the Federal Reserve Economic Data (FRED) API to create a coherent narrative about the current state of the U.S. economy. We'll explore relationships between key economic indicators including monetary policy, inflation, labor markets, and housing.

# %%
# Install required packages using: pip install pandas numpy matplotlib seaborn fredapi plotly requests datetime

# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from fredapi import Fred
import warnings
from datetime import datetime

warnings.filterwarnings('ignore')
plt.style.use('dark_background')
sns.set_palette("husl")

import os

# Get a free FRED API key at: https://fredaccount.stlouisfed.org/apikeys
# Set FRED_API_KEY env var or replace the default below
fred = Fred(api_key=os.environ.get('FRED_API_KEY', 'your_api_key_here'))

# %%
# Fetch key economic indicators from FRED
start_date = '2010-01-01'
end_date = datetime.now().strftime('%Y-%m-%d')

try:
    # Monetary Policy & Interest Rates
    fed_funds = fred.get_series('FEDFUNDS', start=start_date, end=end_date)
    treasury_10y = fred.get_series('GS10', start=start_date, end=end_date)
    mortgage_30y = fred.get_series('MORTGAGE30US', start=start_date, end=end_date)
    
    # Inflation & Prices
    cpi = fred.get_series('CPIAUCSL', start=start_date, end=end_date)
    core_cpi = fred.get_series('CPILFESL', start=start_date, end=end_date)
    
    # Labor Market
    unemployment = fred.get_series('UNRATE', start=start_date, end=end_date)
    payrolls = fred.get_series('PAYEMS', start=start_date, end=end_date)
    
    # Housing Market
    house_prices = fred.get_series('CSUSHPISA', start=start_date, end=end_date)
    housing_starts = fred.get_series('HOUST', start=start_date, end=end_date)
    
    print("Successfully fetched data from FRED API")
    print(f"Data range: {start_date} to {end_date}")
    
except Exception as e:
    print(f"Error fetching from FRED: {e}")
    print("Using synthetic data for demonstration")
    
    dates = pd.date_range(start=start_date, end=end_date, freq='M')
    np.random.seed(42)
    
    fed_funds = pd.Series(np.random.uniform(0.1, 5.5, len(dates)), index=dates)
    treasury_10y = pd.Series(fed_funds + np.random.uniform(0.5, 2.0, len(dates)), index=dates)
    mortgage_30y = pd.Series(treasury_10y + np.random.uniform(0.5, 1.5, len(dates)), index=dates)
    unemployment = pd.Series(np.random.uniform(3.5, 14.7, len(dates)), index=dates)
    cpi = pd.Series(np.cumprod(1 + np.random.normal(0.002, 0.003, len(dates))) * 100, index=dates)
    core_cpi = pd.Series(np.cumprod(1 + np.random.normal(0.0018, 0.002, len(dates))) * 100, index=dates)
    payrolls = pd.Series(np.random.uniform(130000, 155000, len(dates)), index=dates)
    house_prices = pd.Series(np.cumprod(1 + np.random.normal(0.003, 0.01, len(dates))) * 100, index=dates)
    housing_starts = pd.Series(np.random.uniform(500, 1700, len(dates)), index=dates)

# %%
# Data cleaning and preprocessing
def clean_and_resample(series, freq='M'):
    """Clean data by removing outliers and resampling to monthly frequency"""
    series = series.dropna()
    if len(series) > 0:
        Q1 = series.quantile(0.25)
        Q3 = series.quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        series = series[(series >= lower_bound) & (series <= upper_bound)]
        
        if freq == 'M' and not series.empty:
            series = series.resample('M').last()
    
    return series

# Clean all series
fed_funds_clean = clean_and_resample(fed_funds)
treasury_10y_clean = clean_and_resample(treasury_10y)
mortgage_30y_clean = clean_and_resample(mortgage_30y)
unemployment_clean = clean_and_resample(unemployment)
cpi_clean = clean_and_resample(cpi)
core_cpi_clean = clean_and_resample(core_cpi)
payrolls_clean = clean_and_resample(payrolls)
house_prices_clean = clean_and_resample(house_prices)
housing_starts_clean = clean_and_resample(housing_starts)

# Calculate year-over-year inflation rates
cpi_yoy = cpi_clean.pct_change(12) * 100
core_cpi_yoy = core_cpi_clean.pct_change(12) * 100

print("Data cleaning completed successfully")
print(f"Sample data points: Fed Funds Rate: {len(fed_funds_clean)}, Unemployment: {len(unemployment_clean)}")

# %%
fig, axes = plt.subplots(4, 1, figsize=(16, 20))
fig.patch.set_facecolor('#0a0e1a')

colors = {
    'primary': '#00d4ff',
    'secondary': '#ff6b35', 
    'accent': '#7b68ee',
    'success': '#00ff88',
    'warning': '#ffd700',
    'danger': '#ff4757',
    'neutral': '#a4b0be'
}

def style_axis(ax, title, ylabel, ylabel_color='white'):
    ax.set_title(title, fontsize=18, fontweight='bold', color='white', pad=25)
    ax.set_ylabel(ylabel, fontsize=14, color=ylabel_color, fontweight='600')
    ax.tick_params(colors='white', labelsize=12)
    ax.grid(True, alpha=0.2, color='white', linestyle='-', linewidth=0.5)
    ax.set_facecolor('#0f1419')
    for spine_name in ['bottom', 'left']:
        ax.spines[spine_name].set_color('white')
    for spine_name in ['top', 'right']:
        ax.spines[spine_name].set_visible(False)

# Plot 1: Interest Rate Environment
ax1 = axes[0]
ax1.plot(fed_funds_clean.index, fed_funds_clean.values, label='Fed Funds Rate', 
         linewidth=3, color=colors['danger'], alpha=0.9)
ax1.plot(treasury_10y_clean.index, treasury_10y_clean.values, label='10-Year Treasury', 
         linewidth=3, color=colors['primary'], alpha=0.9)
ax1.plot(mortgage_30y_clean.index, mortgage_30y_clean.values, label='30-Year Mortgage', 
         linewidth=3, color=colors['warning'], alpha=0.9)
ax1.legend(loc='upper right', frameon=False, fontsize=12)
style_axis(ax1, 'Interest Rates', 'Rate (%)')

# Plot 2: Inflation Dynamics
ax2 = axes[1]
ax2.plot(cpi_yoy.index, cpi_yoy.values, label='CPI Inflation', 
         linewidth=3, color=colors['secondary'], alpha=0.9)
ax2.plot(core_cpi_yoy.index, core_cpi_yoy.values, label='Core CPI', 
         linewidth=3, color=colors['accent'], alpha=0.9)
ax2.axhline(y=2.0, color=colors['danger'], linestyle='--', alpha=0.8, 
           linewidth=2, label='Fed Target (2%)')
ax2.legend(loc='upper right', frameon=False, fontsize=12)
style_axis(ax2, 'Inflation Trends', 'YoY Change (%)')

# Plot 3: Labor Market
ax3 = axes[2]
ax3_twin = ax3.twinx()

line1 = ax3.plot(unemployment_clean.index, unemployment_clean.values, 
                label='Unemployment Rate', linewidth=3, color=colors['danger'], alpha=0.9)
line2 = ax3_twin.plot(payrolls_clean.index, payrolls_clean.values/1000, 
                     label='Payrolls (Millions)', linewidth=3, color=colors['success'], alpha=0.9)

ax3_twin.set_ylabel('Payrolls (M)', fontsize=14, color=colors['success'], fontweight='600')
ax3_twin.tick_params(colors='white', labelsize=12)
ax3_twin.set_facecolor('#0f1419')
ax3_twin.spines['right'].set_color('white')
ax3_twin.spines['top'].set_visible(False)

lines = line1 + line2
labels = [l.get_label() for l in lines]
ax3.legend(lines, labels, loc='upper right', frameon=False, fontsize=12)
style_axis(ax3, 'Labor Market', 'Unemployment (%)', colors['danger'])

# Plot 4: Housing Market
ax4 = axes[3]
ax4_twin = ax4.twinx()

line3 = ax4.plot(house_prices_clean.index, house_prices_clean.values, 
                label='House Price Index', linewidth=3, color=colors['warning'], alpha=0.9)
line4 = ax4_twin.plot(housing_starts_clean.index, housing_starts_clean.values, 
                     label='Housing Starts (K)', linewidth=3, color=colors['primary'], alpha=0.9)

ax4_twin.set_ylabel('Starts (K)', fontsize=14, color=colors['primary'], fontweight='600')
ax4_twin.tick_params(colors='white', labelsize=12)
ax4_twin.set_facecolor('#0f1419')
ax4_twin.spines['right'].set_color('white')
ax4_twin.spines['top'].set_visible(False)

lines2 = line3 + line4
labels2 = [l.get_label() for l in lines2]
ax4.legend(lines2, labels2, loc='upper left', frameon=False, fontsize=12)
style_axis(ax4, 'Housing Market', 'Price Index', colors['warning'])

plt.tight_layout(pad=3.0)
plt.show()

# %%
# Create correlation analysis and heatmap
recent_data = pd.DataFrame({
    'Fed_Funds': fed_funds_clean,
    'Treasury_10Y': treasury_10y_clean,
    'Mortgage_30Y': mortgage_30y_clean,
    'Unemployment': unemployment_clean,
    'CPI_YoY': cpi_yoy,
    'Core_CPI_YoY': core_cpi_yoy,
    'House_Prices': house_prices_clean.pct_change(12) * 100,
    'Housing_Starts': housing_starts_clean
}).dropna()

correlation_matrix = recent_data.corr()

plt.figure(figsize=(12, 10))
plt.gca().set_facecolor('#1E1E1E')
plt.gcf().patch.set_facecolor('#0E1117')

mask = np.triu(np.ones_like(correlation_matrix, dtype=bool))
heatmap = sns.heatmap(correlation_matrix, mask=mask, annot=True, cmap='RdYlBu_r', center=0,
                     square=True, linewidths=0.5, cbar_kws={"shrink": 0.8}, fmt='.2f',
                     annot_kws={'color': 'white', 'fontsize': 10})

plt.title('Economic Indicators Correlation Matrix\nUnderstanding Interconnected Relationships', 
          fontsize=16, fontweight='bold', color='white', pad=20)
plt.xticks(rotation=45, ha='right', color='white')
plt.yticks(rotation=0, color='white')

cbar = heatmap.collections[0].colorbar
cbar.ax.tick_params(colors='white')
cbar.ax.yaxis.label.set_color('white')

plt.tight_layout()
plt.show()

# %%
# Calculate and display key economic insights
latest_data = {
    'Fed Funds Rate': fed_funds_clean.iloc[-1] if len(fed_funds_clean) > 0 else 0,
    'Unemployment Rate': unemployment_clean.iloc[-1] if len(unemployment_clean) > 0 else 0,
    'CPI Inflation (YoY)': cpi_yoy.iloc[-1] if len(cpi_yoy) > 0 else 0,
    'Core CPI Inflation (YoY)': core_cpi_yoy.iloc[-1] if len(core_cpi_yoy) > 0 else 0,
    '10-Year Treasury': treasury_10y_clean.iloc[-1] if len(treasury_10y_clean) > 0 else 0,
    '30-Year Mortgage': mortgage_30y_clean.iloc[-1] if len(mortgage_30y_clean) > 0 else 0
}

# Calculate recent trends (6-month change)
trends = {}
for key, series in [('Fed Funds', fed_funds_clean), ('Unemployment', unemployment_clean), 
                   ('CPI Inflation', cpi_yoy), ('Treasury 10Y', treasury_10y_clean)]:
    if len(series) >= 6:
        recent_change = series.iloc[-1] - series.iloc[-6]
        trends[key] = recent_change

print("=== CURRENT ECONOMIC SNAPSHOT ===")
print(f"Data as of: {end_date}")
print("\nKey Indicators:")
for indicator, value in latest_data.items():
    print(f"{indicator}: {value:.2f}%")

print("\n6-Month Trends:")
for indicator, change in trends.items():
    direction = "↑" if change > 0 else "↓" if change < 0 else "→"
    print(f"{indicator}: {change:+.2f}pp {direction}")

# Economic regime analysis
if latest_data['CPI Inflation (YoY)'] > 3.0:
    inflation_regime = "High Inflation Environment"
elif latest_data['CPI Inflation (YoY)'] < 1.0:
    inflation_regime = "Low Inflation/Deflationary Pressures"
else:
    inflation_regime = "Moderate Inflation"

if latest_data['Unemployment Rate'] < 4.0:
    labor_regime = "Tight Labor Market"
elif latest_data['Unemployment Rate'] > 7.0:
    labor_regime = "Loose Labor Market"
else:
    labor_regime = "Balanced Labor Market"

print(f"\nEconomic Regime Analysis:")
print(f"Inflation Environment: {inflation_regime}")
print(f"Labor Market Condition: {labor_regime}")

# %% [markdown]
# ## Key Economic Insights and Story
# 
# **The Current Economic Narrative:**
# 
# 1. **Monetary Policy Transmission**: The visualizations reveal how Federal Reserve policy decisions flow through the economy via interest rate channels, affecting everything from mortgage rates to business investment.
# 
# 2. **Inflation Dynamics**: The relationship between headline and core inflation shows underlying price pressures, with core CPI providing a cleaner signal of persistent inflation trends that guide Fed policy.
# 
# 3. **Labor Market Strength**: The inverse relationship between unemployment and job creation demonstrates the health of the labor market, which directly impacts consumer spending and economic growth.
# 
# 4. **Housing Market Interconnections**: Housing prices and construction activity reflect both interest rate sensitivity and broader economic confidence, serving as a key transmission mechanism for monetary policy.
# 
# 5. **Economic Correlations**: The correlation matrix reveals how tightly interconnected these economic variables are, showing that policy changes in one area ripple throughout the entire economic system.
# 
# This comprehensive analysis using real FRED data provides a data-driven foundation for understanding current economic conditions and potential future trends.

