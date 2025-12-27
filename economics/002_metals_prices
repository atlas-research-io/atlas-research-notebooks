# %% [markdown]
# # Precious Metals Performance Analysis
# 
# Fetching and visualizing performance since **October 1st, 2024** for:
# - **Gold (GC=F)**
# - **Silver (SI=F)**
# - **Platinum (PL=F)**
# - **Palladium (PA=F)**
# - **Copper (HG=F)** — industrial metal often grouped with precious metals
# 
# All prices normalized to 100 at the starting point for easy comparison.

# %%
# Install yfinance if needed
%pip install yfinance -q

# %%
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

start_date = datetime(2024, 10, 1)
end_date = datetime.now()

print(f"Fetching data from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")

# %%
# Define the precious metals tickers
tickers = {
    'Gold': 'GC=F',
    'Silver': 'SI=F',
    'Platinum': 'PL=F',
    'Palladium': 'PA=F',
    'Copper': 'HG=F'
}

# Fetch daily closing prices
prices = pd.DataFrame()

for name, ticker in tickers.items():
    try:
        data = yf.download(ticker, start=start_date, end=end_date, progress=False)
        if not data.empty:
            # Handle multi-level columns if present
            if isinstance(data.columns, pd.MultiIndex):
                prices[name] = data['Close'][ticker]
            else:
                prices[name] = data['Close']
            print(f"✓ {name}: {len(data)} days of data")
        else:
            print(f"✗ {name}: No data available")
    except Exception as e:
        print(f"✗ {name}: Error - {e}")

print(f"\nTotal trading days: {len(prices)}")
prices.head()

# %%
# Normalize all prices to start at 100 (percent change from starting point)
normalized = (prices / prices.iloc[0]) * 100

# Calculate total returns
returns = ((prices.iloc[-1] / prices.iloc[0]) - 1) * 100
returns_sorted = returns.sort_values(ascending=False)

print("12-Month Returns (%):\n")
for metal, ret in returns_sorted.items():
    emoji = "🟢" if ret > 0 else "🔴"
    print(f"{emoji} {metal}: {ret:+.1f}%")

# %%
import matplotlib.dates as mdates

fig, ax = plt.subplots(figsize=(18, 10), dpi=100)
fig.patch.set_facecolor('#1e1e1e')
ax.set_facecolor('#1e1e1e')

colors = {
    'Gold': '#FFD700',
    'Silver': '#87CEEB',
    'Platinum': '#E8E8E8',
    'Palladium': '#00FF7F',
    'Copper': '#FF6347'
}

for metal in normalized.columns:
    ax.plot(normalized.index, normalized[metal], 
            color=colors.get(metal, '#FFFFFF'),
            linewidth=1.5, alpha=0.25)
    ax.plot(normalized.index, normalized[metal], 
            label=f"{metal} ({returns[metal]:+.1f}%)",
            color=colors.get(metal, '#FFFFFF'),
            linewidth=2.5,
            alpha=1.0)

ax.axhline(y=100, color='#888888', linestyle='--', alpha=0.8, linewidth=1.5)

events = [
    ('2024-11-05', 'US Election', 'normal'),
    ('2024-12-18', 'Fed -25bps', 'normal'),
    ('2025-01-20', 'Inauguration', 'normal'),
    ('2025-02-01', 'Tariffs', 'tariff'),
    ('2025-02-04', 'China retaliates', 'normal'),
    ('2025-03-04', 'CA/MX tariffs', 'tariff'),
    ('2025-03-12', 'Steel/Al 25%', 'tariff'),
    ('2025-04-02', 'Liberation Day', 'tariff'),
    ('2025-04-09', '90-day pause', 'normal'),
    ('2025-08-01', 'Copper 50%', 'tariff'),
]

y_min = normalized.min().min()
y_max = normalized.max().max()
y_range = y_max - y_min

height_levels_top = [0.12, 0.22, 0.32]
height_levels_bottom = [0.12, 0.22, 0.32]

