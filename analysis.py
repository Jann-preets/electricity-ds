"""
=============================================================
  ELECTRICITY CONSUMPTION PATTERN — CHENNAI RESIDENTIAL AREA
  Data Science Project — Full Analysis Script
  Location  : Chennai, Tamil Nadu
  Date Range: January 2025 – February 2026
  Dataset   : Synthetic dataset modelled on TANGEDCO residential
              tariff patterns and Chennai climate data (IMD)
=============================================================

DATA SOURCE NOTE:
  This dataset is synthetically generated to reflect real-world
  Chennai residential electricity consumption patterns based on:
  - TANGEDCO (Tamil Nadu Generation & Distribution Corporation)
    residential tariff slabs and consumption norms
  - IMD (India Meteorological Department) Chennai temperature
    records for seasonal factors
  - Census of India 2011 household income distribution patterns
  Source reference: tangedco.gov.in | imdchennai.gov.in

HOW TO RUN:
  1. pip install pandas matplotlib seaborn scikit-learn numpy
  2. Place this file and 'chennai_electricity_data.csv' in same folder
  3. Run: python analysis.py
=============================================================
"""

# ── IMPORTS ───────────────────────────────────────────────
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import LabelEncoder
import numpy as np
import os
import warnings
warnings.filterwarnings('ignore')

# Create outputs folder if not exists
os.makedirs('outputs', exist_ok=True)

# ──────────────────────────────────────────────────────────
# STEP 1: LOAD DATASET
# ──────────────────────────────────────────────────────────
print("=" * 65)
print("  CHENNAI ELECTRICITY CONSUMPTION — DATA SCIENCE PROJECT")
print("=" * 65)

df = pd.read_csv('data/chennai_electricity_data.csv', parse_dates=['date'])

print(f"\n✅ Dataset loaded!")
print(f"   City       : Chennai, Tamil Nadu")
print(f"   Rows       : {len(df):,}")
print(f"   Columns    : {len(df.columns)}")
print(f"   Date Range : {df['date'].min().date()} → {df['date'].max().date()}")

# ──────────────────────────────────────────────────────────
# STEP 2: DATA PREPROCESSING
# ──────────────────────────────────────────────────────────
print("\n" + "─" * 65)
print("STEP 2: Data Preprocessing")
print("─" * 65)

# 2a. Check missing values
missing = df.isnull().sum()
print(f"\n   2a. Missing Values:")
print(f"       Total missing : {missing.sum()} ✅ (no missing values)")

# 2b. Remove duplicates
before_dup = len(df)
df.drop_duplicates(inplace=True)
print(f"\n   2b. Duplicate Removal:")
print(f"       Duplicates removed : {before_dup - len(df)}")
print(f"       Rows remaining     : {len(df):,}")

# 2c. Data type correction
df['date']        = pd.to_datetime(df['date'])
df['daily_kwh']   = df['daily_kwh'].astype(float)
df['num_members'] = df['num_members'].astype(int)
df['year']        = df['year'].astype(int)
print(f"\n   2c. Data Types Corrected:")
print(f"       date → datetime | daily_kwh → float | num_members → int")

# 2d. Outlier detection using Z-score
before_out = len(df)
mean_kwh   = df['daily_kwh'].mean()
std_kwh    = df['daily_kwh'].std()
z_scores   = np.abs((df['daily_kwh'] - mean_kwh) / std_kwh)
df         = df[z_scores <= 3]
print(f"\n   2d. Outlier Detection (Z-score ±3σ):")
print(f"       Outliers removed : {before_out - len(df)}")
print(f"       Rows after clean : {len(df):,}")

# 2e. Feature Engineering — 4 derived columns
print(f"\n   2e. Feature Engineering (4 derived columns):")

# Derived 1: season
def assign_season(month):
    if month in ['March','April','May','June']:       return 'Summer'
    elif month in ['July','August','September']:      return 'Monsoon'
    elif month in ['October','November']:             return 'Post-Monsoon'
    else:                                             return 'Cool/Winter'

