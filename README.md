# What Drives Coffee Prices?

**Goals:** 
- Test if coffee production quantities and weather in Colombia can predict its export price.
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

**Evaluation**
- Analyize evaluation metrics with test data

## Dictionary

### Uncommon Words and Phrases

- Coffee Arabica: 
- Coffee Robusta:
- Coffee rust:
- Excelso coffee: 

### Data Dictionary

#### Weather Data

- region: The specific department of Colombia
- name: Name of weather station for that department
- latitude: Latitude of weather station
- longitude: Longitude of weather station
- elevation: Elevation of weather station
- prcp: Average precipitation per day in mm
- tavg: Average temperature
- quantity: thousands of 60kg bags

#### Coffee Data

- price: Export price of Excelso coffee in USD per lb
- inflated: Export price adjusted for inflation into 2018 dollars
- quantity: Thousands of 60kg bags of coffee produced

#### Unified Dataframe

- \[region] 