for i, (date_str, event_text, event_type) in enumerate(events):
    try:
        event_date = pd.to_datetime(date_str)
        if event_date >= normalized.index.min() and event_date <= normalized.index.max():
            is_top = (i % 2 == 0)
            level_idx = (i // 2) % 3

            if is_top:
                y_pos = y_max + (y_range * height_levels_top[level_idx])
                va = 'bottom'
            else:
                y_pos = y_min - (y_range * height_levels_bottom[level_idx])
                va = 'top'

            if event_type == 'tariff':
                ax.axvline(x=event_date, color='#FF4444', linestyle='-', alpha=0.6, linewidth=1.5)
                ax.annotate(event_text, 
                           xy=(event_date, y_pos),
                           fontsize=11,
                           fontweight='bold',
                           color='#FFFFFF',
                           ha='center',
                           va=va,
                           rotation=0,
                           bbox=dict(boxstyle='round,pad=0.4', facecolor='#CC0000', 
                                    edgecolor='#FF6666', alpha=0.9, linewidth=1.5))
            else:
                ax.axvline(x=event_date, color='#00BFFF', linestyle='--', alpha=0.7, linewidth=1.5)
                ax.annotate(event_text, 
                           xy=(event_date, y_pos),
                           fontsize=10,
                           color='#EEEEEE',
                           ha='center',
                           va=va,
                           rotation=0,
                           bbox=dict(boxstyle='round,pad=0.35', facecolor='#1a5276', 
                                    edgecolor='#5dade2', alpha=0.9, linewidth=1.5))
    except:
        pass

ax.set_ylim(y_min - (y_range * 0.4), y_max + (y_range * 0.4))

ax.set_title('Precious Metals Performance (Oct 2024 - Present)', 
             fontsize=26, fontweight='bold', pad=25, color='white')
ax.set_xlabel('')
ax.set_ylabel('Normalized Price (Start = 100)', fontsize=14, color='#DDDDDD', fontweight='bold')

legend = ax.legend(loc='lower right', fontsize=14, framealpha=0.95, 
                   edgecolor='#666666', fancybox=True,
                   facecolor='#2a2a2a', labelcolor='white',
                   borderpad=1.2, handlelength=3, handleheight=1.5)
legend.get_frame().set_linewidth(2)

ax.grid(True, alpha=0.4, linestyle='-', linewidth=0.8, color='#555555')
ax.grid(True, which='minor', alpha=0.2, linestyle='-', linewidth=0.4, color='#444444')
ax.minorticks_on()

for spine in ax.spines.values():
    spine.set_color('#666666')
    spine.set_linewidth(1.5)

ax.tick_params(colors='#DDDDDD', which='both', labelsize=11)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
ax.xaxis.set_major_locator(mdates.AutoDateLocator())

plt.tight_layout()
plt.savefig('precious_metals_performance.png', dpi=150, bbox_inches='tight', 
            facecolor='#1e1e1e', edgecolor='none')
plt.show()

print("\n✓ Chart saved as 'precious_metals_performance.png'")

# %% [markdown]
# 

# %%
top_performer = returns_sorted.index[0]
top_return = returns_sorted.iloc[0]
bottom_performer = returns_sorted.index[-1]
bottom_return = returns_sorted.iloc[-1]

print("="*60)
print("PERFORMANCE ANALYSIS (Oct 2024 - Present)")
print("="*60)

analysis = f"""
Since October 1st, 2024, {top_performer} has been the standout performer 
with a {top_return:+.1f}% gain, while {bottom_performer} lagged at {bottom_return:+.1f}%. 

How These Events Affected Precious Metals:

• Tariff uncertainty → Safe haven demand for gold/silver
• Fed rate cuts → Lower opportunity cost of holding non-yielding metals
• Dollar weakness → Makes dollar-denominated commodities cheaper globally
• Central bank buying → Record gold purchases as reserves diversification
• "Debasement trade" → Concerns about fiscal/monetary policy excess
• Silver industrial demand → Fifth consecutive year of supply deficits

Key events driving precious metals:
• US Election - Trump wins (Nov 5) - policy uncertainty drives safe-haven demand
• Fed rate cut 25bps (Dec 18) - monetary policy easing supports metals
• Trump inauguration (Jan 20) - "America First" agenda uncertainty
• Tariffs announced (Feb 1) - 25% on Canada/Mexico, 10% on China
• China announces retaliation (Feb 4) - counter-tariffs effective Feb 10
• Canada/Mexico tariffs take effect (Mar 4) - trade disruption begins
• Steel & Aluminum 25% tariffs (Mar 12) - industrial metals impact
• Liberation Day tariffs (Apr 2) - broad tariff implementation
• 90-day tariff pause (Apr 9) - temporary relief (except China)
• Copper 50% tariffs (Aug 1) - semi-finished products tariffed; raw copper exempted
"""
print(analysis)

print("\n" + "="*60)
print("TWITTER CAPTION")
print("="*60)

caption = f"""
Precious metals since Oct 2024 📊

🥇 {returns_sorted.index[0]}: {returns_sorted.iloc[0]:+.1f}%
🥈 {returns_sorted.index[1]}: {returns_sorted.iloc[1]:+.1f}%
🥉 {returns_sorted.index[2]}: {returns_sorted.iloc[2]:+.1f}%
   {returns_sorted.index[3]}: {returns_sorted.iloc[3]:+.1f}%
   {returns_sorted.index[4]}: {returns_sorted.iloc[4]:+.1f}%

Election + tariff chaos driving safe-haven demand.
Aug copper drop: 50% tariff on semi-finished copper.

Hard assets are back. 🪙
"""
print(caption)

# %% [markdown]
# ## Why Precious Metals Are Rallying (Oct 2024 - Present)
# 
# ### Key Events & Their Impact on Precious Metals:
# 
# 1. **US Election - Trump Wins (Nov 5)** — Policy shift expectations and uncertainty drives safe-haven demand for gold/silver
# 
# 2. **Fed Rate Cut 25bps (Dec 18)** — Lower interest rates reduce opportunity cost of holding non-yielding precious metals
# 
# 3. **Trump Inauguration (Jan 20)** — "America First" agenda creates policy uncertainty
# 
# 4. **Tariffs Announced (Feb 1)** — 25% on Canada/Mexico, 10% on China sparks trade war fears → safe haven buying
# 
# 5. **China Announces Retaliation (Feb 4)** — Counter-tariffs announced (effective Feb 10), escalating tensions → more safe haven demand
# 
# 6. **Canada/Mexico Tariffs Take Effect (Mar 4)** — North American trade disruption begins, inflation fears support metals
# 
# 7. **Steel & Aluminum 25% Tariffs (Mar 12)** — Direct impact on industrial metals, supply chain concerns
# 
# 8. **Liberation Day Tariffs (Apr 2)** — Broad tariff implementation across multiple sectors → peak uncertainty
# 
# 9. **90-Day Tariff Pause (Apr 9)** — Temporary relief for most countries (except China), some risk-off unwind
# 
# 10. **Copper 50% Tariffs (Aug 1)** — 50% tariff imposed on semi-finished copper products; raw copper (cathodes, ores, scrap) exempted. This ended the COMEX-LME arbitrage trade, causing prices to realign and triggering copper selloff.
# 
# ---
# 
# ### Bullish Drivers for Precious Metals:
# 
# - **Tariff uncertainty** → Safe haven demand (every announcement drove gold/silver buying)
# - **Fed rate cuts** → Lower opportunity cost of holding non-yielding metals
# - **Dollar weakness** → Makes dollar-denominated commodities cheaper for international buyers
# - **Central bank buying** → Record gold purchases as reserves diversification away from USD
# - **"Debasement trade"** → Concerns about excess fiscal/monetary stimulus
# - **Silver industrial demand** → Fifth consecutive year of supply deficits; solar, EV, AI demand surging
# 
# ---
# 
# *Election uncertainty, trade war fears, and tariff policy reversals continue to drive volatility and safe-haven demand in precious metals markets.*

