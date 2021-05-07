# -*- coding: utf-8 -*-
"""
Created on Sun Apr 25 09:32:50 2021

@author: andre
"""
# This script creates a .csv file from each HMDA state-year pickle created in the previous script, combined with census data.

import pandas as pd
import requests

run_control = pd.read_csv("run_control.csv", dtype=str)

# Everything beyond this point is contained in the following for loop.
# ----------------------------------------------------------------------------

# Iterating over each state-year in the run_control.csv
for index, row in run_control.iterrows():
    
    state = row['po_code']
    fips = row['fips']
    year = row['year']

    
    # %%
    # Getting the current state-year's county-level census data to merge onto HMDA data.
    # We need population estimates by race.
    # Variable reference guide here: https://api.census.gov/data/2019/acs/acs5/variables.html
    
    api = f'https://api.census.gov/data/{year}/acs/acs5'
    
    var_list = ["B02001_001E","B02001_002E","B02001_003E","B02001_003M","B25077_001E","B25088_002E","B19113_001E","B19113B_001E","B25024_001E","B25024_002E","B25024_003E"]
    var_string = ["NAME", "B02001_003MA"] + var_list
    var_string = ",".join(var_string)
    for_clause = "county:*"
    in_clause = f"state:{fips}"
    key_value = '17c11300e57ce642d92dbd98da7a2cc71ee482c0'
    
    payload = {'get':var_string,
               'for':for_clause,
               'in':in_clause,
               'key':key_value }
    
    response = requests.get(api, payload)
    
    print( 'Census URL:', response.url )
    print()
    print( f'{state} Census response status:', response.status_code )
    print()
    
    rowlist = response.json()
    colnames = rowlist[0]
    datarows = rowlist[1:]
    county_demos = pd.DataFrame(data=datarows,columns=colnames)
    county_demos['county_code'] = county_demos['state'] + county_demos['county']
    county_demos.drop(['state','county'],axis='columns',inplace=True)
    county_demos.set_index('county_code',inplace=True)
    for var in var_list:
        county_demos = county_demos.astype({var:'int64'})
    
    # %%
    # Wrangling raw HMDA data into by-county format for analysis.
    # -------------------------------------------------------------------------
    raw_hmda = pd.read_pickle(f'raw_hmda_data/{state}_{year}_raw.pkl')
    
    # Filtering to only successful home purchase applications.
    is_purchase = raw_hmda['loan_purpose'] == 1 
    is_successful = raw_hmda['action_taken'] == 1
    successful_home_purchase = is_purchase & is_successful
    purchases = raw_hmda[successful_home_purchase]
    
    # Creating race dummies, and asserting that they are mutually exclusive (each row sums to 1)
    race_dummies = pd.get_dummies(purchases['derived_race'])
    race_dummies['sum'] = race_dummies.sum(axis='columns')
    assert (race_dummies['sum'].sum(axis='rows')) == len(purchases)
    race_dummies.drop('sum',axis='columns',inplace=True)
    
    # Merging race dummies back onto data frame.
    with_dummies = purchases.merge(race_dummies,
                                      left_index=True,
                                      right_index=True,
                                      validate='1:1')
                                     
    # Grouping data by county
    by_county = with_dummies.groupby('county_code')
    
    # Creating a total home purchase applications by county variable. Activity year is arbitrarily chosen as a variable with no missing values. There's a year for each purchase.
    county_counts = by_county.count()
    total_purchases = county_counts['activity_year']
    total_purchases = total_purchases.rename('total_purchases')
    
    # Creating data frame of race by county
    race_counts = by_county[race_dummies.columns.to_list()].sum()
    
    # Merging everything together for our county-level dataframe.
    county_level = pd.concat([total_purchases,race_counts],axis='columns')
    
    
    # %%
    # Merging HMDA data with census data on county code
    # -----------------------------------------------------------------------------
    
    # Using inner join to drop any extra counties in the HMDA data that do not belong according to the census.
    merged = county_level.merge(county_demos,
                                left_index=True,
                                right_index=True,
                                how='inner',
                                validate='1:1')
    
    # Calculating portion of each county's new mortgages that are from Black applicants.
    merged['purchases_w_race'] = merged['total_purchases'] - merged['Race Not Available'] 
    merged['pct_black_purchases'] =  merged['Black or African American'] / merged['purchases_w_race']
    
    # Portion of each county that is Black
    merged['pct_black_pop'] = merged['B02001_003E'] / merged['B02001_001E']
    
    # Percentage point difference between the two.
    merged['rate_disparity'] = merged['pct_black_purchases'] - merged['pct_black_pop']
    
    # Ratio of the two rates, our outcome of interest.
    merged['rate_ratio'] = merged['pct_black_purchases'] / merged['pct_black_pop']
    
    # Portion of homes in county that are single-unit
    merged['pct_single_unit'] = (merged["B25024_002E"] + merged["B25024_003E"]) / merged["B25024_001E"]
    
    
    # %%
    # Dropping counties where the MOE for the Black pop. crosses 1,000. Assuming that we can't draw meaningful 
    # inferences about homeownership rate disparities for these counties.
    
    black_pop_high = ( merged['B02001_003E'] - merged['B02001_003M'] ) > 1000
    
    # There should be no margin of error flag if the estimate is sound. Unlikely to be a problem for any county level population estimate but including just in case.
    no_moe_flag = merged['B02001_003MA'].isnull()
    
    good_black_pop_est = black_pop_high & no_moe_flag
    
    final = merged[good_black_pop_est]
    
    print(len(merged)-len(final), "of", len(merged), f"counties were dropped from {state} because Black populations were too small in {year}.")
    print()
    
    # Renaming a couple of ACS variables to make them more intuitive for the csv file.
    final = final.rename({'Black or African American':'black_purchases',
                          'B02001_003E':'black_population',
                          'B02001_001E':'total_population',
                          'B19113_001E':'med_hh_income',
                          'B19113B_001E':'med_black_hh_income',
                          'B25088_002E':'med_monthly_costs_w_mortgage',
                          'B25077_001E':'med_home_value'},
                           axis='columns')
    
    # Limiting to just the variables we want for countrywide analysis.
    final = final[['NAME','total_purchases','black_purchases','pct_black_purchases',
                   'total_population','black_population','pct_black_pop','rate_disparity',
                   'rate_ratio','pct_single_unit','med_hh_income','med_black_hh_income',
                   'med_monthly_costs_w_mortgage','med_home_value']]
    
    final.to_csv(f"output/{state}{year}.csv")






