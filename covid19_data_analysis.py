# ============================================================
# COVID-19 Data Analysis
# Author: Pradeep Kumar
# Description: Analyzing COVID-19 trends — cases, recoveries,
#              and fatality rates across countries over time.
# Tools: Python, Pandas, Matplotlib, Seaborn
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ── 1. Create Sample Dataset ─────────────────────────────────
np.random.seed(21)

countries = ['India', 'USA', 'Brazil', 'UK', 'Germany', 'France', 'Italy', 'Russia']
dates = pd.date_range('2021-01-01', '2021-12-31', freq='W')

rows = []
base_cases = {'India': 15000, 'USA': 80000, 'Brazil': 40000, 'UK': 25000,
              'Germany': 18000, 'France': 20000, 'Italy': 12000, 'Russia': 22000}

for country in countries:
    base = base_cases[country]
    for i, date in enumerate(dates):
        wave = 1 + 0.8 * np.sin(i * np.pi / 13)
        new_cases = int(base * wave * np.random.uniform(0.85, 1.15))
        new_cases = max(new_cases, 500)
        recovery_rate = np.random.uniform(0.85, 0.95)
        fatality_rate = np.random.uniform(0.01, 0.025)
        rows.append({
            'Date': date,
            'Country': country,
            'New_Cases': new_cases,
            'Recoveries': int(new_cases * recovery_rate),
            'Deaths': int(new_cases * fatality_rate),
            'Tests_Done': int(new_cases * np.random.uniform(8, 15)),
        })

df = pd.DataFrame(rows)
df['Active_Cases'] = df['New_Cases'] - df['Recoveries'] - df['Deaths']
df['Fatality_Rate_Pct'] = (df['Deaths'] / df['New_Cases'] * 100).round(2)
df['Recovery_Rate_Pct'] = (df['Recoveries'] / df['New_Cases'] * 100).round(2)
df['Month'] = df['Date'].dt.strftime('%b')
df['Month_Num'] = df['Date'].dt.month

# Introduce missing values
df.loc[np.random.choice(df.index, 20), 'Tests_Done'] = np.nan

# ── 2. Data Overview ─────────────────────────────────────────
print("=" * 55)
print("         COVID-19 DATA ANALYSIS REPORT")
print("=" * 55)

print("\n📋 Dataset Shape:", df.shape)
print("\n📋 First 5 Rows:")
print(df.head())

print("\n📋 Missing Values:")
print(df.isnull().sum())

# ── 3. Data Cleaning ─────────────────────────────────────────
df['Tests_Done'].fillna(df['Tests_Done'].median(), inplace=True)
print("\n🔧 Missing values filled. Remaining:", df.isnull().sum().sum())

# ── 4. Key Statistics ────────────────────────────────────────
total_cases = df['New_Cases'].sum()
total_deaths = df['Deaths'].sum()
total_recoveries = df['Recoveries'].sum()
avg_fatality = df['Fatality_Rate_Pct'].mean()

print(f"\n🌍 Total Cases (All Countries): {total_cases:,}")
print(f"💀 Total Deaths               : {total_deaths:,}")
print(f"💚 Total Recoveries           : {total_recoveries:,}")
print(f"📉 Avg Fatality Rate          : {avg_fatality:.2f}%")

print("\n📊 Cases by Country (Total):")
country_total = df.groupby('Country')['New_Cases'].sum().sort_values(ascending=False)
print(country_total)

# ── 5. Visualizations ────────────────────────────────────────
fig, axes = plt.subplots(2, 2, figsize=(15, 10))
fig.suptitle('COVID-19 Data Analysis Dashboard (2021)', fontsize=16, fontweight='bold')

# Plot 1: Total Cases by Country
colors = sns.color_palette('Reds_r', len(country_total))
axes[0, 0].barh(country_total.index, country_total.values, color=colors)
axes[0, 0].set_title('Total Cases by Country', fontweight='bold')
axes[0, 0].set_xlabel('Total New Cases')
axes[0, 0].invert_yaxis()
for i, v in enumerate(country_total.values):
    axes[0, 0].text(v + 1000, i, f'{v:,}', va='center', fontsize=8)

# Plot 2: Monthly Trend — Global New Cases
monthly_global = df.groupby(['Month_Num', 'Month'])['New_Cases'].sum().reset_index()
monthly_global = monthly_global.sort_values('Month_Num')
axes[0, 1].plot(monthly_global['Month'], monthly_global['New_Cases'],
                marker='o', color='#F44336', linewidth=2.5, markersize=7)
axes[0, 1].fill_between(range(len(monthly_global)), monthly_global['New_Cases'],
                         alpha=0.15, color='#F44336')
axes[0, 1].set_title('Monthly Global New Cases Trend', fontweight='bold')
axes[0, 1].set_xlabel('Month')
axes[0, 1].set_ylabel('Total New Cases')
axes[0, 1].set_xticks(range(len(monthly_global)))
axes[0, 1].set_xticklabels(monthly_global['Month'], rotation=45)
axes[0, 1].grid(axis='y', alpha=0.3)

# Plot 3: Fatality Rate by Country
fat_rate = df.groupby('Country')['Fatality_Rate_Pct'].mean().sort_values(ascending=False)
axes[1, 0].bar(fat_rate.index, fat_rate.values,
               color=sns.color_palette('OrRd', len(fat_rate)), edgecolor='white')
axes[1, 0].set_title('Average Fatality Rate by Country (%)', fontweight='bold')
axes[1, 0].set_xlabel('Country')
axes[1, 0].set_ylabel('Fatality Rate (%)')
axes[1, 0].tick_params(axis='x', rotation=30)
axes[1, 0].grid(axis='y', alpha=0.3)

# Plot 4: Recovery vs Deaths (stacked bar by country)
rec = df.groupby('Country')['Recoveries'].sum()
dth = df.groupby('Country')['Deaths'].sum()
x = np.arange(len(rec.index))
axes[1, 1].bar(x, rec.values, label='Recoveries', color='#4CAF50', alpha=0.85)
axes[1, 1].bar(x, dth.values, bottom=rec.values, label='Deaths', color='#F44336', alpha=0.85)
axes[1, 1].set_title('Recoveries vs Deaths by Country', fontweight='bold')
axes[1, 1].set_xticks(x)
axes[1, 1].set_xticklabels(rec.index, rotation=30)
axes[1, 1].set_ylabel('Count')
axes[1, 1].legend()
axes[1, 1].grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('covid19_analysis.png', dpi=150, bbox_inches='tight')
plt.show()
print("\n✅ Chart saved as 'covid19_analysis.png'")

# ── 6. Key Insights ──────────────────────────────────────────
highest_cases_country = country_total.idxmax()
lowest_fatality = fat_rate.idxmin()
peak_month = monthly_global.loc[monthly_global['New_Cases'].idxmax(), 'Month']

print("\n" + "=" * 55)
print("                  KEY INSIGHTS")
print("=" * 55)
print(f"  ✅ Highest Cases Country   : {highest_cases_country}")
print(f"  ✅ Lowest Fatality Rate    : {lowest_fatality}")
print(f"  ✅ Peak Cases Month        : {peak_month}")
print(f"  ✅ Global Avg Fatality Rate: {avg_fatality:.2f}%")
print(f"  ✅ Total Global Cases      : {total_cases:,}")
print(f"  ✅ Total Global Recoveries : {total_recoveries:,}")
print("=" * 55)
