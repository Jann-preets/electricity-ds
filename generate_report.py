"""
Generate the 3-4 page Analytical Report PDF for submission
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                 TableStyle, HRFlowable, PageBreak)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
import os

os.makedirs('outputs', exist_ok=True)

# ── COLORS ─────────────────────────────────────────────
DARK   = colors.HexColor('#0e1420')
AMBER  = colors.HexColor('#d4960a')
TEAL   = colors.HexColor('#0f9b72')
BLUE   = colors.HexColor('#1a7fc4')
RED    = colors.HexColor('#d63346')
GRAY   = colors.HexColor('#5a6478')
LGRAY  = colors.HexColor('#f0f2f5')
WHITE  = colors.white
BLACK  = colors.HexColor('#1a1f2e')

doc = SimpleDocTemplate(
    'outputs/analytical_report.pdf',
    pagesize=A4,
    rightMargin=2*cm, leftMargin=2*cm,
    topMargin=2*cm, bottomMargin=2*cm
)

styles = getSampleStyleSheet()

# Custom styles
def S(name, **kwargs):
    return ParagraphStyle(name, **kwargs)

title_style = S('Title2', fontSize=20, fontName='Helvetica-Bold',
                textColor=BLACK, alignment=TA_CENTER, spaceAfter=6)
subtitle_style = S('Subtitle', fontSize=11, fontName='Helvetica',
                   textColor=GRAY, alignment=TA_CENTER, spaceAfter=4)
h1_style = S('H1', fontSize=13, fontName='Helvetica-Bold',
             textColor=DARK, spaceBefore=14, spaceAfter=6,
             borderPad=4, backColor=LGRAY,
             leftIndent=0, rightIndent=0)
h2_style = S('H2', fontSize=11, fontName='Helvetica-Bold',
             textColor=BLUE, spaceBefore=10, spaceAfter=4)
body_style = S('Body2', fontSize=9.5, fontName='Helvetica',
               textColor=BLACK, leading=15, alignment=TA_JUSTIFY,
               spaceAfter=6)
bullet_style = S('Bullet', fontSize=9.5, fontName='Helvetica',
                 textColor=BLACK, leading=14, leftIndent=16,
                 spaceAfter=3)
bold_style = S('Bold', fontSize=9.5, fontName='Helvetica-Bold',
               textColor=BLACK, leading=14, spaceAfter=4)
caption_style = S('Caption', fontSize=8.5, fontName='Helvetica-Oblique',
                  textColor=GRAY, alignment=TA_CENTER, spaceAfter=6)
formula_style = S('Formula', fontSize=10, fontName='Courier-Bold',
                  textColor=DARK, backColor=LGRAY, leading=16,
                  leftIndent=20, spaceAfter=6, spaceBefore=4)

def HR(): return HRFlowable(width='100%', thickness=0.5,
                              color=colors.HexColor('#d0d4dc'), spaceAfter=6)
def SP(h=6): return Spacer(1, h)
def B(text): return f'<b>{text}</b>'
def C(text, col): return f'<font color="{col}">{text}</font>'

story = []

# ══════════════════════════════════════════════════════════════
# PAGE 1 — TITLE + INTRODUCTION + DATA SOURCE
# ══════════════════════════════════════════════════════════════

# Header block
header_data = [[
    Paragraph('<b>ELECTRICITY CONSUMPTION PATTERN</b><br/>'
              '<font size=9>IN RESIDENTIAL AREA — CHENNAI, TAMIL NADU</font>',
              ParagraphStyle('hd', fontSize=14, fontName='Helvetica-Bold',
                             textColor=WHITE, alignment=TA_CENTER, leading=20)),
    Paragraph('<font size=8>Data Science Project<br/>'
              'SRM IST-Ramapuram<br/>2024–25</font>',
              ParagraphStyle('hd2', fontSize=8, fontName='Helvetica',
                             textColor=WHITE, alignment=TA_CENTER, leading=13))
]]
header_table = Table(header_data, colWidths=[13*cm, 4*cm])
header_table.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), DARK),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('TOPPADDING', (0,0), (-1,-1), 14),
    ('BOTTOMPADDING', (0,0), (-1,-1), 14),
    ('LEFTPADDING', (0,0), (-1,-1), 12),
    ('RIGHTPADDING', (0,0), (-1,-1), 12),
    ('ROUNDEDCORNERS', [6,6,6,6]),
]))
story.append(header_table)
story.append(SP(12))

# Meta info row
meta_data = [['Period', 'Jan 2025 – Feb 2026'],
             ['Location', 'Chennai, Tamil Nadu'],
             ['Households', '150'],
             ['Total Records', '63,600 daily readings']]
meta_table = Table(meta_data, colWidths=[4*cm, 13*cm])
meta_table.setStyle(TableStyle([
    ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
    ('FONTNAME', (1,0), (1,-1), 'Helvetica'),
    ('FONTSIZE', (0,0), (-1,-1), 9),
    ('TEXTCOLOR', (0,0), (0,-1), GRAY),
    ('TEXTCOLOR', (1,0), (1,-1), BLACK),
    ('ROWBACKGROUNDS', (0,0), (-1,-1), [LGRAY, WHITE]),
    ('TOPPADDING', (0,0), (-1,-1), 5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ('LEFTPADDING', (0,0), (-1,-1), 10),
    ('GRID', (0,0), (-1,-1), 0.3, colors.HexColor('#d0d4dc')),
]))
story.append(meta_table)
story.append(SP(10))

# ── SECTION 1: INTRODUCTION ──
story.append(Paragraph('1. Introduction', h1_style))
story.append(HR())
story.append(Paragraph(
    'Electricity is one of the most critical utilities in urban residential areas. '
    'Understanding <b>how</b> and <b>why</b> consumption varies across households '
    'helps electricity boards plan infrastructure, design subsidy programs, and '
    'support energy conservation initiatives. This project analyzes residential '
    'electricity consumption patterns across 150 households in <b>Chennai, Tamil Nadu</b> '
    'over a 14-month period from January 2025 to February 2026.',
    body_style))
story.append(Paragraph(
    'Chennai was chosen due to its distinct climate — intense summers (38–42°C, March–June) '
    'driving heavy AC usage, followed by the Northeast monsoon cool season (October–January) '
    'which significantly reduces consumption. This seasonal contrast makes Chennai an ideal '
    'location to study the impact of climate on residential energy use.',
    body_style))

story.append(Paragraph('<b>Objectives:</b>', bold_style))
for obj in [
    'Identify seasonal consumption patterns across Chennai\'s climate cycle',
    'Analyze the impact of income level, household size, and house type on usage',
    'Compare electricity consumption across 10 Chennai localities',
    'Design a custom Seasonal Consumption Stress Index (SCSI)',
    'Build a predictive ML model for daily electricity consumption',
]:
    story.append(Paragraph(f'• {obj}', bullet_style))
story.append(SP(8))

# ── SECTION 2: DATA SOURCE ──
story.append(Paragraph('2. Data Source & Collection', h1_style))
story.append(HR())
story.append(Paragraph(
    'The dataset was synthetically generated to accurately reflect real-world Chennai '
    'residential electricity consumption patterns. All parameters and factors are '
    'grounded in the following official sources:', body_style))

src_data = [
    ['Source', 'Usage in Dataset', 'Reference'],
    ['TANGEDCO', 'Tariff slabs, base consumption norms\nfor Low/Middle/High income', 'tangedco.gov.in'],
    ['IMD Chennai', 'Monthly temperature data driving\nseasonal consumption factors', 'imdchennai.gov.in'],
    ['Census of India 2011', 'Household income distribution\nand appliance ownership patterns', 'censusindia.gov.in'],
    ['CEA India', 'Per-capita electricity consumption\nnorms for Tamil Nadu', 'cea.nic.in'],
]
src_table = Table(src_data, colWidths=[3.5*cm, 7*cm, 6.5*cm])
src_table.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), DARK),
    ('TEXTCOLOR', (0,0), (-1,0), WHITE),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
    ('FONTSIZE', (0,0), (-1,-1), 8.5),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [LGRAY, WHITE]),
    ('GRID', (0,0), (-1,-1), 0.3, colors.HexColor('#d0d4dc')),
    ('TOPPADDING', (0,0), (-1,-1), 5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ('LEFTPADDING', (0,0), (-1,-1), 8),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
]))
story.append(src_table)
story.append(SP(6))

story.append(Paragraph('<b>Dataset Specifications:</b>', bold_style))
spec_data = [
    ['Attribute', 'Detail'],
    ['Total Records', '63,600 daily readings'],
    ['Households', '150 (across 10 Chennai areas)'],
    ['Time Period', 'January 1, 2025 to February 28, 2026 (14 months)'],
    ['Features', '13 columns (9 original + 4 engineered)'],
    ['Income Groups', 'Low (55 HH), Middle (42 HH), High (53 HH)'],
    ['Areas Covered', 'Anna Nagar, T. Nagar, Adyar, Velachery, Tambaram,\nPorur, Chromepet, Perambur, Kodambakkam, Sholinganallur'],
    ['House Types', 'Apartment, Villa, Independent House, Row House'],
    ['Collection Method', 'Synthetic generation based on TANGEDCO norms & IMD data'],
    ['Dataset Limitation', 'Does not capture individual appliance-level metering or\nreal-time smart meter data'],
]
spec_table = Table(spec_data, colWidths=[5*cm, 12*cm])
spec_table.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), BLUE),
    ('TEXTCOLOR', (0,0), (-1,0), WHITE),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTNAME', (0,1), (0,-1), 'Helvetica-Bold'),
    ('FONTNAME', (1,1), (1,-1), 'Helvetica'),
    ('FONTSIZE', (0,0), (-1,-1), 8.5),
    ('TEXTCOLOR', (0,1), (0,-1), GRAY),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [LGRAY, WHITE]),
    ('GRID', (0,0), (-1,-1), 0.3, colors.HexColor('#d0d4dc')),
    ('TOPPADDING', (0,0), (-1,-1), 5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ('LEFTPADDING', (0,0), (-1,-1), 8),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
]))
story.append(spec_table)

story.append(PageBreak())

# ══════════════════════════════════════════════════════════════
# PAGE 2 — PREPROCESSING + EDA
# ══════════════════════════════════════════════════════════════

story.append(Paragraph('3. Data Preprocessing', h1_style))
story.append(HR())

pre_steps = [
    ('3a. Missing Value Handling',
     'All 13 columns were checked for null values. Result: 0 missing values across all 63,600 records. Dataset was complete with no imputation required.'),
    ('3b. Duplicate Removal',
     'Applied df.drop_duplicates() — no duplicate rows were found. All 63,600 records are unique household-date combinations.'),
    ('3c. Data Type Correction',
     'date column converted to datetime64, daily_kwh cast to float64, num_members and year cast to int64 for correct aggregation.'),
    ('3d. Outlier Detection (Z-score)',
     'Applied Z-score method (threshold ±3σ). Mean = 8.40 kWh, Std = 5.74 kWh. Removed 462 outlier records (~0.73%), leaving 63,138 clean rows.'),
]
for title, desc in pre_steps:
    story.append(Paragraph(title, h2_style))
    story.append(Paragraph(desc, body_style))

story.append(Paragraph('3e. Feature Engineering — 4 Derived Columns', h2_style))
feat_data = [
    ['Column', 'Derivation Logic', 'Purpose'],
    ['season', 'Mar–Jun=Summer, Jul–Sep=Monsoon,\nOct–Nov=Post-Monsoon, Dec–Feb=Cool/Winter',
     'Enables seasonal grouping\nand analysis'],
    ['consumption_category', '<5 kWh=Low, 5–12=Medium, >12=High',
     'Classifies households by\nconsumption tier'],
    ['monthly_bill_inr', 'TANGEDCO slab-based formula:\n0-100 units=free, 101-200=Rs1.5/u,\n201-500=Rs3/u, >500=Rs5/u',
     'Real-world cost estimation\nper TANGEDCO tariff'],
    ['peak_season_flag', '1 if season=Summer, else 0',
     'Binary ML feature for\nsummer detection'],
]
feat_table = Table(feat_data, colWidths=[4*cm, 8*cm, 5*cm])
feat_table.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), TEAL),
    ('TEXTCOLOR', (0,0), (-1,0), WHITE),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
    ('FONTSIZE', (0,0), (-1,-1), 8.5),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [LGRAY, WHITE]),
    ('GRID', (0,0), (-1,-1), 0.3, colors.HexColor('#d0d4dc')),
    ('TOPPADDING', (0,0), (-1,-1), 5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ('LEFTPADDING', (0,0), (-1,-1), 8),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
]))
story.append(feat_table)
story.append(SP(10))

# ── SECTION 4: EDA ──
story.append(Paragraph('4. Exploratory Data Analysis', h1_style))
story.append(HR())

story.append(Paragraph('4a. Descriptive Statistics', h2_style))
stat_data = [
    ['Statistic', 'Value', 'Statistic', 'Value'],
    ['Mean', '8.26 kWh/day', 'Median', '6.77 kWh/day'],
    ['Std Deviation', '5.52 kWh/day', 'Min', '1.48 kWh/day'],
    ['Max', '25.63 kWh/day', 'Q1 (25%)', '3.58 kWh/day'],
    ['Q3 (75%)', '11.64 kWh/day', 'IQR', '8.06 kWh/day'],
]
stat_table = Table(stat_data, colWidths=[4*cm, 4.5*cm, 4*cm, 4.5*cm])
stat_table.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), DARK),
    ('TEXTCOLOR', (0,0), (-1,0), WHITE),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTNAME', (0,1), (0,-1), 'Helvetica-Bold'),
    ('FONTNAME', (2,1), (2,-1), 'Helvetica-Bold'),
    ('FONTNAME', (1,1), (1,-1), 'Helvetica'),
    ('FONTNAME', (3,1), (3,-1), 'Helvetica'),
    ('FONTSIZE', (0,0), (-1,-1), 9),
    ('TEXTCOLOR', (0,1), (0,-1), GRAY),
    ('TEXTCOLOR', (2,1), (2,-1), GRAY),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [LGRAY, WHITE]),
    ('GRID', (0,0), (-1,-1), 0.3, colors.HexColor('#d0d4dc')),
    ('TOPPADDING', (0,0), (-1,-1), 5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ('LEFTPADDING', (0,0), (-1,-1), 10),
]))
story.append(stat_table)
story.append(SP(8))

story.append(Paragraph('4b. Trend Analysis — Monthly Consumption', h2_style))
monthly_data = [
    ['Month', 'Avg kWh/day', 'Season', 'Month', 'Avg kWh/day', 'Season'],
    ['Jan 2025', '6.06', 'Cool/Winter', 'Aug 2025', '9.04', 'Monsoon'],
    ['Feb 2025', '7.13', 'Mild', 'Sep 2025', '8.06', 'Post-Monsoon'],
    ['Mar 2025', '10.29', 'Summer', 'Oct 2025', '6.32', 'Post-Monsoon'],
    ['Apr 2025', '11.44', 'Summer', 'Nov 2025', '6.06', 'Cool/Winter'],
    ['May 2025', '11.65 ★', 'Summer (Peak)', 'Dec 2025', '6.23', 'Cool/Winter'],
    ['Jun 2025', '11.10', 'Summer', 'Jan 2026', '6.10', 'Cool/Winter'],
    ['Jul 2025', '9.26', 'Monsoon', 'Feb 2026', '7.13', 'Mild'],
]
m_table = Table(monthly_data, colWidths=[2.7*cm, 3*cm, 3.3*cm, 2.7*cm, 3*cm, 3.3*cm])
m_table.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), DARK),
    ('TEXTCOLOR', (0,0), (-1,0), WHITE),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
    ('FONTSIZE', (0,0), (-1,-1), 8.5),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [LGRAY, WHITE]),
    ('GRID', (0,0), (-1,-1), 0.3, colors.HexColor('#d0d4dc')),
    ('TOPPADDING', (0,0), (-1,-1), 5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ('LEFTPADDING', (0,0), (-1,-1), 8),
]))
story.append(m_table)
story.append(SP(8))

story.append(Paragraph('4c. Correlation Analysis', h2_style))
story.append(Paragraph(
    'Pearson correlation was computed between all numerical features. '
    'Key findings: daily_kwh vs monthly_bill_inr = <b>0.977</b> (very strong — bill is directly derived), '
    'daily_kwh vs peak_season_flag = <b>0.324</b> (moderate — summer drives consumption), '
    'daily_kwh vs num_members = <b>0.276</b> (moderate — larger families use more). '
    'The heatmap visualization (Chart 5) shows the full correlation matrix.',
    body_style))

story.append(Paragraph('4d. Distribution Study', h2_style))
dist_data = [
    ['Category', 'Records', 'Percentage', 'kWh Range'],
    ['Low Consumption', '24,300', '38.5%', '< 5 kWh/day'],
    ['Medium Consumption', '24,123', '38.2%', '5–12 kWh/day'],
    ['High Consumption', '14,715', '23.3%', '> 12 kWh/day'],
]
dist_table = Table(dist_data, colWidths=[5*cm, 3.5*cm, 3.5*cm, 5*cm])
dist_table.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), BLUE),
    ('TEXTCOLOR', (0,0), (-1,0), WHITE),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
    ('FONTSIZE', (0,0), (-1,-1), 9),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [LGRAY, WHITE]),
    ('GRID', (0,0), (-1,-1), 0.3, colors.HexColor('#d0d4dc')),
    ('TOPPADDING', (0,0), (-1,-1), 5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ('LEFTPADDING', (0,0), (-1,-1), 10),
    ('ALIGN', (1,0), (2,-1), 'CENTER'),
]))
story.append(dist_table)

story.append(PageBreak())

# ══════════════════════════════════════════════════════════════
# PAGE 3 — CUSTOM METRIC + ANALYSIS + VISUALIZATIONS
# ══════════════════════════════════════════════════════════════

story.append(Paragraph('5. Custom Analytical Metric — Seasonal Consumption Stress Index (SCSI)', h1_style))
story.append(HR())

story.append(Paragraph('5a. Definition', h2_style))
story.append(Paragraph(
    'The <b>Seasonal Consumption Stress Index (SCSI)</b> is an original metric designed '
    'to quantify how much each month\'s electricity demand deviates from the annual baseline. '
    'A high positive SCSI indicates that the electricity grid is under stress — '
    'demand is significantly above normal — while a negative SCSI indicates a low-demand, '
    'low-stress period.',
    body_style))

story.append(Paragraph('5b. Formula', h2_style))
story.append(Paragraph(
    'SCSI(month) = [ (Month_Avg_kWh - Annual_Avg_kWh) / Annual_Avg_kWh ] x 100',
    formula_style))

story.append(Paragraph('5c. Justification', h2_style))
story.append(Paragraph(
    'Traditional analysis shows absolute kWh values which are hard to compare across '
    'cities or time periods. SCSI normalizes the deviation as a percentage of the annual '
    'average, making it comparable and interpretable regardless of absolute scale. '
    'This is analogous to how financial analysts use percentage change rather than '
    'absolute price to compare stocks.',
    body_style))

story.append(Paragraph('5d. SCSI Results', h2_style))
scsi_vals = [
    ('Jan 2025', '-26.7%', 'Low Stress', 'Cool/Winter'),
    ('Feb 2025', '-13.7%', 'Low Stress', 'Mild'),
    ('Mar 2025', '+24.5%', 'HIGH STRESS', 'Summer'),
    ('Apr 2025', '+38.5%', 'HIGH STRESS', 'Summer'),
    ('May 2025', '+41.0%', 'HIGH STRESS (Peak)', 'Summer'),
    ('Jun 2025', '+34.3%', 'HIGH STRESS', 'Summer'),
    ('Jul 2025', '+12.1%', 'Moderate', 'Monsoon'),
    ('Aug 2025', '+9.4%', 'Moderate', 'Monsoon'),
    ('Sep 2025', '-2.4%', 'Low Stress', 'Post-Monsoon'),
    ('Oct 2025', '-23.5%', 'Low Stress', 'Post-Monsoon'),
    ('Nov 2025', '-26.7%', 'Low Stress', 'Cool/Winter'),
    ('Dec 2025', '-24.6%', 'Low Stress', 'Cool/Winter'),
    ('Jan 2026', '-26.1%', 'Low Stress', 'Cool/Winter'),
    ('Feb 2026', '-13.7%', 'Low Stress', 'Mild'),
]
scsi_header = [['Month', 'SCSI Value', 'Stress Level', 'Season']]
scsi_table_data = scsi_header + [[m, v, s, sea] for m, v, s, sea in scsi_vals]
scsi_table = Table(scsi_table_data, colWidths=[4*cm, 3.5*cm, 5*cm, 4.5*cm])
row_colors = []
for i, (_, _, stress, _) in enumerate(scsi_vals, 1):
    if 'HIGH' in stress: row_colors.append(('BACKGROUND', (0,i), (-1,i), colors.HexColor('#fde8ea')))
    elif 'Moderate' in stress: row_colors.append(('BACKGROUND', (0,i), (-1,i), colors.HexColor('#fef9e7')))
    else: row_colors.append(('BACKGROUND', (0,i), (-1,i), colors.HexColor('#e8f8f3')))

scsi_table.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), DARK),
    ('TEXTCOLOR', (0,0), (-1,0), WHITE),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
    ('FONTSIZE', (0,0), (-1,-1), 8.5),
    ('GRID', (0,0), (-1,-1), 0.3, colors.HexColor('#d0d4dc')),
    ('TOPPADDING', (0,0), (-1,-1), 4),
    ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ('LEFTPADDING', (0,0), (-1,-1), 8),
    ('ALIGN', (1,0), (1,-1), 'CENTER'),
] + row_colors))
story.append(scsi_table)
story.append(SP(6))
story.append(Paragraph(
    '★ May 2025 has the highest SCSI of +41.0%, confirming it as the peak grid stress month '
    'for Chennai. The 4 summer months (Mar–Jun) all exceed the +20% HIGH STRESS threshold.',
    caption_style))
story.append(SP(8))

story.append(Paragraph('6. Analysis Performed', h1_style))
story.append(HR())

analyses = [
    ('Seasonal Pattern Analysis',
     'Monthly averages were computed across all 14 months. Chennai\'s summer peak (March–June) '
     'shows average consumption of 11.12 kWh/day vs 6.18 kWh/day in the cool season — '
     'a 80% difference driven by AC usage in 38–42°C temperatures.'),
    ('Income Level Analysis',
     'High-income households average 14.21 kWh/day vs 3.21 kWh/day for low-income — '
     'a 4.4x gap. This is explained entirely by appliance ownership: high-income homes '
     'own ACs (2+), geysers, dishwashers, and water purifiers; low-income homes own only '
     'fans, a fridge, and lights.'),
    ('Weekend Effect Analysis',
     'Weekday average: 7.90 kWh/day vs Weekend average: 9.18 kWh/day — a consistent '
     '+16.1% uplift. People spending more time at home on Saturdays and Sundays run '
     'ACs, TVs, and appliances for longer hours throughout the day.'),
    ('Area-wise Analysis',
     'Kodambakkam (10.59 kWh/day) leads all areas — likely due to higher income '
     'concentration. Porur (5.82 kWh/day) is the most efficient area. The range '
     'across areas spans from 5.82 to 10.59 kWh/day — an 82% difference.'),
    ('Household Size Analysis',
     'Consumption rises with household size. 5-member homes average 12.1 kWh/day '
     'vs 5.4 kWh/day for single-person homes — a 2.2x difference. More occupants '
     'means simultaneous use of multiple appliances throughout the day.'),
]
for title, desc in analyses:
    story.append(Paragraph(title, h2_style))
    story.append(Paragraph(desc, body_style))

story.append(PageBreak())

# ══════════════════════════════════════════════════════════════
# PAGE 4 — VISUALIZATIONS + ML + INSIGHTS + CONCLUSION
# ══════════════════════════════════════════════════════════════

story.append(Paragraph('7. Visualizations', h1_style))
story.append(HR())
story.append(Paragraph(
    'Seven charts were generated (see outputs/charts.png). Each chart type is used '
    'intentionally to reveal a specific pattern:', body_style))

viz_data = [
    ['Chart', 'Type', 'What It Shows'],
    ['1', 'Line Plot', 'Monthly consumption trend Jan 2025–Feb 2026 with peak and low annotations'],
    ['2', 'Bar Chart', 'Income level vs average daily consumption — shows the 4.4x gap'],
    ['3', 'Boxplot', 'Distribution spread by income group — shows variance and outliers'],
    ['4', 'Scatter Plot', 'Household members vs daily kWh with trend line — shows size effect'],
    ['5', 'Heatmap', 'Correlation matrix of all numerical features'],
    ['6', 'Bar Chart', 'SCSI values by month — custom metric visualization'],
    ['7', 'Boxplot', 'Consumption distribution across 4 Chennai seasons'],
]
viz_table = Table(viz_data, colWidths=[1.5*cm, 3.5*cm, 12*cm])
viz_table.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), DARK),
    ('TEXTCOLOR', (0,0), (-1,0), WHITE),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
    ('FONTSIZE', (0,0), (-1,-1), 9),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [LGRAY, WHITE]),
    ('GRID', (0,0), (-1,-1), 0.3, colors.HexColor('#d0d4dc')),
    ('TOPPADDING', (0,0), (-1,-1), 5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ('LEFTPADDING', (0,0), (-1,-1), 8),
    ('ALIGN', (0,0), (0,-1), 'CENTER'),
]))
story.append(viz_table)
story.append(SP(10))

story.append(Paragraph('8. Machine Learning Model', h1_style))
story.append(HR())
story.append(Paragraph(
    'A <b>Linear Regression</b> model was trained to predict daily electricity '
    'consumption from household and temporal features. The dataset was split '
    '80% training (50,510 samples) and 20% testing (12,628 samples) using '
    'sklearn\'s train_test_split with random_state=42 for reproducibility.',
    body_style))

story.append(Paragraph('Model Performance:', h2_style))
ml_data = [
    ['Metric', 'Value', 'Interpretation'],
    ['R² Score', '0.4585', '46% of consumption variance is explained by the model'],
    ['RMSE', '4.07 kWh/day', 'Average prediction error of ±4.07 kWh per day'],
    ['Training Size', '50,510 records', '80% of cleaned dataset'],
    ['Test Size', '12,628 records', '20% of cleaned dataset'],
]
ml_table = Table(ml_data, colWidths=[4*cm, 4*cm, 9*cm])
ml_table.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), TEAL),
    ('TEXTCOLOR', (0,0), (-1,0), WHITE),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
    ('FONTSIZE', (0,0), (-1,-1), 9),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [LGRAY, WHITE]),
    ('GRID', (0,0), (-1,-1), 0.3, colors.HexColor('#d0d4dc')),
    ('TOPPADDING', (0,0), (-1,-1), 5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ('LEFTPADDING', (0,0), (-1,-1), 8),
]))
story.append(ml_table)
story.append(SP(6))

story.append(Paragraph('Feature Importances (by absolute coefficient):', h2_style))
fi_data = [
    ['Feature', 'Coefficient', 'Impact'],
    ['Peak Season Flag', '+4.13', 'Highest — Summer months increase usage the most'],
    ['Income Level', '-3.58', 'Very high — encoder direction; higher income = more usage'],
    ['Is Weekend', '+1.39', 'High — weekends add ~1.4 kWh/day on average'],
    ['No. of Members', '+0.80', 'Moderate — each extra person adds ~0.8 kWh/day'],
    ['House Type', '-0.12', 'Low — house type has minimal standalone effect'],
    ['Area', '-0.03', 'Minimal — area effect absorbed by income distribution'],
]
fi_table = Table(fi_data, colWidths=[5*cm, 3.5*cm, 8.5*cm])
fi_table.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), BLUE),
    ('TEXTCOLOR', (0,0), (-1,0), WHITE),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
    ('FONTSIZE', (0,0), (-1,-1), 9),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [LGRAY, WHITE]),
    ('GRID', (0,0), (-1,-1), 0.3, colors.HexColor('#d0d4dc')),
    ('TOPPADDING', (0,0), (-1,-1), 5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ('LEFTPADDING', (0,0), (-1,-1), 8),
]))
story.append(fi_table)
story.append(SP(10))

story.append(Paragraph('9. Key Insights & Conclusion', h1_style))
story.append(HR())

insights = [
    ('Seasonal Pattern',
     'May 2025 is Chennai\'s peak consumption month (11.65 kWh/day, SCSI=+41%). '
     'March–June collectively form a HIGH STRESS period with 80% higher consumption '
     'than the cool season (October–January average: 6.18 kWh/day).'),
    ('Income Inequality',
     'The 4.4x consumption gap between High and Low income households is the single '
     'largest differentiator. Policy implication: targeted subsidies for low-income '
     'households have minimal grid impact since they already consume very little.'),
    ('Behavioural Patterns',
     'The consistent +16.1% weekend uplift across all income groups suggests that '
     'occupancy time — not just appliance ownership — is a significant driver.'),
    ('Grid Planning Implication',
     'TANGEDCO should plan for peak load distribution in March–June, particularly '
     'in areas like Kodambakkam (10.59 kWh) where consumption is highest.'),
    ('Model Limitation & Improvement',
     'Linear Regression explains 46% of variance. Upgrading to Random Forest or '
     'Gradient Boosting (estimated R²~75–80%) would capture non-linear interactions '
     'between income, season, and household size.'),
]
for title, desc in insights:
    story.append(Paragraph(f'<b>{title}:</b> {desc}', bullet_style))
    story.append(SP(4))

story.append(SP(8))
story.append(HR())
story.append(Paragraph(
    'This project demonstrates a complete data science workflow — from data collection '
    'and cleaning through EDA, custom metric design, visualization, and machine learning — '
    'applied to a real-world urban energy consumption problem in Chennai, Tamil Nadu.',
    ParagraphStyle('conc', fontSize=9.5, fontName='Helvetica-Oblique',
                   textColor=GRAY, alignment=TA_CENTER, leading=14)))

# ── Footer ──
story.append(SP(10))
footer_data = [['Data Science Project | SRM IST-Ramapuram | Chennai, Tamil Nadu | 2024–25']]
footer_table = Table(footer_data, colWidths=[17*cm])
footer_table.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), DARK),
    ('TEXTCOLOR', (0,0), (-1,-1), WHITE),
    ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
    ('FONTSIZE', (0,0), (-1,-1), 8),
    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ('TOPPADDING', (0,0), (-1,-1), 8),
    ('BOTTOMPADDING', (0,0), (-1,-1), 8),
]))
story.append(footer_table)

doc.build(story)
print("✅ Analytical report saved → outputs/analytical_report.pdf")
