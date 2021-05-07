# -*- coding: utf-8 -*-
"""
Created on Wed May  5 07:29:29 2021

@author: andre
"""

import pandas as pd
import seaborn as sns

# %%
# Creating a single data frame from all of the data downloaded and organized in the previous script.
# ----------------------------------------------------------------------------

run_control = pd.read_csv("run_control.csv", dtype=str)

all_counties = pd.DataFrame()

# Pulling each .csv file out of the output folder according to its name and stacking them all up.
for index, row in run_control.iterrows():
    
    state = row['po_code']
    year = row['year']
    region = row['region']
    
    var_types = {'county_code':str,
                 'total_purchases':int,
                 'total_population':int,
                 'black_population':int,
                 'med_hh_income':int,
                 'black_hh_income':int,
                 'med_monthly_costs_w_mortgage':int,
                 'med_home_value':int}
    
    current_state = pd.read_csv(f'output/{state}{year}.csv', dtype=var_types, na_values= -666666666)
    current_state['year'] = int(year)
    current_state['region'] = region
    
    all_counties = all_counties.append(current_state, ignore_index=True)

all_counties = all_counties.set_index('county_code')



# Removing improbable outlier, Fulton County Illinois. Median Black income > $250k
all_counties = all_counties.drop(['17057'])

# Slicing up for analysis

is_high_county = all_counties['rate_ratio'] > 0.9
is_low_county = all_counties['rate_ratio'] < 0.5
is_south = all_counties['region'] == "South"
is_midwest = all_counties['region'] == "Midwest"
is_northeast = all_counties['region'] == "Northeast"
is_west = all_counties['region'] == "West"

high_counties = all_counties[is_high_county]
low_counties = all_counties[is_low_county]
south_counties = all_counties[is_south]
midwest_counties = all_counties[is_midwest]
northeast_counties = all_counties[is_northeast]
west_counties = all_counties[is_west]

by_region = all_counties.groupby('region')
high_by_region = high_counties.groupby('region')
low_by_region = low_counties.groupby('region')

summary = by_region.mean()
high_summary = high_by_region.mean()
low_summary = low_by_region.mean()

# %%
# Visualizations
# ----------------------------------------------------------------------------

# Questions:
# How are scores distributed overall, by region?

# How are scores related to med. home value, pct. single unit, med. income, med. black income, monthly costs
sns.set_style()
scatter1 = sns.scatterplot(data=all_counties,
                x='med_home_value',
                y='rate_ratio',
                size='total_population',
                sizes=(5,2000),
                hue='region',
                alpha=0.5)
scatter1.legend(fontsize=12, bbox_to_anchor=(1,1))




sns.set_style()
scatter2 = sns.scatterplot(data=all_counties,
                x='pct_single_unit',
                y='rate_ratio',
                size='total_population',
                sizes=(5,2000),
                hue='region',
                alpha=0.5)
scatter2.legend(fontsize=12, bbox_to_anchor=(1,1))


sns.set_style()
scatter3 = sns.scatterplot(data=all_counties,
                x='med_black_hh_income',
                y='rate_ratio',
                size='total_population',
                sizes=(5,2000),
                hue='region',
                alpha=0.5)
scatter3.legend(fontsize=12, bbox_to_anchor=(1,1))


sns.set_style()
scatter4 = sns.scatterplot(data=all_counties,
                x='med_hh_income',
                y='rate_ratio',
                size='total_population',
                sizes=(5,2000),
                hue='region',
                alpha=0.5)
scatter4.legend(fontsize=12, bbox_to_anchor=(1,1))


sns.set_style()
scatter5 = sns.scatterplot(data=high_counties,
                x='med_black_hh_income',
                y='rate_ratio',
                size='total_population',
                sizes=(5,2000),
                hue='region',
                alpha=0.5)
scatter5.legend(fontsize=12, bbox_to_anchor=(1,1))

sns.kdeplot(data=all_counties,
            x='rate_ratio',
            hue='region',
            fill=True,
            alpha=0.5)