df['season'] = df['month'].apply(assign_season)
print(f"       ✅ season          — Summer/Monsoon/Post-Monsoon/Cool/Winter")

# Derived 2: consumption_category
def consumption_cat(kwh):
    if kwh < 5:    return 'Low'
    elif kwh < 12: return 'Medium'
    else:          return 'High'

df['consumption_category'] = df['daily_kwh'].apply(consumption_cat)
print(f"       ✅ consumption_category — Low/Medium/High based on kWh")

# Derived 3: monthly_bill_inr (TANGEDCO slab-based estimate)
# Slab: 0-100 units @₹0, 101-200 @₹1.5, 201-500 @₹3, >500 @₹5 per unit
def estimate_bill(daily_kwh):
    monthly_units = daily_kwh * 30
    if monthly_units <= 100:   return 0
    elif monthly_units <= 200: return (monthly_units - 100) * 1.5
    elif monthly_units <= 500: return 100*1.5 + (monthly_units - 200) * 3
    else:                      return 100*1.5 + 300*3 + (monthly_units - 500) * 5

df['monthly_bill_inr'] = df['daily_kwh'].apply(estimate_bill)
print(f"       ✅ monthly_bill_inr — TANGEDCO slab-based cost estimate (₹)")

# Derived 4: peak_season_flag
df['peak_season_flag'] = df['season'].apply(lambda x: 1 if x == 'Summer' else 0)
print(f"       ✅ peak_season_flag — 1 if Summer (Mar–Jun), else 0")

# 2f. Basic statistical summary
print(f"\n   2f. Statistical Summary (daily_kwh):")
stats = df['daily_kwh'].describe()
print(f"       Mean   : {stats['mean']:.2f} kWh")
print(f"       Median : {df['daily_kwh'].median():.2f} kWh")
print(f"       Std    : {stats['std']:.2f} kWh")
print(f"       Min    : {stats['min']:.2f} kWh")
print(f"       Max    : {stats['max']:.2f} kWh")
print(f"       Q1     : {stats['25%']:.2f} kWh")
print(f"       Q3     : {stats['75%']:.2f} kWh")

# Save cleaned dataset
df.to_csv('data/chennai_electricity_cleaned.csv', index=False)
print(f"\n   ✅ Cleaned dataset saved → data/chennai_electricity_cleaned.csv")

# ──────────────────────────────────────────────────────────
# STEP 3: EXPLORATORY DATA ANALYSIS
# ──────────────────────────────────────────────────────────
print("\n" + "─" * 65)
print("STEP 3: Exploratory Data Analysis (EDA)")
print("─" * 65)

# Month ordering
month_order_full = [
    'Jan-2025','Feb-2025','Mar-2025','Apr-2025','May-2025','Jun-2025',
    'Jul-2025','Aug-2025','Sep-2025','Oct-2025','Nov-2025','Dec-2025',
    'Jan-2026','Feb-2026'
]
df['month_label'] = df['date'].dt.strftime('%b-%Y')
df['month_label'] = pd.Categorical(df['month_label'], categories=month_order_full, ordered=True)

monthly_avg = df.groupby('month_label', observed=True)['daily_kwh'].mean()

# 3a. Mean, Median, Std
print("\n   3a. Central Tendency:")
print(f"       Overall Mean   : {df['daily_kwh'].mean():.2f} kWh/day")
print(f"       Overall Median : {df['daily_kwh'].median():.2f} kWh/day")
print(f"       Std Deviation  : {df['daily_kwh'].std():.2f} kWh/day")

# 3b. Trend analysis
print("\n   3b. Monthly Trend:")
for month, kwh in monthly_avg.items():
    bar = "█" * int(kwh / 0.5)
    print(f"       {str(month):12s}: {kwh:5.2f} kWh  {bar}")

# 3c. Distribution
print("\n   3c. Consumption Category Distribution:")
cat_dist = df['consumption_category'].value_counts()
for cat, count in cat_dist.items():
    pct = count / len(df) * 100
    print(f"       {cat:8s}: {count:,} records ({pct:.1f}%)")

