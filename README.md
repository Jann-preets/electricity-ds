# ⚡ Electricity Consumption Pattern in Residential Area
### Chennai, Tamil Nadu | Data Science Project | Jan 2025 – Feb 2026

---

## Problem Statement

Electricity consumption in urban residential areas varies significantly based on income, season, household size, and location. This project analyzes these patterns for Chennai households to help utility boards plan infrastructure and design targeted conservation programs.

---

## Project Structure

```
electricity-ds/
├── data/
│   ├── chennai_electricity_data.csv       # Raw dataset (63,600 records)
│   └── chennai_electricity_cleaned.csv    # Cleaned + feature-engineered dataset
├── outputs/
│   ├── charts.png                         # 7 analysis charts
│   └── analytical_report.pdf             # 4-page analytical report
├── analysis.py                            # Full analysis + ML script
├── generate_report.py                     # PDF report generator
├── index.html                             # Interactive dashboard
└── README.md
```

---

## How to Run

```bash
# Install dependencies
pip install pandas matplotlib seaborn scikit-learn numpy reportlab

# Step 1 — Run full analysis (cleans data, EDA, charts, ML model)
python analysis.py

# Step 2 — Generate PDF report
python generate_report.py

# Step 3 — View dashboard
# Open index.html in any browser
```

---

## Dataset

| Item | Detail |
|------|--------|
| Records | 63,600 daily readings |
| Households | 150 across 10 Chennai areas |
| Period | Jan 1 2025 – Feb 28 2026 (14 months) |
| Features | 13 columns (9 original + 4 engineered) |
| Source | Synthetic — modelled on TANGEDCO tariff norms & IMD Chennai climate data |

---

## Preprocessing Steps

- Missing value check — 0 missing values
- Duplicate removal — 0 duplicates
- Data type correction — date, float, int
- Outlier removal (Z-score ±3σ) — 462 rows removed
- Feature engineering — 4 derived columns: `season`, `consumption_category`, `monthly_bill_inr`, `peak_season_flag`

---

## Custom Metric — Seasonal Consumption Stress Index (SCSI)

**Formula:** `SCSI = ((Month_Avg - Annual_Avg) / Annual_Avg) × 100`

**Interpretation:**
- SCSI > +20% → High Stress (Summer peak)
- SCSI 0–20% → Moderate
- SCSI < 0% → Low Stress (Cool season)

May 2025 = SCSI of +41.0% — highest grid stress month in Chennai.

---

## Key Findings

- **Peak:** May 2025 at 11.65 kWh/day — Chennai summer (38–42°C) drives heavy AC usage
- **Lowest:** November 2025 at 6.06 kWh/day — NE monsoon cool season
- **Income gap:** High income = 14.21 kWh vs Low income = 3.21 kWh (4.4× difference)
- **Weekend effect:** +16.1% more consumption on Sat–Sun
- **Top area:** Kodambakkam (10.59 kWh) | Lowest: Porur (5.82 kWh)

---

## ML Model

Linear Regression | R² = 0.46 | RMSE = 4.07 kWh/day | 80/20 split

---

## Tools & Technologies

Python, pandas, NumPy, Matplotlib, Seaborn, scikit-learn, ReportLab, HTML5, CSS3, JavaScript, Chart.js

---

*Data Science Semester Project · SRM IST-Ramapuram · 2024–25*
