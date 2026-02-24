# customer_analysis.py
# Requirements: pip install pandas numpy matplotlib

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# ────────────────────────────────────────────────
#  CONFIGURATION
# ────────────────────────────────────────────────

CSV_FILE = "customers.csv"

# ────────────────────────────────────────────────
#  1. Load & Prepare Data
# ────────────────────────────────────────────────

print("Loading data...")

try:
    df = pd.read_csv(CSV_FILE)
except FileNotFoundError:
    print(f"Error: File '{CSV_FILE}' not found.")
    print("Example expected columns: CustomerID, Name, Age, Gender, City, JoinDate, AnnualSpend, Orders, Category")
    exit(1)

print(f"Dataset shape: {df.shape}")
print("Columns:", df.columns.tolist())

# Standardize column names
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_").str.replace(r"[^a-z0-9_]", "", regex=True)

# Guess date column
date_cols = [col for col in df.columns if "date" in col or "joined" in col or "signup" in col]
if date_cols:
    try:
        df[date_cols[0]] = pd.to_datetime(df[date_cols[0]], errors='coerce')
    except:
        pass

# Guess numeric columns
num_cols = ['age', 'annual_spend', 'spend', 'total_spend', 'orders', 'purchases', 'tenure', 'days_as_customer']
for col in num_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

# ────────────────────────────────────────────────
#  2. Feature Engineering
# ────────────────────────────────────────────────

print("\nCreating features...")

# Days as customer
if any(col in df.columns for col in ['joindate', 'join_date', 'signup_date']):
    date_col = next((c for c in ['joindate', 'join_date', 'signup_date'] if c in df.columns), None)
    if date_col:
        today = pd.Timestamp.now()
        df['days_as_customer'] = (today - df[date_col]).dt.days.clip(lower=0)

# Simple RFM-like score
if all(col in df.columns for col in ['orders', 'annual_spend']):
    df['monetary'] = df['annual_spend'].fillna(0)
    df['frequency'] = df['orders'].fillna(0)
    
    m = df['monetary'].values
    f = df['frequency'].values
    m_norm = (m - np.nanmin(m)) / (np.nanmax(m) - np.nanmin(m) + 1e-8)
    f_norm = (f - np.nanmin(f)) / (np.nanmax(f) - np.nanmin(f) + 1e-8)
    
    df['rfm_score'] = np.round(100 * (0.6 * m_norm + 0.4 * f_norm), 1)

# Age groups
if 'age' in df.columns:
    bins = [0, 18, 25, 35, 45, 55, 999]
    labels = ['<18', '18-24', '25-34', '35-44', '45-54', '55+']
    df['age_group'] = pd.cut(df['age'], bins=bins, labels=labels, right=False)

print("Done.")

# ────────────────────────────────────────────────
#  3. Visualizations (3×2 layout)
# ────────────────────────────────────────────────

plt.style.use('ggplot')

fig = plt.figure(figsize=(16, 14))

# 1. Age histogram
ax1 = fig.add_subplot(3, 2, 1)
if 'age' in df.columns:
    df['age'].plot.hist(ax=ax1, bins=24, color='cornflowerblue', edgecolor='white')
    ax1.set_title('Age Distribution')
    ax1.set_xlabel('Age')
    ax1.grid(True, alpha=0.3)

# 2. Gender pie
ax2 = fig.add_subplot(3, 2, 2)
if 'gender' in df.columns:
    df['gender'].value_counts().plot.pie(ax=ax2, autopct='%1.0f%%',
                                         colors=['#66c2a5','#fc8d62','#8da0cb','#e78ac3'],
                                         startangle=90, textprops={'fontsize':10})
    ax2.set_title('Gender Distribution')
    ax2.set_ylabel('')

# 3. Annual spend histogram
ax3 = fig.add_subplot(3, 2, 3)
if 'annual_spend' in df.columns:
    df['annual_spend'].plot.hist(ax=ax3, bins=30, color='mediumseagreen', edgecolor='white')
    ax3.set_title('Annual Spend Distribution')
    ax3.set_xlabel('Annual Spend ($)')
    ax3.grid(True, alpha=0.3)

# 4. Avg spend by age group (bar)
ax4 = fig.add_subplot(3, 2, 4)
if 'age_group' in df.columns and 'annual_spend' in df.columns:
    df.groupby('age_group', observed=True)['annual_spend'].mean()\
      .plot.bar(ax=ax4, color='orchid')
    ax4.set_title('Avg Annual Spend by Age Group')
    ax4.set_ylabel('Avg Spend ($)')
    plt.xticks(rotation=45, ha='right')

# 5. Bar chart — Number of customers by city or category
ax5 = fig.add_subplot(3, 2, 5)
if 'city' in df.columns:
    df['city'].value_counts().head(10).plot.bar(ax=ax5, color='teal')
    ax5.set_title('Number of Customers by City (Top 10)')
    ax5.set_ylabel('Count')
    plt.xticks(rotation=50, ha='right')
elif 'category' in df.columns:
    df['category'].value_counts().head(8).plot.bar(ax=ax5, color='teal')
    ax5.set_title('Number of Customers by Category (Top 8)')
    ax5.set_ylabel('Count')
    plt.xticks(rotation=45, ha='right')

# 6. Pie chart — Top 5 cities or categories (sorted)
ax6 = fig.add_subplot(3, 2, 6)
if 'city' in df.columns:
    top5 = df['city'].value_counts().sort_values(ascending=False).head(5)
    top5.plot.pie(ax=ax6, autopct='%1.1f%%', startangle=90,
                  colors=plt.cm.Pastel1(range(len(top5))),
                  textprops={'fontsize':10})
    ax6.set_title('Top 5 Cities by Customer Count')
    ax6.set_ylabel('')
elif 'category' in df.columns:
    top5 = df['category'].value_counts().sort_values(ascending=False).head(5)
    top5.plot.pie(ax=ax6, autopct='%1.1f%%', startangle=90,
                  colors=plt.cm.Pastel1(range(len(top5))),
                  textprops={'fontsize':10})
    ax6.set_title('Top 5 Categories by Customer Count')
    ax6.set_ylabel('')

plt.tight_layout()
plt.show()

print("\nAnalysis complete.")