# 3d. Correlation analysis
print("\n   3d. Correlation Analysis:")
num_cols = ['daily_kwh','num_members','peak_season_flag','monthly_bill_inr']
corr = df[num_cols].corr()
print(f"       daily_kwh vs num_members       : {corr.loc['daily_kwh','num_members']:.3f}")
print(f"       daily_kwh vs peak_season_flag  : {corr.loc['daily_kwh','peak_season_flag']:.3f}")
print(f"       daily_kwh vs monthly_bill_inr  : {corr.loc['daily_kwh','monthly_bill_inr']:.3f}")

# 3e. Patterns and anomalies
income_avg   = df.groupby('income_level')['daily_kwh'].mean()
weekend_avg  = df.groupby('is_weekend')['daily_kwh'].mean()
weekday_val  = weekend_avg.get('No', 0)
weekend_val  = weekend_avg.get('Yes', 0)
pct_diff     = ((weekend_val - weekday_val) / weekday_val) * 100
area_avg     = df.groupby('area')['daily_kwh'].mean().sort_values(ascending=False)

print("\n   3e. Key Patterns:")
print(f"       Income gap (High/Low)  : {income_avg['High']/income_avg['Low']:.1f}×")
print(f"       Weekend uplift         : +{pct_diff:.1f}%")
print(f"       Top area               : {area_avg.index[0]} ({area_avg.iloc[0]:.2f} kWh)")
print(f"       Lowest area            : {area_avg.index[-1]} ({area_avg.iloc[-1]:.2f} kWh)")

# ──────────────────────────────────────────────────────────
# STEP 4: CUSTOM ANALYTICAL METRIC
#         Seasonal Consumption Stress Index (SCSI)
# ──────────────────────────────────────────────────────────
print("\n" + "─" * 65)
print("STEP 4: Custom Analytical Metric — Seasonal Consumption Stress Index (SCSI)")
print("─" * 65)

print("""
   DEFINITION:
   The Seasonal Consumption Stress Index (SCSI) measures how much
   each month's electricity demand deviates from the annual average.
   A high SCSI indicates grid stress and high consumer burden.

   FORMULA:
   SCSI = ((Month_Avg - Annual_Avg) / Annual_Avg) × 100

   INTERPRETATION:
   • SCSI > 20   → High stress month (Summer peak, grid under pressure)
   • SCSI 0–20   → Moderate month
   • SCSI < 0    → Low stress month (Winter/Cool season)
""")

annual_avg = df['daily_kwh'].mean()
scsi_data  = {}
for month, avg in monthly_avg.items():
    scsi = ((avg - annual_avg) / annual_avg) * 100
    scsi_data[month] = round(scsi, 2)

print("   SCSI Values by Month:")
for month, scsi in scsi_data.items():
    stress = "🔴 HIGH STRESS" if scsi > 20 else ("🟡 MODERATE" if scsi >= 0 else "🟢 LOW STRESS")
    print(f"   {str(month):12s}: SCSI = {scsi:+6.1f}%  {stress}")

# ──────────────────────────────────────────────────────────
# STEP 5: VISUALIZATIONS (8 charts — all required types)
# ──────────────────────────────────────────────────────────
print("\n" + "─" * 65)
print("STEP 5: Creating Visualizations...")
print("─" * 65)

# Color palette
C = {
    'y':'#f4be45','g':'#2dd4a0','b':'#5bb8f5',
    'r':'#f06470','p':'#a78bfa','bg':'#080b10',
    'card':'#0e1420','grid':'#1a2235','text':'#eceae2','muted':'#7a8698'
}
INC_COLORS = {'Low':C['g'], 'Middle':C['b'], 'High':C['r']}

plt.rcParams.update({
    'font.family':'DejaVu Sans',
    'axes.facecolor':C['card'],'figure.facecolor':C['bg'],
    'axes.edgecolor':C['grid'],'axes.labelcolor':C['muted'],
    'xtick.color':C['muted'],'ytick.color':C['muted'],
    'text.color':C['text'],'grid.color':C['grid'],
    'grid.linewidth':0.6,'figure.dpi':150,
})

