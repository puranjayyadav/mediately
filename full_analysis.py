import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
import os

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 8)
plt.rcParams['font.size'] = 10

# Read the Excel file
print("Loading data...")
df_key = pd.read_excel('Mediately Data Scientist.xlsx', sheet_name='Campaign Name Key')
df_raw = pd.read_excel('Mediately Data Scientist.xlsx', sheet_name='RAW DATA')

# Clean the campaign name key
df_key_clean = df_key.iloc[1:, [1, 2]].copy()
df_key_clean.columns = ['Campaign Name', 'Program Name']
df_key_clean = df_key_clean.dropna()

# Create a mapping dictionary - manual mapping based on campaign names
campaign_mapping = {
    'COLLEGE_WW_MSEM_Conversions_Nov24': 'MS in engineering management',
    'COLLEGE_MSO_Conversions_WW_July24': 'Masters of space operations',
    'COLLEGE_MSEM_Conversions_WW_July24': 'MS in engineering management',
    'COLLEGE_BSE_Conversions_WW_July24': 'Bachelors of science in engineering',
    'COLLEGE_MBAA_Conversions_WW_July24': 'MBA Airlines',
    'COLLEGE_Military_Conversions_WW_July24': 'Military focused campaign',
    'COLLEGE_MSM_Conversions_WW_July24': 'MS in management',
    'COLLEGE_BSA_Conversions_WW_July24': 'Bachelors of science in aerospace'
}

# Clean raw data
df = df_raw.copy()
df['Program'] = df['Campaign name'].map(campaign_mapping)
df['Program'] = df['Program'].fillna(df['Campaign name'])

# Parse dates
df['Date'] = pd.to_datetime(df['Reporting starts'])
df['Month'] = df['Date'].dt.month
df['Month_Name'] = df['Date'].dt.strftime('%b')
df['Quarter'] = df['Date'].dt.quarter
df['Week'] = df['Date'].dt.isocalendar().week
df['Year'] = df['Date'].dt.year

# Fill missing values with 0 for calculations
df['Link clicks'] = df['Link clicks'].fillna(0)
df['Landing page views'] = df['Landing page views'].fillna(0)
df['Results'] = df['Results'].fillna(0)

# Calculate CPL (Cost Per Lead)
df['CPL'] = np.where(df['Results'] > 0, df['Amount spent (USD)'] / df['Results'], np.nan)

# Calculate conversion rates
df['Click_to_Submit_Rate'] = np.where(df['Link clicks'] > 0, 
                                       (df['Results'] / df['Link clicks']) * 100, np.nan)
df['LPV_to_Submit_Rate'] = np.where(df['Landing page views'] > 0, 
                                     (df['Results'] / df['Landing page views']) * 100, np.nan)

# Filter to only Leads objective campaigns
df_leads = df[df['Objective'] == 'Leads'].copy()

print(f"\n=== DATA SUMMARY ===")
print(f"Total records: {len(df)}")
print(f"Leads objective records: {len(df_leads)}")
print(f"\nPrograms: {df_leads['Program'].unique()}")
print(f"\nDate range: {df_leads['Date'].min()} to {df_leads['Date'].max()}")

# Create output directory for charts
os.makedirs('charts', exist_ok=True)

# ============================================================================
# QUESTION 1: Seasonality Analysis
# ============================================================================
print("\n=== QUESTION 1: SEASONALITY ANALYSIS ===")

monthly_stats = df_leads.groupby('Month_Name').agg({
    'Results': 'sum',
    'CPL': 'mean',
    'Amount spent (USD)': 'sum'
}).reset_index()

