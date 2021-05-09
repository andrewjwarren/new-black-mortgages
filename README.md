# New Black Mortgages in U.S. Counties
### Where is the Black homeownership gap narrowing in the U.S. ?

## Summary
A large portion of U.S. household net worth comes from homeownership, and Black Americans have the [lowest homeownership rate](https://www.urban.org/urban-wire/closer-look-fifteen-year-drop-black-homeownership) of any racial group, a result of generations of discriminatory wealth-building policy that continued [well into the 20th century](https://www.npr.org/2017/05/03/526655831/a-forgotten-history-of-how-the-u-s-government-segregated-america). Naturally, making homeownership more affordable to Black Americans is a large part of many policy proposals to close the racial wealth gap.

This project uses the rich and publicly available [Home Mortgage Disclosure Act](https://www.consumerfinance.gov/data-research/hmda/) data to analyze where Black homeownership is thriving in the U.S. I have created a series of scripts that can flexibly combine HMDA data with American Community Survey (ACS) data to create a county-level data frame for any combination of states and calendar years available in HMDA. The resulting data frame includes a new measure of Black homeownership trends (the Black Home Purchase Ratio) that can provide researchers and policymakers a useful at-a-glance sense of how equitably distributed new home purchases are for a given county in a given year.

___
## The Black Home Purchase Ratio
The Black Home Purchase Ratio is calculated for every county with more than 1,000 Black residents, for a given year. The numerator is the percentage of new home purchases that went to Black-only mortgage borrowers. The denominator is the share of the county's population that is Black-only (ACS 5 year estimate). A county where 20% of the population is Black and where 20% of home purchases are to Black mortgage applicants would have a ratio of 1.

___
## Repository Contents
The repository contains the following:
  *Three scripts that both download and analyze data. They must be run in order.
  *run_control.csv, a file that the scripts use to loop through specific states and years.
  *Two empty folders, 'raw_hmda_data' and 'output', where the scripts will dump state-year data as they download and process it.

___
## Instructions
1. Edit run_control.csv to where each row is a state-year combination you want to analyze. Do not change the columns. Note: these programs have only been tested with 2019 data and 50 U.S. states plus D.C. Double check results carefully if you decide to run other years.
2. Run 1_data_gathering.py, which downloads a large .csv for every state-year in run_control.csv, pickles the file, and saves it to the raw_hmda_data folder. This may take a while on slow internet connections.
3. Run 2_csv_creation.py, which downloads ACS data for each state-year, merges it with HMDA data, calculates a few variables of interest, and saves each resulting data frame to a .csv file in the output folder.
4. Run 3_visualization.py, which creates a single data frame from all the .csv files created in the previous script. It then produces one example of how this data can be visualized.
