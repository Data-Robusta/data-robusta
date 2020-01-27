# What Drives Coffee Prices?

**Goals:** 
- Test if weather in Colombia can predict the export price of Colombian coffee
- Identify key factors in determining Colombian coffee prices

## Table of Contents

- [Dependencies](#dependencies)
- [Organization](#organization)
- [Dictionary](#dictionary)

## Dependencies
- python3 3.7.3
- pandas 2.5.0
- seaborn .9.0
- numpy 1.17.4
- matplotlib 3.1.1
- scikit-learn 0.22.1
- CPI 0.1.16
- FBProphet 0.5
- Pickle 4.0

## Organization

`data_robusta_final.ipynb` pipeline:

**Acquisition**
- Acquire coffee price and production quantity data from Fedecafé Excel spreadsheets. Also creates a column of prices adjusted into 2018 dollars using the Consumer Price Index.
- Acquire Colombia's average temperature, minimum temperature, and average precipitation data by day by weather station from 1960 to 2018. Aggregate these fields into monthly averages in the cases of precipitation and average temperature, and the monthly minimum of the daily minimums. Map weather stations to regions in Colombia. Notably, some of these data were missing.
- Combine these two dataframes into one.

**Preparation**
- Widens the dataframe to have one column for each regional weather metric
- Fills in missing weather data with values predicted by univariate Prophet models
- NEEDS FURTHER EXPLANATION

**Exploration**
- Vizualize distributions and correlations within the data
- Explore price volatility
- See how major weather events affected price
- Research Colombian history
- Look at stockpile reserves over time
- Search for predictive power of Brazilian coffee prices
- Visualize which countries buy most coffee from Colombia

**Modeling**
- NEEDS WORK

## Dictionary

### Uncommon Words and Phrases

- Coffee Arabica: One of the two major coffee varieties, considered sweeter, more flavorful, and more acidic than Robusta. Our project focuses on this type of coffee.
- Coffee Robusta: The other major coffee variety, sought after for its much higher caffeine content and lesser vulnerability to pests and adverse weather conditions.
- Coffee rust: A disease that devastates coffee plants and produces red-yellow spots on the leaves that look like rust.
- Excelso coffee: A size-grading of coffee beans. This is the second largest coffee grading and is most commonly sold.
- Prophet model: A time-series modeling library developed by Facebook used to quickly and accurately predict trends over time
- ICO: International Coffee Organization, a trade bloc that tracks global coffee statistics and encourages development.
- Fedecafé: Common abbreviation for National Federation of Coffee Growers of Colombia (Spanish: Federación Nacional de Cafeteros de Colombia), a non-profit business association that promotes production and exportation of Colombian coffee.
- NOAA: National Oceanic and Atmospheric Administration, the source for all of our weather data.
- RMSE: Root mean squared error, the average amount our predictions differ from the actual values.
- CPI: Consumer Price Index, a measure of the average change over time in the prices paid by U.S. consumers, used to approximate inflation.

### Data Dictionary

#### Weather Data

- region: The specific department of Colombia
- name: Name of weather station for that department
- latitude: Latitude of weather station
- longitude: Longitude of weather station
- elevation: Elevation of weather station
- prcp: Average precipitation per day in mm
- tavg: Average temperature

#### Coffee Data

- price: Export price of Excelso coffee in USD per lb
- inflated: Export price adjusted for inflation into 2018 dollars
- quantity: Thousands of 60kg bags of coffee produced

#### Unified Dataframe

- \[region]_mean_precip: Average monthly precipitation for that region (missing values were backfilled by time-series models on each column)
- \[region]_mean_temp: Average monthy temperature for that region (missing values were backfilled by time-series models on each column)
- \[region]_min_temp: Minimum monthly temperature for that region (missing values were backfilled by time-series models on each column)
- quantity: Thousands of 60kg bags of coffee produced
- price: Export price of Excelso coffee in USD per lb
- inflated: Export price adjusted for inflation into 2018 dollars