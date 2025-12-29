import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings('ignore')

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 8)
plt.rcParams['font.size'] = 10

# Load data
print("Loading data...")
df_key = pd.read_excel('Mediately Data Scientist.xlsx', sheet_name='Campaign Name Key')
df_raw = pd.read_excel('Mediately Data Scientist.xlsx', sheet_name='RAW DATA')

# Clean data (same as before)
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

df = df_raw.copy()
df['Program'] = df['Campaign name'].map(campaign_mapping)
df['Program'] = df['Program'].fillna(df['Campaign name'])

df['Date'] = pd.to_datetime(df['Reporting starts'])
df['Month'] = df['Date'].dt.month
df['Month_Name'] = df['Date'].dt.strftime('%b')
df['Quarter'] = df['Date'].dt.quarter
df['Week'] = df['Date'].dt.isocalendar().week
df['Year'] = df['Date'].dt.year

df['Link clicks'] = df['Link clicks'].fillna(0)
df['Landing page views'] = df['Landing page views'].fillna(0)
df['Results'] = df['Results'].fillna(0)
df['CPL'] = np.where(df['Results'] > 0, df['Amount spent (USD)'] / df['Results'], np.nan)

df_leads = df[df['Objective'] == 'Leads'].copy()

print(f"Data loaded: {len(df_leads)} records")

# ============================================================================
# PREDICTIVE ANALYSIS 1: Forecast Lead Volume by Month
# ============================================================================
print("\n=== PREDICTIVE ANALYSIS 1: Lead Volume Forecasting ===")

monthly_data = df_leads.groupby(['Month']).agg({
    'Results': 'sum',
    'Amount spent (USD)': 'sum',
    'Link clicks': 'sum',
    'Landing page views': 'sum',
    'CPL': lambda x: x[x.notna()].mean()
}).reset_index()

monthly_data = monthly_data.sort_values('Month')

# Prepare features for forecasting
X = monthly_data[['Month']].values
y_leads = monthly_data['Results'].values
y_cpl = monthly_data['CPL'].fillna(monthly_data['CPL'].mean()).values

# Create future months (next 6 months)
future_months = np.array([[7], [8], [9], [10], [11], [12]])  # Jul-Dec 2025

# Simple linear regression for trend
model_leads = LinearRegression()
model_leads.fit(X, y_leads)
forecast_leads = model_leads.predict(future_months)

model_cpl = LinearRegression()
model_cpl.fit(X, y_cpl)
forecast_cpl = model_cpl.predict(future_months)

# Add seasonality adjustment (based on historical patterns)
seasonal_factors = {
    7: 0.52,  # July - low season
    8: 0.84,  # August
    9: 0.52,  # September - low season
    10: 0.69, # October
    11: 0.55, # November
    12: 1.00  # December - reference
}

forecast_leads_adjusted = forecast_leads * np.array([seasonal_factors[m[0]] for m in future_months])
forecast_cpl_adjusted = forecast_cpl * np.array([1/seasonal_factors[m[0]] for m in future_months])  # Inverse relationship

print("\nForecasted Lead Volume (Next 6 Months):")
month_names = ['Jul 2025', 'Aug 2025', 'Sep 2025', 'Oct 2025', 'Nov 2025', 'Dec 2025']
for i, (month, leads, cpl) in enumerate(zip(month_names, forecast_leads_adjusted, forecast_cpl_adjusted)):
    print(f"{month}: {leads:.0f} leads, CPL: ${cpl:.2f}")

# Visualization
fig, axes = plt.subplots(2, 1, figsize=(14, 10))

# Historical + Forecast Leads
historical_months = monthly_data['Month'].values
historical_leads = monthly_data['Results'].values
all_months = np.concatenate([historical_months, future_months.flatten()])
all_leads = np.concatenate([historical_leads, forecast_leads_adjusted])

axes[0].plot(historical_months, historical_leads, 'o-', label='Historical', linewidth=2, markersize=8)
axes[0].plot(future_months.flatten(), forecast_leads_adjusted, 's--', label='Forecast', linewidth=2, markersize=8, color='red')
axes[0].axvline(x=6, color='gray', linestyle='--', alpha=0.5, label='Forecast Start')
axes[0].set_xlabel('Month (1=Jul, 12=Jun)', fontsize=12)
axes[0].set_ylabel('Lead Volume', fontsize=12)
axes[0].set_title('Lead Volume Forecast - Next 6 Months', fontsize=14, fontweight='bold')
axes[0].legend()
axes[0].grid(True, alpha=0.3)
axes[0].set_xticks(range(1, 13))

