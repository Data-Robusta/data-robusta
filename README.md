### Data Robusta Capstone README

We tried to use coffee production quantities and weather in Colombia to predict its export price.

Stuff and things in the README

### Dependencies and version
- python3 3.7.3
- pandas 2.5.0
- seaborn .9.0
- numpy 1.17.4
- matplotlib 3.1.1
- scikit-learn 0.22.1
- CPI 0.1.16
- FBProphet 0.5
- Pickle 4.0


#### Data Dictionary

#### Tall dataframe

- region: The specific department of Colombia
- name: Name of weather station for that department
- latitude: Latitude of weather station
- longitude: Longitude of weather station
- elevation: Elevation of weather station
- prcp: Average precipitation per day in mm
- tavg: Average temperature
- quantity: thousands of 60kg bags

#### Wide dataframe




#### Data insights

Original dataframe is 708 rows with 42 columns and the month as the index

#### missing data points

- max_temp missing 2421 values
- min_temp missing 484 values
- mean_precip missing 1605 values
- mean_temp missing 225 values