fig = plt.figure(figsize=(18, 22))
fig.suptitle(
    'Chennai Residential Electricity Consumption — Jan 2025 to Feb 2026\n'
    'Data Science Project | SRM IST-Ramapuram',
    fontsize=14, fontweight='bold', y=0.98, color=C['text']
)
gs = gridspec.GridSpec(4, 2, figure=fig, hspace=0.45, wspace=0.35)

# ── Chart 1: LINE PLOT — Monthly trend ──
ax1 = fig.add_subplot(gs[0, :])
vals   = monthly_avg.values
labels = [str(m) for m in monthly_avg.index]
ax1.plot(range(len(vals)), vals, color=C['y'], linewidth=2.5,
         marker='o', markersize=7, markerfacecolor=C['bg'], markeredgewidth=2)
ax1.fill_between(range(len(vals)), vals, alpha=0.1, color=C['y'])
ax1.set_xticks(range(len(vals)))
ax1.set_xticklabels(labels, rotation=30, fontsize=9)
ax1.set_title('① Line Plot — Monthly Consumption Trend (Jan 2025–Feb 2026)',
              fontweight='bold', color=C['text'], pad=10)
ax1.set_ylabel('Avg kWh/day', color=C['muted'])
peak_i = int(np.argmax(vals))
low_i  = int(np.argmin(vals))
ax1.annotate('Peak (May)', xy=(peak_i, vals[peak_i]),
             xytext=(peak_i-2, vals[peak_i]+0.6),
             arrowprops=dict(arrowstyle='->', color=C['r']),
             fontsize=9, color=C['r'], fontweight='bold')
ax1.annotate('Low (Nov)', xy=(low_i, vals[low_i]),
             xytext=(low_i+1, vals[low_i]-0.8),
             arrowprops=dict(arrowstyle='->', color=C['g']),
             fontsize=9, color=C['g'], fontweight='bold')

# ── Chart 2: BAR CHART — Income level ──
ax2 = fig.add_subplot(gs[1, 0])
inc_s = income_avg.sort_index()
bars2 = ax2.bar(inc_s.index, inc_s.values,
                color=[INC_COLORS[k] for k in inc_s.index],
                width=0.5, edgecolor=C['bg'], linewidth=1.5, zorder=3)
for b in bars2:
    ax2.text(b.get_x()+b.get_width()/2, b.get_height()+0.1,
             f'{b.get_height():.1f}', ha='center', va='bottom',
             fontsize=10, fontweight='bold', color=C['text'])
ax2.set_title('② Bar Chart — Income Level vs Consumption',
              fontweight='bold', color=C['text'], pad=8)
ax2.set_ylabel('Avg kWh/day', color=C['muted'])
ax2.grid(axis='y', color=C['grid'], linewidth=0.6)

# ── Chart 3: BOXPLOT — Distribution by income ──
ax3 = fig.add_subplot(gs[1, 1])
income_groups = [df[df['income_level']==lvl]['daily_kwh'].values
                 for lvl in ['Low','Middle','High']]
bp = ax3.boxplot(income_groups, labels=['Low','Middle','High'],
                 patch_artist=True, medianprops=dict(color='white', linewidth=2))
box_colors = [C['g'], C['b'], C['r']]
for patch, color in zip(bp['boxes'], box_colors):
    patch.set_facecolor(color); patch.set_alpha(0.7)
for element in ['whiskers','caps','fliers']:
    plt.setp(bp[element], color=C['muted'])
ax3.set_title('③ Boxplot — Consumption Distribution by Income',
              fontweight='bold', color=C['text'], pad=8)
ax3.set_ylabel('kWh/day', color=C['muted'])
ax3.grid(axis='y', color=C['grid'], linewidth=0.6)