# Order months correctly
month_order = ['Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
monthly_stats['Month_Name'] = pd.Categorical(monthly_stats['Month_Name'], categories=month_order, ordered=True)
monthly_stats = monthly_stats.sort_values('Month_Name')

print("\nMonthly Lead Volume:")
print(monthly_stats[['Month_Name', 'Results']])
print("\nMonthly Average CPL:")
print(monthly_stats[['Month_Name', 'CPL']])

# Visualization for seasonality
fig, axes = plt.subplots(2, 1, figsize=(14, 10))

# Lead volume by month
axes[0].plot(monthly_stats['Month_Name'], monthly_stats['Results'], marker='o', linewidth=2, markersize=8)
axes[0].set_title('Lead Volume by Month (FY2024)', fontsize=14, fontweight='bold')
axes[0].set_xlabel('Month', fontsize=12)
axes[0].set_ylabel('Total Leads', fontsize=12)
axes[0].grid(True, alpha=0.3)
axes[0].tick_params(axis='x', rotation=45)

# CPL by month
axes[1].plot(monthly_stats['Month_Name'], monthly_stats['CPL'], marker='o', linewidth=2, markersize=8, color='orange')
axes[1].set_title('Average Cost Per Lead (CPL) by Month (FY2024)', fontsize=14, fontweight='bold')
axes[1].set_xlabel('Month', fontsize=12)
axes[1].set_ylabel('Average CPL (USD)', fontsize=12)
axes[1].grid(True, alpha=0.3)
axes[1].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig('charts/01_seasonality_analysis.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# QUESTION 2: Click to Submit Conversion Rate
# ============================================================================
print("\n=== QUESTION 2: CLICK TO SUBMIT CONVERSION RATE ===")

total_clicks = df_leads['Link clicks'].sum()
total_submits = df_leads['Results'].sum()
click_to_submit_rate = (total_submits / total_clicks * 100) if total_clicks > 0 else 0

print(f"\nTotal Link Clicks: {total_clicks:,.0f}")
print(f"Total RFI Submits: {total_submits:,.0f}")
print(f"Click-to-Submit Conversion Rate: {click_to_submit_rate:.2f}%")

# By program
program_click_rates = df_leads.groupby('Program').agg({
    'Link clicks': 'sum',
    'Results': 'sum'
}).reset_index()
program_click_rates['Conversion_Rate'] = (program_click_rates['Results'] / program_click_rates['Link clicks'] * 100).round(2)
program_click_rates = program_click_rates.sort_values('Conversion_Rate', ascending=False)

print("\nClick-to-Submit Rate by Program:")
print(program_click_rates[['Program', 'Link clicks', 'Results', 'Conversion_Rate']])

# Visualization
fig, ax = plt.subplots(figsize=(12, 6))
bars = ax.barh(program_click_rates['Program'], program_click_rates['Conversion_Rate'], color='steelblue')
ax.set_xlabel('Conversion Rate (%)', fontsize=12)
ax.set_title('Click-to-Submit Conversion Rate by Program', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3, axis='x')

# Add value labels
for i, (idx, row) in enumerate(program_click_rates.iterrows()):
    ax.text(row['Conversion_Rate'] + 0.1, i, f"{row['Conversion_Rate']:.2f}%", 
            va='center', fontsize=10)

plt.tight_layout()
plt.savefig('charts/02_click_to_submit_rate.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# QUESTION 3: Landing Page View to Submit Conversion Rate
# ============================================================================
print("\n=== QUESTION 3: LANDING PAGE VIEW TO SUBMIT CONVERSION RATE ===")

total_lpv = df_leads['Landing page views'].sum()
lpv_to_submit_rate = (total_submits / total_lpv * 100) if total_lpv > 0 else 0

print(f"\nTotal Landing Page Views: {total_lpv:,.0f}")
print(f"Total RFI Submits: {total_submits:,.0f}")
print(f"LPV-to-Submit Conversion Rate: {lpv_to_submit_rate:.2f}%")

# By program
program_lpv_rates = df_leads.groupby('Program').agg({
    'Landing page views': 'sum',
    'Results': 'sum'
}).reset_index()
program_lpv_rates['Conversion_Rate'] = (program_lpv_rates['Results'] / program_lpv_rates['Landing page views'] * 100).round(2)
program_lpv_rates = program_lpv_rates.sort_values('Conversion_Rate', ascending=False)

print("\nLPV-to-Submit Rate by Program:")
print(program_lpv_rates[['Program', 'Landing page views', 'Results', 'Conversion_Rate']])

# Visualization
fig, ax = plt.subplots(figsize=(12, 6))
bars = ax.barh(program_lpv_rates['Program'], program_lpv_rates['Conversion_Rate'], color='green')
ax.set_xlabel('Conversion Rate (%)', fontsize=12)
ax.set_title('Landing Page View-to-Submit Conversion Rate by Program', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3, axis='x')

# Add value labels
for i, (idx, row) in enumerate(program_lpv_rates.iterrows()):
    ax.text(row['Conversion_Rate'] + 0.1, i, f"{row['Conversion_Rate']:.2f}%", 
            va='center', fontsize=10)

plt.tight_layout()
plt.savefig('charts/03_lpv_to_submit_rate.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# QUESTION 4: Underperforming Programs Analysis
# ============================================================================
print("\n=== QUESTION 4: UNDERPERFORMING PROGRAMS ANALYSIS ===")

program_performance = df_leads.groupby('Program').agg({
    'Amount spent (USD)': 'sum',
    'Results': 'sum',
    'CPL': lambda x: x[x.notna()].mean(),
    'Link clicks': 'sum',
    'Landing page views': 'sum',
    'Impressions': 'sum'
}).reset_index()

program_performance['Click_to_Submit_Rate'] = (program_performance['Results'] / program_performance['Link clicks'] * 100).round(2)
program_performance['LPV_to_Submit_Rate'] = (program_performance['Results'] / program_performance['Landing page views'] * 100).round(2)
program_performance['CTR'] = (program_performance['Link clicks'] / program_performance['Impressions'] * 100).round(3)
program_performance['CPL'] = program_performance['CPL'].round(2)

# Calculate percentiles for categorization
cpl_median = program_performance['CPL'].median()
cpl_75th = program_performance['CPL'].quantile(0.75)
conversion_median = program_performance['Click_to_Submit_Rate'].median()
conversion_25th = program_performance['Click_to_Submit_Rate'].quantile(0.25)

# Categorize programs
def categorize_program(row):
    if pd.isna(row['CPL']) or row['Results'] == 0:
        return 'No Leads'
    elif row['CPL'] > cpl_75th and row['Click_to_Submit_Rate'] < conversion_25th:
        return 'Underperforming'
    elif row['CPL'] > cpl_median:
        return 'High CPL'
    elif row['Click_to_Submit_Rate'] < conversion_median:
        return 'Low Conversion'
    else:
        return 'Performing Well'

program_performance['Category'] = program_performance.apply(categorize_program, axis=1)
program_performance = program_performance.sort_values('CPL', ascending=False)

print("\nProgram Performance Summary:")
print(program_performance[['Program', 'Amount spent (USD)', 'Results', 'CPL', 
                           'Click_to_Submit_Rate', 'Category']].to_string())

underperforming = program_performance[program_performance['Category'].isin(['Underperforming', 'High CPL', 'Low Conversion', 'No Leads'])]
print("\n\nUnderperforming Programs:")
print(underperforming[['Program', 'Category', 'CPL', 'Click_to_Submit_Rate', 'Results']].to_string())

# Visualization
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# CPL vs Conversion Rate scatter
colors = {'Underperforming': 'red', 'High CPL': 'orange', 'Low Conversion': 'yellow', 
          'Performing Well': 'green', 'No Leads': 'gray'}
for category in program_performance['Category'].unique():
    subset = program_performance[program_performance['Category'] == category]
    axes[0].scatter(subset['Click_to_Submit_Rate'], subset['CPL'], 
                   label=category, s=200, alpha=0.7, c=colors.get(category, 'blue'))
    for idx, row in subset.iterrows():
        axes[0].annotate(row['Program'][:20], 
                        (row['Click_to_Submit_Rate'], row['CPL']),
                        fontsize=8, alpha=0.7)

axes[0].axhline(y=cpl_median, color='gray', linestyle='--', alpha=0.5, label=f'Median CPL: ${cpl_median:.2f}')
axes[0].axvline(x=conversion_median, color='gray', linestyle='--', alpha=0.5, label=f'Median Conversion: {conversion_median:.2f}%')
axes[0].set_xlabel('Click-to-Submit Conversion Rate (%)', fontsize=12)
axes[0].set_ylabel('Cost Per Lead (USD)', fontsize=12)
axes[0].set_title('Program Performance: CPL vs Conversion Rate', fontsize=14, fontweight='bold')
axes[0].legend()
axes[0].grid(True, alpha=0.3)

# CPL by program
program_performance_sorted = program_performance.sort_values('CPL', ascending=True)
bars = axes[1].barh(program_performance_sorted['Program'], program_performance_sorted['CPL'],
                    color=[colors.get(cat, 'blue') for cat in program_performance_sorted['Category']])
axes[1].set_xlabel('Cost Per Lead (USD)', fontsize=12)
axes[1].set_title('Cost Per Lead by Program', fontsize=14, fontweight='bold')
axes[1].grid(True, alpha=0.3, axis='x')

plt.tight_layout()
plt.savefig('charts/04_underperforming_programs.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# QUESTION 5: Trends Analysis - Ad Engagements vs Leads
# ============================================================================
print("\n=== QUESTION 5: TRENDS ANALYSIS ===")

# Aggregate by week to see trends
weekly_data = df_leads.groupby('Week').agg({
    'Link clicks': 'sum',
    'Landing page views': 'sum',
    'Results': 'sum',
    'Amount spent (USD)': 'sum'
}).reset_index()

# Calculate lagged correlations
weekly_data['Clicks_Lag1'] = weekly_data['Link clicks'].shift(1)
weekly_data['LPV_Lag1'] = weekly_data['Landing page views'].shift(1)
weekly_data['Clicks_Lag2'] = weekly_data['Link clicks'].shift(2)
weekly_data['LPV_Lag2'] = weekly_data['Landing page views'].shift(2)

# Calculate correlations
corr_clicks_lag1 = weekly_data[['Clicks_Lag1', 'Results']].corr().iloc[0, 1]
corr_clicks_lag2 = weekly_data[['Clicks_Lag2', 'Results']].corr().iloc[0, 1]
corr_lpv_lag1 = weekly_data[['LPV_Lag1', 'Results']].corr().iloc[0, 1]
corr_lpv_lag2 = weekly_data[['LPV_Lag2', 'Results']].corr().iloc[0, 1]

print(f"\nCorrelation Analysis:")
print(f"Clicks (1 week lag) vs Leads: {corr_clicks_lag1:.3f}")
print(f"Clicks (2 week lag) vs Leads: {corr_clicks_lag2:.3f}")
print(f"LPV (1 week lag) vs Leads: {corr_lpv_lag1:.3f}")
print(f"LPV (2 week lag) vs Leads: {corr_lpv_lag2:.3f}")

# Monthly trend analysis
monthly_trends = df_leads.groupby(['Month_Name']).agg({
    'Link clicks': 'sum',
    'Landing page views': 'sum',
    'Results': 'sum',
    'Amount spent (USD)': 'sum'
}).reset_index()
monthly_trends['Month_Name'] = pd.Categorical(monthly_trends['Month_Name'], categories=month_order, ordered=True)
monthly_trends = monthly_trends.sort_values('Month_Name')

# Calculate lagged values
monthly_trends['Clicks_Lag1'] = monthly_trends['Link clicks'].shift(1)
monthly_trends['Results_Current'] = monthly_trends['Results']

# Visualization
fig, axes = plt.subplots(2, 1, figsize=(14, 10))

# Clicks vs Leads trend
ax1 = axes[0]
ax1_twin = ax1.twinx()
line1 = ax1.plot(monthly_trends['Month_Name'], monthly_trends['Link clicks'], 
                marker='o', label='Link Clicks', color='blue', linewidth=2)
line2 = ax1_twin.plot(monthly_trends['Month_Name'], monthly_trends['Results'], 
                     marker='s', label='Leads', color='red', linewidth=2)
ax1.set_xlabel('Month', fontsize=12)
ax1.set_ylabel('Link Clicks', fontsize=12, color='blue')
ax1_twin.set_ylabel('Leads', fontsize=12, color='red')
ax1.set_title('Monthly Trend: Link Clicks vs Leads', fontsize=14, fontweight='bold')
ax1.tick_params(axis='x', rotation=45)
ax1.grid(True, alpha=0.3)
lines = line1 + line2
labels = [l.get_label() for l in lines]
ax1.legend(lines, labels, loc='upper left')

# LPV vs Leads trend
ax2 = axes[1]
ax2_twin = ax2.twinx()
line3 = ax2.plot(monthly_trends['Month_Name'], monthly_trends['Landing page views'], 
                marker='o', label='Landing Page Views', color='green', linewidth=2)
line4 = ax2_twin.plot(monthly_trends['Month_Name'], monthly_trends['Results'], 
                     marker='s', label='Leads', color='red', linewidth=2)
ax2.set_xlabel('Month', fontsize=12)
ax2.set_ylabel('Landing Page Views', fontsize=12, color='green')
ax2_twin.set_ylabel('Leads', fontsize=12, color='red')
ax2.set_title('Monthly Trend: Landing Page Views vs Leads', fontsize=14, fontweight='bold')
ax2.tick_params(axis='x', rotation=45)
ax2.grid(True, alpha=0.3)
lines = line3 + line4
labels = [l.get_label() for l in lines]
ax2.legend(lines, labels, loc='upper left')

plt.tight_layout()
plt.savefig('charts/05_engagement_trends.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# QUESTION 6: Budget Allocation Recommendations
# ============================================================================
print("\n=== QUESTION 6: BUDGET ALLOCATION RECOMMENDATIONS ===")

# Calculate ROI metrics
program_roi = program_performance.copy()
program_roi['Leads_per_Dollar'] = program_roi['Results'] / program_roi['Amount spent (USD)']
program_roi['Efficiency_Score'] = (program_roi['Click_to_Submit_Rate'] / 100) * (1 / program_roi['CPL']) * 1000
program_roi = program_roi.sort_values('Efficiency_Score', ascending=False)

print("\nProgram Efficiency Ranking:")
print(program_roi[['Program', 'CPL', 'Click_to_Submit_Rate', 'Leads_per_Dollar', 'Efficiency_Score', 'Category']].to_string())

# Visualization
fig, ax = plt.subplots(figsize=(12, 6))
bars = ax.barh(program_roi['Program'], program_roi['Efficiency_Score'], 
               color=[colors.get(cat, 'blue') for cat in program_roi['Category']])
ax.set_xlabel('Efficiency Score', fontsize=12)
ax.set_title('Program Efficiency Score (Higher = Better ROI)', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3, axis='x')

plt.tight_layout()
plt.savefig('charts/06_budget_allocation.png', dpi=300, bbox_inches='tight')
plt.close()

# Save all analysis results
print("\n=== SAVING ANALYSIS RESULTS ===")
os.makedirs('analysis_results', exist_ok=True)
monthly_stats.to_csv('analysis_results/monthly_stats.csv', index=False)
program_click_rates.to_csv('analysis_results/program_click_rates.csv', index=False)
program_lpv_rates.to_csv('analysis_results/program_lpv_rates.csv', index=False)
program_performance.to_csv('analysis_results/program_performance.csv', index=False)
program_roi.to_csv('analysis_results/program_roi.csv', index=False)
weekly_data.to_csv('analysis_results/weekly_trends.csv', index=False)
monthly_trends.to_csv('analysis_results/monthly_trends.csv', index=False)

print("\nAnalysis complete! All charts and data saved.")

