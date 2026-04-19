# scripts/02_clean.py
# merge stats + wages, make new columns
 
import pandas as pd
import numpy as np
import os
 
os.makedirs('data/cleaned', exist_ok=True)
 
# load
standings = pd.read_csv('data/raw/fbref_standings.csv')
wages     = pd.read_csv('data/raw/wages.csv')
 
# trim columns
cols = ['Squad','MP','W','D','L','GF','GA','Pts','xG']
cols = [c for c in cols if c in standings.columns]
standings = standings[cols].copy()
 
# fix dtypes
for col in ['MP','W','D','L','GF','GA','Pts','xG']:
    if col in standings.columns:
        standings[col] = pd.to_numeric(standings[col], errors='coerce')
 
# clean up
standings = standings.dropna(subset=['Squad'])
standings['Squad'] = standings['Squad'].str.strip()
wages['Squad']     = wages['Squad'].str.strip()
 
# join on club name
merged = standings.merge(wages, on='Squad', how='inner')
 
# check for mismatches
unmatched = set(standings['Squad']) - set(merged['Squad'])
if unmatched:
    print('WARNING: These clubs did not match:', unmatched)
 
# new vars
merged['goal_diff']       = merged['GF'] - merged['GA']
merged['pts_per_million'] = merged['Pts'] / merged['annual_wages_millions']
merged['win_rate']        = merged['W'] / merged['MP']
 
if 'xG' in merged.columns:
    merged['finishing'] = merged['GF'] - merged['xG']
 
# save
merged.to_csv('data/cleaned/pl_merged.csv', index=False)
print(f'Done! Saved {len(merged)} clubs to data/cleaned/pl_merged.csv')
print(merged[['Squad','Pts','annual_wages_millions','pts_per_million']]
      .sort_values('Pts', ascending=False).to_string(index=False))
