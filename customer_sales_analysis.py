# ============================================================
# Customer Sales Analysis
# Author: Pradeep Kumar
# Description: EDA on customer sales data to uncover trends,
#              top products, and regional performance insights.
# Tools: Python, Pandas, Matplotlib, Seaborn
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ── 1. Create Sample Dataset ─────────────────────────────────
np.random.seed(42)
n = 500

regions = ['North', 'South', 'East', 'West']
categories = ['Electronics', 'Clothing', 'Furniture', 'Food', 'Sports']
months = pd.date_range('2024-01-01', periods=12, freq='MS')

data = {
    'Order_ID': range(1001, 1001 + n),
    'Date': np.random.choice(months, n),
    'Region': np.random.choice(regions, n, p=[0.3, 0.2, 0.3, 0.2]),
    'Category': np.random.choice(categories, n, p=[0.25, 0.25, 0.2, 0.15, 0.15]),
    'Quantity': np.random.randint(1, 10, n),
    'Unit_Price': np.random.uniform(100, 5000, n).round(2),
    'Customer_Age': np.random.randint(18, 65, n),
    'Customer_Gender': np.random.choice(['Male', 'Female'], n),
}

df = pd.DataFrame(data)
df['Revenue'] = (df['Quantity'] * df['Unit_Price']).round(2)
df['Month'] = df['Date'].dt.strftime('%b')
df['Month_Num'] = df['Date'].dt.month

# Introduce some missing values for cleaning demo
df.loc[np.random.choice(df.index, 15), 'Customer_Age'] = np.nan

# ── 2. Data Overview ─────────────────────────────────────────
print("=" * 55)
print("         CUSTOMER SALES ANALYSIS REPORT")
print("=" * 55)

print("\n📋 Dataset Shape:", df.shape)
print("\n📋 First 5 Rows:")
print(df.head())

print("\n📋 Data Types:")
print(df.dtypes)

print("\n📋 Missing Values:")
print(df.isnull().sum())

# ── 3. Data Cleaning ─────────────────────────────────────────
print("\n🔧 Filling missing Customer_Age with median...")
df['Customer_Age'].fillna(df['Customer_Age'].median(), inplace=True)
print("   Missing values after cleaning:", df.isnull().sum().sum())

# ── 4. Key Statistics ────────────────────────────────────────
print("\n📊 Revenue Summary:")
print(df['Revenue'].describe().round(2))

total_revenue = df['Revenue'].sum()
avg_order_value = df['Revenue'].mean()
print(f"\n💰 Total Revenue:       ₹{total_revenue:,.2f}")
print(f"💰 Avg Order Value:     ₹{avg_order_value:,.2f}")
print(f"💰 Total Orders:        {len(df)}")

# ── 5. Analysis ──────────────────────────────────────────────

# Revenue by Category
print("\n📊 Revenue by Category:")
cat_rev = df.groupby('Category')['Revenue'].sum().sort_values(ascending=False)
print(cat_rev.round(2))

# Revenue by Region
print("\n📊 Revenue by Region:")
reg_rev = df.groupby('Region')['Revenue'].sum().sort_values(ascending=False)
print(reg_rev.round(2))

# Monthly Revenue Trend
monthly = df.groupby(['Month_Num', 'Month'])['Revenue'].sum().reset_index()
monthly = monthly.sort_values('Month_Num')

# ── 6. Visualizations ────────────────────────────────────────
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Customer Sales Analysis Dashboard', fontsize=16, fontweight='bold', y=1.02)

# Plot 1: Revenue by Category
sns.barplot(x=cat_rev.values, y=cat_rev.index, palette='Blues_r', ax=axes[0, 0])
axes[0, 0].set_title('Revenue by Category', fontweight='bold')
axes[0, 0].set_xlabel('Total Revenue (₹)')
axes[0, 0].set_ylabel('')
for i, v in enumerate(cat_rev.values):
    axes[0, 0].text(v + 500, i, f'₹{v:,.0f}', va='center', fontsize=9)

# Plot 2: Revenue by Region
colors = ['#2196F3', '#4CAF50', '#FF9800', '#9C27B0']
axes[0, 1].pie(reg_rev.values, labels=reg_rev.index, autopct='%1.1f%%',
               colors=colors, startangle=90)
axes[0, 1].set_title('Revenue Distribution by Region', fontweight='bold')

# Plot 3: Monthly Revenue Trend
axes[1, 0].plot(monthly['Month'], monthly['Revenue'], marker='o',
                color='#2196F3', linewidth=2, markersize=6)
axes[1, 0].fill_between(range(len(monthly)), monthly['Revenue'],
                         alpha=0.1, color='#2196F3')
axes[1, 0].set_title('Monthly Revenue Trend', fontweight='bold')
axes[1, 0].set_xlabel('Month')
axes[1, 0].set_ylabel('Revenue (₹)')
axes[1, 0].set_xticks(range(len(monthly)))
axes[1, 0].set_xticklabels(monthly['Month'], rotation=45)
axes[1, 0].grid(axis='y', alpha=0.3)

# Plot 4: Revenue Distribution
sns.histplot(df['Revenue'], bins=30, color='#4CAF50', ax=axes[1, 1], kde=True)
axes[1, 1].set_title('Revenue Distribution per Order', fontweight='bold')
axes[1, 1].set_xlabel('Revenue (₹)')
axes[1, 1].set_ylabel('Frequency')

plt.tight_layout()
plt.savefig('customer_sales_analysis.png', dpi=150, bbox_inches='tight')
plt.show()
print("\n✅ Chart saved as 'customer_sales_analysis.png'")

# ── 7. Key Insights ──────────────────────────────────────────
print("\n" + "=" * 55)
print("                  KEY INSIGHTS")
print("=" * 55)
top_cat = cat_rev.idxmax()
top_region = reg_rev.idxmax()
peak_month = monthly.loc[monthly['Revenue'].idxmax(), 'Month']
print(f"  ✅ Top Revenue Category : {top_cat}")
print(f"  ✅ Top Performing Region: {top_region}")
print(f"  ✅ Peak Sales Month     : {peak_month}")
print(f"  ✅ Total Revenue        : ₹{total_revenue:,.2f}")
print(f"  ✅ Avg Order Value      : ₹{avg_order_value:,.2f}")
print("=" * 55)
