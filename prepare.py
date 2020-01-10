import pandas as pd
import os
from colombia_weather import get_weather
from colombia_coffee import get_coffee

weather = get_weather()
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

weather.date = pd.to_datetime(weather.date)
weather = weather.set_index('date')

coffee = get_coffee()
coffee = coffee.rename(columns={'key_0': 'date'})
coffee = coffee.set_index('date')