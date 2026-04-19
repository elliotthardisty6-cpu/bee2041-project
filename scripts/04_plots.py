# scripts/04_plots.py
# Creates all 5 charts for the blog post
 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
import os
 
os.makedirs('figures', exist_ok=True)
df = pd.read_csv('data/cleaned/pl_with_residuals.csv')
 
# colours
col_blue  = '#2563A8'
col_red   = '#C0392B'
col_grey  = '#7F8C8D'
col_green = '#27AE60'
 
# styling
plt.rcParams.update({'font.family':'sans-serif','font.size':11,
                     'axes.spines.top':False,'axes.spines.right':False})
 
 
# chart 1 - scatter
fig, ax = plt.subplots(figsize=(10,6))
ax.scatter(df['annual_wages_millions'], df['Pts'],
           color=col_blue, s=80, zorder=3)
 
# add labels
for _, row in df.iterrows():
    ax.annotate(row['Squad'],
                (row['annual_wages_millions'], row['Pts']),
                textcoords='offset points', xytext=(5,3),
                fontsize=8, color='#333')
 
# regression line
model = smf.ols('Pts ~ annual_wages_millions', data=df).fit()
x_range = np.linspace(df['annual_wages_millions'].min(),
                       df['annual_wages_millions'].max(), 100)
y_pred = (model.params['Intercept']
          + model.params['annual_wages_millions'] * x_range)
ax.plot(x_range, y_pred, color=col_red, linewidth=2,
        linestyle='--', label='Regression line')
 
ax.set_xlabel('Annual Wage Bill (£ millions)', fontsize=12)
ax.set_ylabel('League Points', fontsize=12)
ax.set_title('Wage Spending vs League Points — Premier League 2023/24',
             fontsize=13, fontweight='bold')
ax.text(0.05, 0.95, f'R² = {model.rsquared:.2f}',
        transform=ax.transAxes, fontsize=10, color=col_red, va='top')
ax.legend(fontsize=10)
fig.tight_layout()
fig.savefig('figures/01_wages_vs_points.png', dpi=150)
print('Saved chart 1')
plt.close()
 
 
# chart 2 - residuals
df2 = df.sort_values('residual', ascending=True)
colours = [col_green if r > 0 else col_red for r in df2['residual']]
fig, ax = plt.subplots(figsize=(10,7))
ax.barh(df2['Squad'], df2['residual'], color=colours, edgecolor='white')
ax.axvline(0, color='black', linewidth=0.8)
ax.set_xlabel('Points above/below model prediction', fontsize=12)
ax.set_title('Value for Money: Over- and Under-Performers\n'
             '(Green = outperformed wage-based prediction)',
             fontsize=12, fontweight='bold')
fig.tight_layout()
fig.savefig('figures/02_value_for_money.png', dpi=150)
print('Saved chart 2')
plt.close()
 
 
# chart 3
df3 = df.sort_values('annual_wages_millions', ascending=False)
fig, ax = plt.subplots(figsize=(10,6))
ax.bar(df3['Squad'], df3['annual_wages_millions'],
       color=col_blue, edgecolor='white')
ax.set_xticklabels(df3['Squad'], rotation=45, ha='right', fontsize=9)
ax.set_ylabel('Annual Wage Bill (£ millions)', fontsize=12)
ax.set_title('Premier League 2023/24 — Wage Bills by Club',
             fontsize=13, fontweight='bold')
fig.tight_layout()
fig.savefig('figures/03_wage_bills.png', dpi=150)
print('Saved chart 3')
plt.close()
 
 
# chart 4
df4 = df.sort_values('pts_per_million', ascending=False)
colours4 = [col_green if i<5 else (col_red if i>=15 else col_grey)
            for i in range(len(df4))]
fig, ax = plt.subplots(figsize=(10,6))
ax.bar(df4['Squad'], df4['pts_per_million'],
       color=colours4, edgecolor='white')
ax.set_xticklabels(df4['Squad'], rotation=45, ha='right', fontsize=9)
ax.set_ylabel('Points per £1 million of wages', fontsize=12)
ax.set_title('Efficiency: Points Per £1 Million Spent on Wages',
             fontsize=13, fontweight='bold')
ax.text(0.02, 0.95, 'Green = top 5 most efficient',
        transform=ax.transAxes, color=col_green, fontsize=9)
ax.text(0.02, 0.89, 'Red = bottom 5 least efficient',
        transform=ax.transAxes, color=col_red, fontsize=9)
fig.tight_layout()
fig.savefig('figures/04_points_per_million.png', dpi=150)
print('Saved chart 4')
plt.close()
 
 
# chart 5
fig, ax = plt.subplots(figsize=(8,5))
ax.hist(df['residual'], bins=10, color=col_blue,
        edgecolor='white', alpha=0.85)
ax.axvline(0, color=col_red, linewidth=1.5, linestyle='--')
ax.set_xlabel('Residual (actual minus predicted points)', fontsize=12)
ax.set_ylabel('Number of clubs', fontsize=12)
ax.set_title('Distribution of Residuals', fontsize=13, fontweight='bold')
fig.tight_layout()
fig.savefig('figures/05_residuals.png', dpi=150)
print('Saved chart 5')
plt.close()
 
print('\nAll 5 charts saved to figures/')
