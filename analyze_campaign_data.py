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

# Read the Excel file
print("Loading data...")
df_key = pd.read_excel('Mediately Data Scientist.xlsx', sheet_name='Campaign Name Key')
df_raw = pd.read_excel('Mediately Data Scientist.xlsx', sheet_name='RAW DATA')

print(f"\nCampaign Name Key shape: {df_key.shape}")
print(f"RAW DATA shape: {df_raw.shape}")

# Display the key mapping
print("\n=== Campaign Name Key ===")
print(df_key.head(20))

# Display raw data info
print("\n=== RAW DATA Info ===")
print(df_raw.info())
print("\n=== RAW DATA Head ===")
print(df_raw.head(20))
print("\n=== RAW DATA Sample ===")
print(df_raw.sample(10))

# Check for missing values
print("\n=== Missing Values ===")
print(df_raw.isnull().sum())

# Check unique values in key columns
print("\n=== Unique Campaign Names ===")
print(df_raw['Campaign name'].value_counts().head(20))

print("\n=== Unique Objectives ===")
print(df_raw['Objective'].value_counts())

print("\n=== Date Range ===")
print(f"Start: {df_raw['Reporting starts'].min()}")
print(f"End: {df_raw['Reporting ends'].max()}")

