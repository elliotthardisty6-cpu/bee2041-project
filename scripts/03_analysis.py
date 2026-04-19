# scripts/03_analysis.py
# OLS: does wage bill predict points?
 
import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
import os
 
os.makedirs('figures', exist_ok=True)
 
df = pd.read_csv('data/cleaned/pl_merged.csv')
 
# model 1 - simple
model1 = smf.ols('Pts ~ annual_wages_millions', data=df).fit()
 
print('=' * 55)
print('REGRESSION RESULTS: Points ~ Annual Wages')
print('=' * 55)
print(model1.summary())
 
# key stats
coef = model1.params['annual_wages_millions']
r2   = model1.rsquared
pval = model1.pvalues['annual_wages_millions']
sig  = 'YES (p < 0.05)' if pval < 0.05 else 'NO (p >= 0.05)'
 
print('\n--- KEY NUMBERS FOR YOUR BLOG ---')
print(f'For each extra £1m in wages: +{coef:.2f} points')
print(f'R-squared: {r2:.3f}  (wages explain {r2*100:.1f}% of points variation)')
print(f'Statistically significant: {sig}')
 
# model 2 - with control var
model2 = smf.ols('Pts ~ annual_wages_millions + goal_diff',
                  data=df).fit()
print('\n' + '=' * 55)
print('MODEL 2: Points ~ Wages + Goal Difference')
print('=' * 55)
print(model2.summary())
 
# residuals - value for money
df['predicted_pts'] = model1.predict(df)
df['residual']      = df['Pts'] - df['predicted_pts']
 
print('\n--- VALUE FOR MONEY RANKINGS ---')
print('Positive = got MORE points than wages predicted')
print('Negative = got FEWER points than wages predicted')
print(df[['Squad','Pts','annual_wages_millions',
          'predicted_pts','residual']]
      .sort_values('residual', ascending=False)
      .round(1).to_string(index=False))
 
# save for plots
df.to_csv('data/cleaned/pl_with_residuals.csv', index=False)
print('\nSaved to data/cleaned/pl_with_residuals.csv')
