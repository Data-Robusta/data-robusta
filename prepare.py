import pandas as pd
import os
import numpy as np
from cpi import inflate
from colombia_weather import get_weather, weather_stations
from colombia_coffee import get_coffee
from fbprophet.diagnostics import cross_validation, performance_metrics
from fbprophet import Prophet
import datetime as dt

# converts dates from the format 'YYYY-MM-DD' to 'YYYY-MM-01'
def first_of_month(date):
    date = str(date)
    date = date[:-2] + '01'
    return date

# imputes missing weather data based on Prophet models for each region's monthly mean precipitaion, mean temperatures, and minimum temperatures
def impute(data):

    # creates dictionary in which completed series will be stored along with RMSEs for each Prophet model
    info = {}

    # creates index that will be used generally to make sure indices match
    # necessary to ensure every month's index will be listed on the first
    index = pd.date_range('1960-01-01', '2018-12-01', freq='MS')

    # iterates through all regions
    for region in data.region.unique():

        # creates regional subset of dataframe
        regional = data[data.region == region]

        # initializes regional dictionary in which the filled data and RMSEs for each climate metric will be stored
        info[region] = {}

        # iterates through climate metrics
        for col in ['mean_precip', 'mean_temp', 'min_temp']:
            info[region][col] = {}
            df = regional[[col]]

            # sets index to the pre-defined month-start index
            df = df.reindex(index, fill_value = np.nan)
            df = df.reset_index()

            # renames variables to accomodate Prophet model
            df = df.rename(columns={col: 'y', 'index': 'ds'})

            # creates and fits Prophet model
            m = Prophet()
            m.fit(df)

            # creates dataframe in which Prophet-guessed values will be merged with original data
            filled = m.make_future_dataframe(periods=0)

            # cross-validates model and saves the RMSE
            cv = cross_validation(m, horizon='298 days')
            info[region][col]['rmse'] = performance_metrics(cv).rmse.mean()

            # gets all predicted values from Prophet model
            forecast = m.predict(filled)

            # fills in missing values into dataframe then saves them in info dictionary
            df.loc[df['y'].isna(), 'y'] = forecast[df['y'].isna()].yhat
            info[region][col]['data'] = df.y

    # sets index to month-starts
    data = data[['quantity', 'price', 'inflated']].resample('MS').mean()

    # creates new dataframe in which all completed values will be included
    new = pd.DataFrame()

    new['date'] = index

    data = data.reset_index()

    # stores complete data straight from initial dataframe into output dataframe
    new['quantity'] = data['quantity']

    new['price'] = data['price']

    new['inflated'] = data['inflated']

    # fills in the output dataframe with the information from the info dictionary
    for region in info:
        for var in info[region]:
            name = region + '_' + var
            new[name] = info[region][var]['data']

    new = new.set_index('date')

    # saves data to csv
    new.to_csv('prepped.csv')
    return new

# gets full dataframe with coffee and weather data
# fresh should typically not be specified.
# setting fresh to True will get a new dataframe instead of reading from the prior-created csv
# use the fresh flag when changes have been made to the code or data
# data will be stored in data.csv
def get_data(fresh=False):
    # checks if data.csv exists and whether the user has requested a fresh copy
    # reads from csv so long as data.csv exists AND the user didn't request fresh
    if os.path.exists('data.csv') and not fresh:
        df = pd.read_csv('data.csv')

        # changes datetime column into index
        df.date = pd.to_datetime(df.date)
        df = df.set_index('date')

    # fresh copy creation
    else:
        # gets weather data
        weather = get_weather()

        # changes column names to accomodate lazy typing
        weather = weather.rename(columns={
            'DATE': 'date',
            'STATION': 'station_code',
            'NAME': 'station_name',
            'LATITUDE': 'lat',
            'LONGITUDE': 'long',
            'ELEVATION': 'elevation',
            'PRCP': 'precipitation',
            'TAVG': 'avg_temp',
            'TMAX': 'max_temp',
            'TMIN': 'min_temp'
            })

        # remaps station names to names of major coffee-producing regions
        weather['region'] = weather.station_name.map(weather_stations)

        # drops rows which are not from major coffee-producing regions
        weather = weather.dropna(subset=['region'])

        # drops columns of little value
        weather = weather.drop(columns=['station_code', 'station_name', 'lat', 'long'])

        # changes dates to first-of-month format to better match the coffee data
        weather.date = weather.date.apply(first_of_month)
       
        # converts date column to datetime and sets it to the index
        weather.date = pd.to_datetime(weather.date)
        weather = weather.set_index('date')

        # creates grouper object which groups the data by month and region
        grouper = weather.groupby([pd.Grouper(freq='MS'), 'region'])

        # uses named aggregation to find monthly mean precipitation, monthly mean temperature,
        # monthly minimum temperature, and monthly maximum temperature, all separated by region
        weather = grouper.agg(mean_precip=('precipitation', np.mean), mean_temp=('avg_temp', np.mean), min_temp=('min_temp', 'min'), max_temp=('max_temp', 'max'))
        
        # returns region to be a normal column instead of an index. this is to aid the upcoming merge since I don't know how to merge on a multi-index.
        weather = weather.reset_index(level='region')

        # turned out max temp wasn't a very useful column
        weather = weather.drop(columns='max_temp')

        # gets coffee data
        coffee = get_coffee(fresh=True)

        # renames date column
        coffee = coffee.rename(columns={'key_0': 'date'})

        # creates inflated prices in 2018 dollars
        coffee['inflated'] = coffee.apply(lambda x: inflate(x.price, x.date.year), axis=1)

        # sets index to date column
        coffee = coffee.set_index('date')

        # combines the two dataframes, merging on date. performs a left join instead of inner join to include all weather data.
        df = pd.merge(left=weather, right=coffee, how='outer', left_index=True, right_index=True)

        # slices only 1960-2018 because those are the years for which we have price/quantity data
        df = df[:'2018']
        
        # stores dataframe as csv named data.csv
        df.to_csv('data.csv')
    return df

