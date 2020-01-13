import pandas as pd
import os
import numpy as np
from cpi import inflate
from colombia_weather import get_weather, weather_stations
from colombia_coffee import get_coffee

# converts dates from the format 'YYYY-MM-DD' to 'YYYY-MM-01'
def first_of_month(date):
    date = str(date)
    date = date[:-2] + '01'
    return date

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
        grouper = weather.groupby([pd.Grouper(freq='BMS'), 'region'])

        # uses named aggregation to find monthly mean precipitation, monthly mean temperature,
        # monthly minimum temperature, and monthly maximum temperature, all separated by region
        weather = grouper.agg(mean_precip=('precipitation', np.mean), mean_temp=('avg_temp', np.mean), min_temp=('min_temp', 'min'), max_temp=('max_temp', 'max'))
        
        # returns region to be a normal column instead of an index. this is to aid the upcoming merge since I don't know how to merge on a multi-index.
        weather = weather.reset_index(level='region')

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