# ── Chart 4: SCATTER PLOT — Members vs Consumption ──
ax4 = fig.add_subplot(gs[2, 0])
sample = df.sample(n=1500, random_state=42)
scatter_colors = [INC_COLORS.get(inc, C['b']) for inc in sample['income_level']]
ax4.scatter(sample['num_members'], sample['daily_kwh'],
            c=scatter_colors, alpha=0.35, s=20, edgecolors='none')
# Add trend line
z = np.polyfit(sample['num_members'], sample['daily_kwh'], 1)
p = np.poly1d(z)
x_line = np.linspace(1, 6, 100)
ax4.plot(x_line, p(x_line), color=C['y'], linewidth=2, linestyle='--', label='Trend')
ax4.set_title('④ Scatter Plot — Household Size vs Consumption',
              fontweight='bold', color=C['text'], pad=8)
ax4.set_xlabel('Number of Members', color=C['muted'])
ax4.set_ylabel('kWh/day', color=C['muted'])
ax4.legend(['Trend line'], fontsize=8, facecolor=C['card'], labelcolor=C['text'])
ax4.grid(color=C['grid'], linewidth=0.6)

# ── Chart 5: HEATMAP — Correlation matrix ──
ax5 = fig.add_subplot(gs[2, 1])
num_df = df[['daily_kwh','num_members','peak_season_flag','monthly_bill_inr']].copy()
num_df.columns = ['kWh/day','Members','Peak Flag','Bill (₹)']
corr_matrix = num_df.corr()
sns.heatmap(corr_matrix, ax=ax5, annot=True, fmt='.2f', cmap='YlOrRd',
            linewidths=0.5, cbar_kws={'label':'Correlation'},
            annot_kws={'size':10, 'weight':'bold'}, linecolor=C['bg'])
ax5.set_title('⑤ Heatmap — Correlation Matrix',
              fontweight='bold', color=C['text'], pad=8)
ax5.tick_params(colors=C['muted'], labelsize=9)

# ── Chart 6: BAR CHART — SCSI Index ──
ax6 = fig.add_subplot(gs[3, 0])
scsi_vals   = list(scsi_data.values())
scsi_labels = [str(m)[:3] for m in scsi_data.keys()]
bar_colors6 = [C['r'] if v > 20 else (C['y'] if v >= 0 else C['g']) for v in scsi_vals]
ax6.bar(range(len(scsi_vals)), scsi_vals, color=bar_colors6,
        edgecolor=C['bg'], linewidth=1, zorder=3)
ax6.axhline(0, color=C['muted'], linewidth=1, linestyle='--')
ax6.axhline(20, color=C['r'], linewidth=1, linestyle=':', alpha=0.6, label='High stress threshold')
ax6.set_xticks(range(len(scsi_vals)))
ax6.set_xticklabels(scsi_labels, rotation=30, fontsize=8)
ax6.set_title('⑥ Bar Chart — Seasonal Consumption Stress Index (SCSI)',
              fontweight='bold', color=C['text'], pad=8)
ax6.set_ylabel('SCSI (%)', color=C['muted'])
ax6.legend(fontsize=8, facecolor=C['card'], labelcolor=C['text'])
ax6.grid(axis='y', color=C['grid'], linewidth=0.6)

# ── Chart 7: BOXPLOT — Season distribution ──
ax7 = fig.add_subplot(gs[3, 1])
season_order  = ['Cool/Winter','Post-Monsoon','Monsoon','Summer']
season_groups = [df[df['season']==s]['daily_kwh'].values for s in season_order]
bp7 = ax7.boxplot(season_groups, labels=['Cool','Post-\nMon','Monsoon','Summer'],
                  patch_artist=True, medianprops=dict(color='white', linewidth=2))
s_colors = [C['b'], C['g'], C['p'], C['r']]
for patch, color in zip(bp7['boxes'], s_colors):
    patch.set_facecolor(color); patch.set_alpha(0.7)
for element in ['whiskers','caps','fliers']:
    plt.setp(bp7[element], color=C['muted'])
ax7.set_title('⑦ Boxplot — Consumption by Season',
              fontweight='bold', color=C['text'], pad=8)
