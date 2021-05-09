# -*- coding: utf-8 -*-
"""
Created on Wed May  5 07:29:29 2021

@author: andre
"""

# This script produces a single data frame from all the .csv files created in the previous script.
# It then produces one example of a visualization (bubble plot) that can be created with this data.

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import itertools

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

all_counties['med_home_value_thous'] = all_counties['med_home_value'] / 1000

# Removing improbable outlier, Fulton County Illinois. Median Black income > $250k and no Black home purchases.

all_counties = all_counties.drop(['17057'])

# Slicing up by region for analysis

is_south = all_counties['region'] == "South"
is_midwest = all_counties['region'] == "Midwest"
is_northeast = all_counties['region'] == "Northeast"
is_west = all_counties['region'] == "West"

south_counties = all_counties[is_south]
midwest_counties = all_counties[is_midwest]
northeast_counties = all_counties[is_northeast]
west_counties = all_counties[is_west]

by_region = all_counties.groupby('region')

print(by_region[['rate_ratio','med_home_value_thous']].median())

# %%
# Visualizations
# ----------------------------------------------------------------------------

# Creating a scatterplot of county bubbles, faceted by region.
# X-axis is median home value in thousands of dollars.
# Y-axis is Black new home purchase ratio.
# Size of bubbles is proportionate to the county's total population.

sns.set_style()
sns.set_palette("deep")
palette = itertools.cycle(sns.color_palette())

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2,2)

sns.scatterplot(data=midwest_counties,
                x='med_home_value_thous',
                y='rate_ratio',
                ax=ax1,
                size='total_population',
                sizes=(5,3000),
                color=next(palette),
                legend=None,
                alpha=0.5 )
ax1.set_title("Midwest")
ax1.set_xlabel(None)
ax1.set_ylabel(None)
ax1.set_xlim(0,1000)

sns.scatterplot(data=northeast_counties,
                x='med_home_value_thous',
                y='rate_ratio',
                ax=ax2,
                size='total_population',
                sizes=(5,3000),
                color=next(palette),
                legend=None,
                alpha=0.5 )
ax2.set_title("Northeast")
ax2.set_xlabel(None)
ax2.set_ylabel(None)
ax2.set_xlim(0,1000)

sns.scatterplot(data=west_counties,
                x='med_home_value_thous',
                y='rate_ratio',
                ax=ax3,
                size='total_population',
                sizes=(5,3000),
                color=next(palette),
                legend=None,
                alpha=0.5 )
ax3.set_title("West")
ax3.set_xlabel(None)
ax3.set_ylabel(None)
ax3.set_xlim(0,1000)
ax3.set_ylim(-0.1,2.25)

sns.scatterplot(data=south_counties,
                x='med_home_value_thous',
                y='rate_ratio',
                ax=ax4,
                size='total_population',
                sizes=(5,3000),
                color=next(palette),
                legend=None,
                alpha=0.5 )
ax4.set_title("South")
ax4.set_xlabel(None)
ax4.set_ylabel(None)
ax4.set_xlim(0,1000)

fig.set_size_inches(10,7)
fig.tight_layout()
fig.savefig("by_region.png", dpi=300)


