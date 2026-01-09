# %% [markdown]
# # GDP Per Capita by Country
# 
# This notebook fetches the latest GDP per capita data (in current US$) for countries around the world using the World Bank API.

# %%
import pandas as pd
import requests

# Fetch GDP per capita data from World Bank API
# Indicator: NY.GDP.PCAP.CD (GDP per capita in current US$)
url = "https://api.worldbank.org/v2/country/all/indicator/NY.GDP.PCAP.CD"
params = {
    "format": "json",
    "per_page": 500,
    "date": "2022:2023",  # Get most recent years
    "source": 2
}

response = requests.get(url, params=params)
data = response.json()

print(f"Successfully fetched data from World Bank API")
print(f"Total records available: {data[0]['total']}")
print(f"Records fetched: {len(data[1])}")

# %%
# Parse the data into a DataFrame
records = []
for item in data[1]:
    if item['value'] is not None:  # Only include countries with data
        records.append({
            'Country': item['country']['value'],
            'Country Code': item['countryiso3code'],
            'Year': item['date'],
            'GDP per Capita (USD)': item['value']
        })

df = pd.DataFrame(records)

# Get the most recent year for each country
df_latest = df.sort_values('Year', ascending=False).drop_duplicates(subset='Country', keep='first')
df_latest = df_latest.sort_values('GDP per Capita (USD)', ascending=False).reset_index(drop=True)

print(f"Countries with GDP per capita data: {len(df_latest)}")

# %%
!pip install pycountry -q

# %%
regional_codes = ['WLD', 'HIC', 'LIC', 'LMC', 'MIC', 'UMC', 'EAS', 'ECS', 'LCN', 'MEA', 
                  'NAC', 'SAS', 'SSF', 'EUU', 'OED', 'OSS', 'PSS', 'TSS', 'ARB', 'CSS',
                  'EMU', 'FCS', 'HPC', 'IBD', 'IBT', 'IDA', 'IDB', 'IDX', 'LAC', 'LDC',
                  'LMY', 'LTE', 'MNA', 'PRE', 'PST', 'SSA', 'TEA', 'TEC', 'TLA', 'TMN', 'TSA']

df_countries = df_latest[~df_latest['Country Code'].isin(regional_codes)].copy()
df_countries = df_countries[df_countries['Country Code'] != ''].reset_index(drop=True)
df_countries.index = df_countries.index + 1

import pycountry

def get_flag_img(country_code_3):
    """Convert ISO3 country code to flag image HTML using flagcdn.com."""
    try:
        country = pycountry.countries.get(alpha_3=country_code_3)
        if country:
            iso2 = country.alpha_2.lower()
            return f'<img src="https://flagcdn.com/24x18/{iso2}.png" width="24" height="18" alt="{iso2}">'
    except:
        pass
    
    special_codes = {
        'XKX': 'xk',
        'HKG': 'hk',
        'MAC': 'mo',
        'TWN': 'tw',
        'PSE': 'ps',
    }
    iso2 = special_codes.get(country_code_3, '')
    if iso2:
        return f'<img src="https://flagcdn.com/24x18/{iso2}.png" width="24" height="18" alt="{iso2}">'
    return '🏳️'

df_countries['Flag'] = df_countries['Country Code'].apply(get_flag_img)

print(f"Total countries: {len(df_countries)}")

# %%
from IPython.display import display, HTML

pd.options.display.float_format = '${:,.2f}'.format
pd.set_option('display.max_rows', 250)

df_display = df_countries[['Flag', 'Country', 'Country Code', 'Year', 'GDP per Capita (USD)']].copy()
df_display['GDP per Capita (USD)'] = df_display['GDP per Capita (USD)'].apply(lambda x: f'${x:,.2f}')

html = df_display.to_html(escape=False, index=True)
display(HTML(html))

# %%
# Format the GDP values nicely
pd.options.display.float_format = '${:,.2f}'.format
pd.set_option('display.max_rows', 250)

# Display the full table
df_display = df_countries[['Country', 'Country Code', 'Year', 'GDP per Capita (USD)']].copy()
df_display

# %% [markdown]
# ## Summary Statistics

# %%
# Summary statistics
print("=" * 50)
print("GDP PER CAPITA SUMMARY STATISTICS")
print("=" * 50)
print(f"\nNumber of countries: {len(df_countries)}")
print(f"\nHighest GDP per capita:")
print(f"  {df_countries.iloc[0]['Country']}: ${df_countries.iloc[0]['GDP per Capita (USD)']:,.2f}")
print(f"\nLowest GDP per capita:")
print(f"  {df_countries.iloc[-1]['Country']}: ${df_countries.iloc[-1]['GDP per Capita (USD)']:,.2f}")
print(f"\nMean GDP per capita: ${df_countries['GDP per Capita (USD)'].mean():,.2f}")
print(f"Median GDP per capita: ${df_countries['GDP per Capita (USD)'].median():,.2f}")
print(f"\nData year: {df_countries['Year'].mode()[0]}")

# %%
from IPython.display import display, HTML

top_20 = "<h3>TOP 20 COUNTRIES BY GDP PER CAPITA</h3><table style='font-size:14px'>"
for i, row in df_countries.head(20).iterrows():
    top_20 += f"<tr><td>{i}</td><td>{row['Flag']}</td><td>{row['Country']}</td><td style='text-align:right'>${row['GDP per Capita (USD)']:,.2f}</td></tr>"
top_20 += "</table>"

bottom_20 = "<h3>BOTTOM 20 COUNTRIES BY GDP PER CAPITA</h3><table style='font-size:14px'>"
for i, row in df_countries.tail(20).iterrows():
    bottom_20 += f"<tr><td>{i}</td><td>{row['Flag']}</td><td>{row['Country']}</td><td style='text-align:right'>${row['GDP per Capita (USD)']:,.2f}</td></tr>"
bottom_20 += "</table>"

display(HTML(top_20))
display(HTML(bottom_20))

