# %% [markdown]
# # Central Bank Balance Sheet Comparison - Animated Line Chart Race
# 
# This notebook creates an animated line chart comparing central bank balance sheet data from the Federal Reserve Economic Data (FRED) database.

# %%
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

try:
    from fredapi import Fred
    FRED_AVAILABLE = True
except ImportError:
    FRED_AVAILABLE = False
    print("fredapi not installed. Install with: pip install fredapi")

# %% [markdown]
# ## Fetch Data from FRED
# 
# We'll retrieve:
# - **WALCL**: Federal Reserve Total Assets (Millions USD)
# - **ECBASSETSW**: ECB Total Assets (Millions EUR)
# - **JPNASSETS**: Bank of Japan Total Assets (100 Million JPY)
# 
# Plus exchange rates for currency conversion to Trillions USD.

# %%
import os

# Get a free FRED API key at: https://fredaccount.stlouisfed.org/apikeys
# Set FRED_API_KEY env var or use the default key below
FRED_API_KEY = os.environ.get('FRED_API_KEY', '976a964605bdb8bed09739ba9b4d8511')

if FRED_AVAILABLE and FRED_API_KEY != 'your_api_key_here':
    try:
        fred = Fred(api_key=FRED_API_KEY)

        fed = fred.get_series('WALCL', observation_start='2003-01-01')
        ecb = fred.get_series('ECBASSETSW', observation_start='2003-01-01')
        boj = fred.get_series('JPNASSETS', observation_start='2003-01-01')

        eur_usd = fred.get_series('DEXUSEU', observation_start='2003-01-01')
        jpy_usd = fred.get_series('DEXJPUS', observation_start='2003-01-01')

        fed = fed.resample('M').last()
        ecb = ecb.resample('M').last()
        boj = boj.resample('M').last()
        eur_usd = eur_usd.resample('M').last()
        jpy_usd = jpy_usd.resample('M').last()

        # WALCL is in Millions USD -> divide by 1,000,000 for Trillions
        # ECBASSETSW is in Millions EUR -> multiply by EUR/USD rate, divide by 1,000,000 for Trillions
        # JPNASSETS is in 100 Million JPY -> multiply by 100 to get Million JPY, divide by JPY/USD rate, divide by 1,000,000 for Trillions
        df_usd = pd.DataFrame({
            'Federal Reserve': fed / 1_000_000,
            'ECB': (ecb * eur_usd) / 1_000_000,
            'Bank of Japan': (boj * 100) / (jpy_usd * 1_000_000)
        }).dropna()

        print("Data successfully fetched from FRED!")
        print(f"Date range: {df_usd.index.min()} to {df_usd.index.max()}")
        print(f"\nUnit check (latest values in Trillions USD):")
        print(f"  Federal Reserve: ${df_usd['Federal Reserve'].iloc[-1]:.2f}T")
        print(f"  ECB: ${df_usd['ECB'].iloc[-1]:.2f}T")
        print(f"  Bank of Japan: ${df_usd['Bank of Japan'].iloc[-1]:.2f}T")

    except Exception as e:
        print(f"Error fetching from FRED: {e}")
        FRED_AVAILABLE = False

if not FRED_AVAILABLE or FRED_API_KEY == 'your_api_key_here':
    print("Using sample data (to use real data, add your FRED API key)")
    dates = pd.date_range('2003-01-01', '2024-01-01', freq='M')
    np.random.seed(42)

    fed_base = np.concatenate([
        np.linspace(0.7, 0.9, 60),
        np.linspace(0.9, 2.3, 24),
        np.linspace(2.3, 2.8, 48),
        np.linspace(2.8, 4.2, 12),
        np.linspace(4.2, 8.9, 24),
        np.linspace(8.9, 7.5, len(dates) - 168)
    ])

    ecb_base = np.concatenate([
        np.linspace(0.9, 1.5, 60),
        np.linspace(1.5, 2.8, 24),
        np.linspace(2.8, 3.2, 48),
        np.linspace(3.2, 4.5, 12),
        np.linspace(4.5, 9.0, 24),
        np.linspace(9.0, 7.0, len(dates) - 168)
    ])

    boj_base = np.concatenate([
        np.linspace(1.0, 1.1, 60),
        np.linspace(1.1, 1.3, 24),
        np.linspace(1.3, 2.5, 48),
        np.linspace(2.5, 3.5, 12),
        np.linspace(3.5, 5.5, 24),
        np.linspace(5.5, 4.5, len(dates) - 168)
    ])

    df_usd = pd.DataFrame({
        'Federal Reserve': fed_base * (1 + 0.02 * np.random.randn(len(dates))),
        'ECB': ecb_base * (1 + 0.02 * np.random.randn(len(dates))),
        'Bank of Japan': boj_base * (1 + 0.02 * np.random.randn(len(dates)))
    }, index=dates)

