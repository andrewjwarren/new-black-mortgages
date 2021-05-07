# -*- coding: utf-8 -*-
"""
Created on Wed May  5 13:00:29 2021

@author: andre
"""
# This script downloads loan-level data from the HMDA API for every state-year combination in the run_control file.  

# Before running:
# 1. Ensure run_control.csv has every state-year you want to iterate over (and only those state-years)
# 2. Make yourself a drink and put on a record. EP if you have a fast internet connection and double LP if slow.

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
    # Getting the current state-year's data from the HMDA api.
    # The result a large data frame with an observation for every mortgage application in that state and year.
    
    api = "https://ffiec.cfpb.gov/v2/data-browser-api/view/csv"
    
    payload = {'states':state,
               'years':year}
    
    response = requests.get(api, payload)
    print( 'HMDA URL:', response.url )
    print()
    print( f'{state} {year} HMDA response status:', response.status_code )
    print()
    
    # Selecting only variables of interest from ~100 publicly available variables.
    var_list = ['activity_year','state_code','county_code','loan_purpose','derived_race','action_taken']
    
    string_vars = {'derived_msa-md':str,
                   'state_code':str,
                   'county_code':str,
                   'census_tract':str}
    
    raw_hmda = pd.read_csv(response.url, dtype=string_vars, usecols=var_list)
    
    # Pickling the raw data so you only ever have to run this script once.
    raw_hmda.to_pickle(f'raw_hmda_data/{state}_{year}_raw.pkl')