def get_prepped(fresh=False):
    if os.path.exists('prepped.csv') and not fresh:
        df = pd.read_csv('prepped.csv')

        # changes datetime column into index
        df.date = pd.to_datetime(df.date)
        df = df.set_index('date')
    else:
        df = get_data()
        df.loc[df.region.isna(), 'region'] = 'Santander'
        df = impute(df)
    return df

def make_weighted(quantity=False):
    df = get_prepped()
    weights = pd.read_excel('coffee_data/colu_coffee_data.xlsx', sheet_name=7, index_col=1, header=5)
    weights = weights.drop(columns='Unnamed: 0')
    weights = weights.reset_index().rename(columns={'index': 'region'})
    weights = weights.iloc[:23]
    weights = weights[weights['2018*'] > 60]
    weights = weights.set_index('region')
    for col in weights.columns:
        weights = weights.rename(columns={str(col): str(col)[0:4]})
    weights = weights.T
    weights.index = weights.index.astype(str)
    weights.index = pd.to_datetime(weights.index)
    yearly = df.resample('YS').mean()
    yearly = yearly[['quantity', 'inflated', 'Caldas_mean_precip', 'Caldas_mean_temp',
        'Antioquia_mean_precip', 'Antioquia_mean_temp', 'Cauca_mean_precip', 'Cauca_mean_temp',
        'Huila_mean_precip', 'Huila_mean_temp', 'Tolima_mean_precip', 'Tolima_mean_temp']]
    yearly = yearly['1995':]
    weights = weights.reindex(index=yearly.index)
    for col in weights.columns:
        for year in range(1995, 2002):
            weights.loc[str(year), col] = weights.loc['2002', col].values

    for col in weights.drop(columns='TOTAL ').columns:
        yearly[col + '_weight'] = weights[col] / weights['TOTAL ']

    fields = ['_mean_precip', '_mean_temp']
    weighted = pd.DataFrame()

    for field in fields:
        weighted['weighted' + field] = (yearly['Antioquia' + field] * yearly['Antioquia_weight']) \
    + (yearly['Caldas' + field] * yearly['Caldas_weight'])\
    + (yearly['Cauca' + field] * yearly['Cauca_weight'])\
    + (yearly['Huila'  + field] * yearly['Huila_weight'])\
    + (yearly['Tolima' + field] * yearly['Tolima_weight'])
    
    if quantity:
        weighted['quantity'] = df.quantity
        
    weighted['price'] = yearly.inflated
    return weighted

def make_weighted_monthly(quantity=False):
    df = get_prepped()
    weights = pd.read_excel('coffee_data/colu_coffee_data.xlsx', sheet_name=7, index_col=1, header=5)
    weights = weights.drop(columns='Unnamed: 0')
    weights = weights.reset_index().rename(columns={'index': 'region'})
    weights = weights.iloc[:23]
    weights = weights[weights['2018*'] > 60]
    weights = weights.set_index('region')
    for col in weights.columns:
        weights = weights.rename(columns={str(col): str(col)[0:4]})
    weights = weights.T
    weights.index = weights.index.astype(str)
    weights.index = pd.to_datetime(weights.index)
    monthly_index = pd.date_range('1995-01-01', '2018-12-01', freq='MS')
    weights = weights.reindex(monthly_index)
    weights.loc[weights.index < '2002'] = weights['2002-01']
    weights = weights.bfill()
    weights = weights.ffill()
    df = df['1995':]

    for col in weights.drop(columns='TOTAL ').columns:
        df[col + '_weight'] = weights[col] / weights['TOTAL ']
    
    fields = ['_mean_precip', '_mean_temp']
    weighted = pd.DataFrame()
    for field in fields:
        weighted['weighted' + field] = (df['Antioquia' + field] * df['Antioquia_weight']) \
    + (df['Caldas' + field] * df['Caldas_weight'])\
    + (df['Cauca' + field] * df['Cauca_weight'])\
    + (df['Huila'  + field] * df['Huila_weight'])\
    + (df['Tolima' + field] * df['Tolima_weight'])

    if quantity:
        weighted['quantity'] = df.quantity

    weighted['price'] = df.inflated
    return weighted