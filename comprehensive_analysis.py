import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

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

# Create a mapping dictionary
campaign_to_program = {}
for idx, row in df_key_clean.iterrows():
    campaign_name = str(row['Campaign Name']).strip()
    program_name = str(row['Program Name']).strip()
    campaign_to_program[campaign_name] = program_name

# Clean raw data
df = df_raw.copy()

# Add program name
df['Program'] = df['Campaign name'].map(campaign_to_program)
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

print(f"\nTotal records: {len(df)}")
print(f"Leads objective records: {len(df_leads)}")
print(f"\nPrograms: {df_leads['Program'].unique()}")

# Save cleaned data
df_leads.to_csv('cleaned_campaign_data.csv', index=False)
print("\nCleaned data saved to cleaned_campaign_data.csv")