print(f"\nDataset shape: {df_usd.shape}")
df_usd.head(10)

# %% [markdown]
# ## Prepare Data for Animation
# 
# We'll normalize each central bank's balance sheet to start at 100 (index = 100 at first observation) so we can compare relative growth rates across institutions with different absolute sizes.

# %%
df_normalized = df_usd.copy()
for col in df_normalized.columns:
    df_normalized[col] = (df_normalized[col] / df_normalized[col].iloc[0]) * 100

print("Normalized data (Index = 100 at start):")
print(f"Starting values: {df_normalized.iloc[0].to_dict()}")
print(f"Ending values: {df_normalized.iloc[-1].round(1).to_dict()}")

df_long = df_normalized.reset_index().melt(
    id_vars='index',
    var_name='Central Bank',
    value_name='Index (100 = Start)'
)
df_long = df_long.rename(columns={'index': 'Date'})
df_long['Year_Month'] = df_long['Date'].dt.to_period('M').astype(str)

df_long.tail(10)

# %% [markdown]
# ## Create Animated Line Chart Race

# %%
color_map = {'Federal Reserve': '#4fc3f7', 'ECB': '#ffb74d', 'Bank of Japan': '#81c784'}

fig = go.Figure()

for col in df_normalized.columns:
    fig.add_trace(go.Scatter(
        x=[df_normalized.index[0]],
        y=[df_normalized[col].iloc[0]],
        mode='lines',
        name=col,
        line=dict(width=3, color=color_map[col])
    ))

frames = []
dates = df_normalized.index[::3]

for date in dates:
    frame_data = []
    for col in df_normalized.columns:
        df_subset = df_normalized.loc[:date]
        frame_data.append(
            go.Scatter(
                x=df_subset.index,
                y=df_subset[col],
                mode='lines',
                name=col,
                line=dict(width=3, color=color_map[col])
            )
        )
    frames.append(go.Frame(data=frame_data, name=date.strftime('%Y-%m')))

fig.frames = frames

fig.update_layout(
    title='<b>Central Bank Balance Sheet Growth Race</b><br><sup>Normalized Index (100 = Starting Value) | Data: FRED</sup>',
    font_family='Arial',
    font_color='#e0e0e0',
    title_font_size=20,
    title_font_color='#ffffff',
    paper_bgcolor='#1e1e1e',
    plot_bgcolor='#1e1e1e',
    xaxis=dict(
        title='Date',
        range=[df_normalized.index.min(), df_normalized.index.max()],
        gridcolor='#3a3a3a',
        linecolor='#3a3a3a',
        tickfont=dict(color='#b0b0b0'),
        title_font=dict(color='#e0e0e0')
    ),
    yaxis=dict(
        title='Index (100 = Start)',
        range=[0, df_normalized.max().max() * 1.1],
        gridcolor='#3a3a3a',
        linecolor='#3a3a3a',
        tickfont=dict(color='#b0b0b0'),
        title_font=dict(color='#e0e0e0')
    ),
    legend=dict(
        yanchor="top", y=0.99, xanchor="left", x=0.01,
        bgcolor='rgba(30,30,30,0.9)',
        bordercolor='#3a3a3a',
        borderwidth=1,
        font=dict(color='#e0e0e0')
    ),
    hovermode='x unified',
    updatemenus=[dict(
        type='buttons',
        showactive=False,
        y=1.15,
        x=0.5,
        xanchor='center',
        bgcolor='#2d2d2d',
        bordercolor='#4a4a4a',
        font=dict(color='#e0e0e0'),
        buttons=[
            dict(label='▶ Play', method='animate',
                 args=[None, {'frame': {'duration': 100, 'redraw': True}, 'fromcurrent': True, 'transition': {'duration': 50}}]),
            dict(label='⏸ Pause', method='animate',
                 args=[[None], {'frame': {'duration': 0, 'redraw': False}, 'mode': 'immediate', 'transition': {'duration': 0}}])
        ]
    )],
    sliders=[dict(
        active=0,
        currentvalue=dict(prefix='Date: ', font=dict(size=14, color='#e0e0e0')),
        pad=dict(t=50),
        bgcolor='#2d2d2d',
        bordercolor='#4a4a4a',
        tickcolor='#4a4a4a',
        font=dict(color='#b0b0b0'),
        steps=[dict(args=[[f.name], dict(frame=dict(duration=100, redraw=True), mode='immediate')],
                   method='animate', label=f.name) for f in frames]
    )]
)