# Historical + Forecast CPL
axes[1].plot(historical_months, y_cpl, 'o-', label='Historical', linewidth=2, markersize=8)
axes[1].plot(future_months.flatten(), forecast_cpl_adjusted, 's--', label='Forecast', linewidth=2, markersize=8, color='red')
axes[1].axvline(x=6, color='gray', linestyle='--', alpha=0.5, label='Forecast Start')
axes[1].set_xlabel('Month (1=Jul, 12=Jun)', fontsize=12)
axes[1].set_ylabel('CPL (USD)', fontsize=12)
axes[1].set_title('CPL Forecast - Next 6 Months', fontsize=14, fontweight='bold')
axes[1].legend()
axes[1].grid(True, alpha=0.3)
axes[1].set_xticks(range(1, 13))

plt.tight_layout()
plt.savefig('charts/07_predictive_forecast.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# PREDICTIVE ANALYSIS 2: Program Performance Prediction
# ============================================================================
print("\n=== PREDICTIVE ANALYSIS 2: Program Performance Prediction ===")

program_data = df_leads.groupby('Program').agg({
    'Amount spent (USD)': 'sum',
    'Results': 'sum',
    'Link clicks': 'sum',
    'Landing page views': 'sum',
    'CPL': lambda x: x[x.notna()].mean()
}).reset_index()

program_data['Click_to_Submit_Rate'] = (program_data['Results'] / program_data['Link clicks'] * 100).fillna(0)
program_data['LPV_to_Submit_Rate'] = (program_data['Results'] / program_data['Landing page views'] * 100).fillna(0)
program_data['Historical_CPL'] = program_data['CPL'].fillna(program_data['CPL'].mean())

# Predict future performance based on historical trends
# Assume same spend, predict leads
program_data['Predicted_Leads'] = program_data['Amount spent (USD)'] / program_data['Historical_CPL']
program_data['Predicted_CPL'] = program_data['Historical_CPL'] * 0.9  # Assume 10% improvement with optimization

# Calculate predicted ROI
program_data['Current_ROI'] = program_data['Results'] / program_data['Amount spent (USD)']
program_data['Predicted_ROI'] = program_data['Predicted_Leads'] / program_data['Amount spent (USD)']

print("\nProgram Performance Predictions (with optimization):")
print(program_data[['Program', 'Historical_CPL', 'Predicted_CPL', 'Predicted_Leads', 'Predicted_ROI']].to_string())

# ============================================================================
# PRESCRIPTIVE ANALYSIS 1: Optimal Budget Allocation Model
# ============================================================================
print("\n=== PRESCRIPTIVE ANALYSIS 1: Optimal Budget Allocation ===")

# Load program ROI data
program_roi = pd.read_csv('analysis_results/program_roi.csv')

# Filter out programs with no leads
program_roi_clean = program_roi[program_roi['Efficiency_Score'].notna() & (program_roi['Results'] > 0)].copy()

# Current total budget
current_total_budget = program_roi_clean['Amount spent (USD)'].sum()

# Scenario 1: Maximize Lead Volume (with budget constraint)
# Allocate based on efficiency score
program_roi_clean['Optimal_Budget_Volume'] = (
    program_roi_clean['Efficiency_Score'] / program_roi_clean['Efficiency_Score'].sum() * current_total_budget
)

# Scenario 2: Optimize CPL (reduce average CPL)
# Allocate more to low CPL programs
program_roi_clean['CPL_Inverse'] = 1 / program_roi_clean['CPL']
program_roi_clean['Optimal_Budget_CPL'] = (
    program_roi_clean['CPL_Inverse'] / program_roi_clean['CPL_Inverse'].sum() * current_total_budget
)

# Scenario 3: Balanced approach (weighted by efficiency and conversion rate)
program_roi_clean['Balanced_Score'] = (
    program_roi_clean['Efficiency_Score'] * 0.6 + 
    (program_roi_clean['Click_to_Submit_Rate'] / 100) * 0.4
)
program_roi_clean['Optimal_Budget_Balanced'] = (
    program_roi_clean['Balanced_Score'] / program_roi_clean['Balanced_Score'].sum() * current_total_budget
)

# Calculate predicted outcomes
program_roi_clean['Predicted_Leads_Volume'] = (
    program_roi_clean['Optimal_Budget_Volume'] / program_roi_clean['CPL']
)
program_roi_clean['Predicted_Leads_CPL'] = (
    program_roi_clean['Optimal_Budget_CPL'] / program_roi_clean['CPL']
)
program_roi_clean['Predicted_Leads_Balanced'] = (
    program_roi_clean['Optimal_Budget_Balanced'] / program_roi_clean['CPL']
)

print("\nOptimal Budget Allocation Scenarios:")
print("\nScenario 1: Maximize Lead Volume")
print(program_roi_clean[['Program', 'Amount spent (USD)', 'Optimal_Budget_Volume', 
                         'Predicted_Leads_Volume']].to_string())

print(f"\nTotal Predicted Leads (Volume Scenario): {program_roi_clean['Predicted_Leads_Volume'].sum():.0f}")
print(f"Current Total Leads: {program_roi_clean['Results'].sum():.0f}")
print(f"Improvement: {((program_roi_clean['Predicted_Leads_Volume'].sum() / program_roi_clean['Results'].sum()) - 1) * 100:.1f}%")

print("\nScenario 2: Optimize CPL")
print(program_roi_clean[['Program', 'Amount spent (USD)', 'Optimal_Budget_CPL', 
                         'Predicted_Leads_CPL']].to_string())

print("\nScenario 3: Balanced Approach (Recommended)")
print(program_roi_clean[['Program', 'Amount spent (USD)', 'Optimal_Budget_Balanced', 
                         'Predicted_Leads_Balanced']].to_string())

# Visualization
fig, ax = plt.subplots(figsize=(14, 8))
x = np.arange(len(program_roi_clean))
width = 0.25

ax.bar(x - width, program_roi_clean['Amount spent (USD)'], width, label='Current Budget', alpha=0.8)
ax.bar(x, program_roi_clean['Optimal_Budget_Balanced'], width, label='Optimal Budget (Balanced)', alpha=0.8)
ax.bar(x + width, program_roi_clean['Optimal_Budget_Volume'], width, label='Optimal Budget (Volume)', alpha=0.8)

ax.set_xlabel('Program', fontsize=12)
ax.set_ylabel('Budget (USD)', fontsize=12)
ax.set_title('Optimal Budget Allocation Scenarios', fontsize=14, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels([p[:20] for p in program_roi_clean['Program']], rotation=45, ha='right')
ax.legend()
ax.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('charts/08_optimal_budget_allocation.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# PRESCRIPTIVE ANALYSIS 2: What-If Scenarios
# ============================================================================
print("\n=== PRESCRIPTIVE ANALYSIS 2: What-If Scenarios ===")

scenarios = {
    'Increase Top 3 Programs by 30%': {
        'programs': program_roi_clean.nlargest(3, 'Efficiency_Score')['Program'].tolist(),
        'increase': 1.3
    },
    'Reduce High CPL Programs by 25%': {
        'programs': program_roi_clean.nlargest(3, 'CPL')['Program'].tolist(),
        'increase': 0.75
    },
    'Pause Underperformers, Reallocate': {
        'programs': program_roi_clean.nsmallest(2, 'Efficiency_Score')['Program'].tolist(),
        'increase': 0.0
    }
}

scenario_results = []

for scenario_name, params in scenarios.items():
    scenario_df = program_roi_clean.copy()
    
    # Adjust budgets
    for program in params['programs']:
        mask = scenario_df['Program'] == program
        if params['increase'] == 0.0:
            # Pause - set to 0
            scenario_df.loc[mask, 'Scenario_Budget'] = 0
        else:
            scenario_df.loc[mask, 'Scenario_Budget'] = (
                scenario_df.loc[mask, 'Amount spent (USD)'] * params['increase']
            )
    
    # Reallocate paused budgets to top performers
    if params['increase'] == 0.0:
        paused_budget = scenario_df[scenario_df['Program'].isin(params['programs'])]['Amount spent (USD)'].sum()
        top_programs = scenario_df[~scenario_df['Program'].isin(params['programs'])].nlargest(3, 'Efficiency_Score')
        reallocation_per_program = paused_budget / len(top_programs)
        for program in top_programs['Program']:
            mask = scenario_df['Program'] == program
            scenario_df.loc[mask, 'Scenario_Budget'] = (
                scenario_df.loc[mask, 'Amount spent (USD)'] + reallocation_per_program
            )
    
    # Fill non-adjusted programs
    scenario_df['Scenario_Budget'] = scenario_df['Scenario_Budget'].fillna(
        scenario_df['Amount spent (USD)']
    )
    
    # Calculate predicted leads
    scenario_df['Scenario_Leads'] = scenario_df['Scenario_Budget'] / scenario_df['CPL']
    scenario_df['Scenario_CPL'] = scenario_df['CPL']  # Assume same CPL
    
    total_budget = scenario_df['Scenario_Budget'].sum()
    total_leads = scenario_df['Scenario_Leads'].sum()
    avg_cpl = total_budget / total_leads if total_leads > 0 else np.nan
    
    scenario_results.append({
        'Scenario': scenario_name,
        'Total_Budget': total_budget,
        'Total_Leads': total_leads,
        'Avg_CPL': avg_cpl,
        'Improvement_Leads': ((total_leads / program_roi_clean['Results'].sum()) - 1) * 100,
        'Improvement_CPL': ((program_roi_clean['CPL'].mean() / avg_cpl) - 1) * 100 if not np.isnan(avg_cpl) else 0
    })
    
    print(f"\n{scenario_name}:")
    print(f"  Total Budget: ${total_budget:,.0f}")
    print(f"  Predicted Leads: {total_leads:.0f}")
    print(f"  Average CPL: ${avg_cpl:.2f}")
    print(f"  Lead Improvement: {((total_leads / program_roi_clean['Results'].sum()) - 1) * 100:.1f}%")

scenario_df_results = pd.DataFrame(scenario_results)
scenario_df_results.to_csv('analysis_results/what_if_scenarios.csv', index=False)

# Visualization
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Leads comparison
axes[0].bar(range(len(scenario_results)), [r['Total_Leads'] for r in scenario_results], 
           alpha=0.7, color=['steelblue', 'green', 'orange'])
axes[0].axhline(y=program_roi_clean['Results'].sum(), color='red', linestyle='--', 
               label=f'Current Leads ({program_roi_clean["Results"].sum():.0f})')
axes[0].set_xticks(range(len(scenario_results)))
axes[0].set_xticklabels([r['Scenario'] for r in scenario_results], rotation=15, ha='right')
axes[0].set_ylabel('Total Leads', fontsize=12)
axes[0].set_title('What-If Scenarios: Predicted Lead Volume', fontsize=14, fontweight='bold')
axes[0].legend()
axes[0].grid(True, alpha=0.3, axis='y')

# CPL comparison
axes[1].bar(range(len(scenario_results)), [r['Avg_CPL'] for r in scenario_results], 
           alpha=0.7, color=['steelblue', 'green', 'orange'])
axes[1].axhline(y=program_roi_clean['CPL'].mean(), color='red', linestyle='--', 
               label=f'Current Avg CPL (${program_roi_clean["CPL"].mean():.2f})')
axes[1].set_xticks(range(len(scenario_results)))
axes[1].set_xticklabels([r['Scenario'] for r in scenario_results], rotation=15, ha='right')
axes[1].set_ylabel('Average CPL (USD)', fontsize=12)
axes[1].set_title('What-If Scenarios: Average CPL', fontsize=14, fontweight='bold')
axes[1].legend()
axes[1].grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('charts/09_what_if_scenarios.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# PRESCRIPTIVE ANALYSIS 3: ROI Optimization Model
# ============================================================================
print("\n=== PRESCRIPTIVE ANALYSIS 3: ROI Optimization Model ===")

# Calculate expected ROI for different budget allocations
budget_levels = [0.8, 0.9, 1.0, 1.1, 1.2]  # 80% to 120% of current budget
roi_scenarios = []

for budget_multiplier in budget_levels:
    scenario_budget = program_roi_clean.copy()
    scenario_budget['Allocated_Budget'] = (
        scenario_budget['Optimal_Budget_Balanced'] * budget_multiplier
    )
    scenario_budget['Predicted_Leads'] = (
        scenario_budget['Allocated_Budget'] / scenario_budget['CPL']
    )
    
    total_budget = scenario_budget['Allocated_Budget'].sum()
    total_leads = scenario_budget['Predicted_Leads'].sum()
    avg_cpl = total_budget / total_leads if total_leads > 0 else np.nan
    roi = total_leads / total_budget if total_budget > 0 else 0
    
    roi_scenarios.append({
        'Budget_Multiplier': budget_multiplier,
        'Total_Budget': total_budget,
        'Total_Leads': total_leads,
        'Avg_CPL': avg_cpl,
        'ROI': roi
    })

roi_df = pd.DataFrame(roi_scenarios)
print("\nROI Optimization by Budget Level:")
print(roi_df.to_string(index=False))

roi_df.to_csv('analysis_results/roi_optimization.csv', index=False)

# Visualization
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

axes[0].plot(roi_df['Total_Budget'], roi_df['Total_Leads'], 'o-', linewidth=2, markersize=8)
axes[0].set_xlabel('Total Budget (USD)', fontsize=12)
axes[0].set_ylabel('Total Leads', fontsize=12)
axes[0].set_title('Budget vs. Lead Volume', fontsize=14, fontweight='bold')
axes[0].grid(True, alpha=0.3)

axes[1].plot(roi_df['Total_Budget'], roi_df['ROI'], 'o-', linewidth=2, markersize=8, color='green')
axes[1].set_xlabel('Total Budget (USD)', fontsize=12)
axes[1].set_ylabel('ROI (Leads per Dollar)', fontsize=12)
axes[1].set_title('Budget vs. ROI', fontsize=14, fontweight='bold')
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('charts/10_roi_optimization.png', dpi=300, bbox_inches='tight')
plt.close()

print("\n=== ANALYSIS COMPLETE ===")
print("All predictive and prescriptive analyses saved!")