ax7.set_ylabel('kWh/day', color=C['muted'])
ax7.grid(axis='y', color=C['grid'], linewidth=0.6)

plt.savefig('outputs/charts.png', dpi=150, bbox_inches='tight', facecolor=C['bg'])
print("   ✅ Charts saved → outputs/charts.png")
plt.close()

# ──────────────────────────────────────────────────────────
# STEP 6: MACHINE LEARNING MODEL
# ──────────────────────────────────────────────────────────
print("\n" + "─" * 65)
print("STEP 6: Machine Learning — Linear Regression Model")
print("─" * 65)

df_ml = df.copy()
le    = LabelEncoder()
for col in ['income_level','house_type','is_weekend','area','season']:
    df_ml[col+'_enc'] = le.fit_transform(df_ml[col])

feature_cols = ['income_level_enc','house_type_enc','num_members',
                'is_weekend_enc','area_enc','peak_season_flag']
X = df_ml[feature_cols]
y = df_ml['daily_kwh']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
rmse   = np.sqrt(mean_squared_error(y_test, y_pred))
r2     = r2_score(y_test, y_pred)

print(f"\n   Model            : Linear Regression")
print(f"   Training samples : {len(X_train):,} (80%)")
print(f"   Testing samples  : {len(X_test):,} (20%)")
print(f"\n   📈 Performance:")
print(f"   R² Score  : {r2:.4f}  (~{r2*100:.0f}% variance explained)")
print(f"   RMSE      : {rmse:.4f} kWh/day")

print(f"\n   🔑 Feature Importances (by absolute coefficient):")
feat_imp = sorted(zip(feature_cols, model.coef_), key=lambda x: abs(x[1]), reverse=True)
for feat, coef in feat_imp:
    direction = "↑ increases" if coef > 0 else "↓ decreases"
    print(f"   {feat.replace('_enc',''):22s}: {coef:+.4f}  ({direction} consumption)")

# ──────────────────────────────────────────────────────────
# STEP 7: FINAL SUMMARY
# ──────────────────────────────────────────────────────────
print("\n" + "=" * 65)
print("  FINAL FINDINGS — CHENNAI ELECTRICITY CONSUMPTION PROJECT")
print("=" * 65)

peak_label   = monthly_avg.idxmax()
low_label    = monthly_avg.idxmin()
summer_avg_v = df[df['season']=='Summer']['daily_kwh'].mean()
cool_avg_v   = df[df['season']=='Cool/Winter']['daily_kwh'].mean()
top_scsi     = max(scsi_data, key=scsi_data.get)

print(f"""
📌 KEY INSIGHTS:

   1. SEASONAL PATTERN
      Peak month     : {peak_label} ({monthly_avg[peak_label]:.2f} kWh/day)
      Lowest month   : {low_label} ({monthly_avg[low_label]:.2f} kWh/day)
      Summer avg     : {summer_avg_v:.2f} kWh/day  (Mar–Jun)
      Cool season avg: {cool_avg_v:.2f} kWh/day  (Oct–Jan)

   2. CUSTOM METRIC — SCSI
      Highest stress : {top_scsi} (SCSI = {scsi_data[top_scsi]:+.1f}%)
      Meaning        : May has the highest grid stress in Chennai

   3. INCOME GAP
      High income    : {income_avg['High']:.2f} kWh/day
      Low income     : {income_avg['Low']:.2f} kWh/day
      Gap ratio      : {income_avg['High']/income_avg['Low']:.1f}×

   4. WEEKEND EFFECT
      Weekday        : {weekday_val:.2f} kWh/day
      Weekend        : {weekend_val:.2f} kWh/day
      Uplift         : +{pct_diff:.1f}%

   5. ML MODEL
      R² = {r2:.4f} | RMSE = {rmse:.2f} kWh/day

📂 OUTPUTS GENERATED:
   data/chennai_electricity_cleaned.csv  — Cleaned dataset with features
   outputs/charts.png                    — 7 analysis charts

✅ Analysis complete!
""")