fig.show()

# %%
fig2 = go.Figure()

for col in df_normalized.columns:
    fig2.add_trace(go.Scatter(
        x=df_normalized.index,
        y=df_normalized[col],
        name=col,
        line=dict(color=color_map[col], width=3),
        hovertemplate='%{x|%Y-%m}<br>' + col + ': %{y:.1f}<extra></extra>'
    ))

fig2.update_layout(
    title='<b>Central Bank Balance Sheet Growth (Normalized)</b><br><sup>Index = 100 at Start | Data: FRED</sup>',
    title_font_size=20,
    font_family='Arial',
    xaxis_title='Date',
    yaxis_title='Index (100 = Start)',
    hovermode='x unified',
    legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
)

fig2.show()

# %% [markdown]
# ## Summary Statistics

# %%
print("=" * 60)
print("SUMMARY STATISTICS")
print("=" * 60)

for col in df_usd.columns:
    growth = ((df_usd[col].iloc[-1] / df_usd[col].iloc[0]) - 1) * 100
    print(f"\n📈 {col}:")
    print(f"   Starting Value: ${df_usd[col].iloc[0]:.2f}T")
    print(f"   Ending Value: ${df_usd[col].iloc[-1]:.2f}T")
    print(f"   Peak Value: ${df_usd[col].max():.2f}T (on {df_usd[col].idxmax().strftime('%Y-%m')})")
    print(f"   Total Growth: {growth:.1f}% (Index: {df_normalized[col].iloc[-1]:.1f})")

print(f"\n💡 Combined Total (Latest): ${df_usd.iloc[-1].sum():.2f}T")
print("=" * 60)

# %% [markdown]
# ## Export Data to CSV

# %%
df_export = df_usd.copy()
df_export.index.name = 'Date'

for col in df_usd.columns:
    df_export[f'{col} (Index)'] = (df_usd[col] / df_usd[col].iloc[0]) * 100

df_export['Total (All Banks)'] = df_usd.sum(axis=1)
df_export = df_export.round(4)

output_filename = 'central_bank_balance_sheets_usd.csv'
df_export.to_csv(output_filename)

print(f"✓ Data exported to '{output_filename}'")
print(f"  - {len(df_export)} rows (monthly observations)")
print(f"  - {len(df_export.columns)} columns")
print(f"  - Date range: {df_export.index.min().strftime('%Y-%m-%d')} to {df_export.index.max().strftime('%Y-%m-%d')}")
print(f"\nColumns: {list(df_export.columns)}")

print("\nFirst 5 rows:")
df_export.head()

# %% [markdown]
# ## Summary
# 
# This notebook:
# 1. ✅ Fetched monthly central bank balance sheet data from FRED (2003-present)
# 2. ✅ Converted all values to USD using exchange rates
# 3. ✅ **Normalized data to Index=100 at start for fair comparison**
# 4. ✅ Created static and animated visualizations showing relative growth
# 5. ✅ Exported data to CSV with both absolute values (Trillions USD) and normalized index values

