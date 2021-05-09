# Results

___
As is, the scripts in this repository produce only one descriptive result, a bubble plot of counties organized by census region, with median home value on the x-axis and the Black Mortgage Ratio on the y-axis. This is merely an example of one of the ways this data can be explored.

![alt text](https://github.com/andrewjwarren/new-black-mortgages/blob/main/by_region.png)

More substantively, the scripts produce a county-level data frame that has lots of flexibility. Any other U.S. county-level data set with any variables of interest can easily be merged onto this data frame using FIPS county codes. Future researchers could use these scripts to explore other geographical patterns or to model the marginal effect of policy interventions on the Black Mortgage Ratio or logged increase/decrease in number of new mortgages to Black residents. This process can also be easily modified to produce longitudinal data by county as well, simply by including multiple years for a given state in the run_control.csv file. This will substantially increase the download time needed in the first script, but opens up interesting possibilities for fixed effects models and difference-in-differences research designs.
