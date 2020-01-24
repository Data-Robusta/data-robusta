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
- Acquire from included json file (data.json) if it exists.
- If not, scrape a list of the top 100 most-starred GitHub repositories for the following languages: Python, Shell, JavaScript, and PHP.
- Then, use the GitHub API to create a json file that includes each repository's name, raw README contents, and listed language.

**Preparation**
- Perform a basic clean of the README text.
- Create a stemmed version of the cleaned text.
- Create a lemmatized version of the cleaned text.

**Exploration**
- Vizualize distributions within the data

**Modeling**
- Split data
- Create multiple models with training data

## Dictionary

### Uncommon Words and Phrases

- Coffee Arabica: One of the two major coffee varieties, considered sweeter, more flavorful, and more acidic than Robusta. Our project focuses on this type of coffee.
- Coffee Robusta: The other major coffee variety, sought after for its much higher caffeine content and lesser vulnerability to pests and adverse weather conditions.
- Coffee rust: 
- Excelso coffee: 
- Prophet model: 
- ICO: 
- Fedecafé: Common abbreviation for National Federation of Coffee Growers of Colombia (Spanish: Federación Nacional de Cafeteros de Colombia), a non-profit business association that promotes production and exportation of Colombian coffee
- NOAA: National Oceanic and Atmospheric Administration, the source for all of our weather data
- RMSE: Root mean squared error, the average amount our predictions differ from the actual values

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