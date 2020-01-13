import pandas as pd
import os

# Make dataframes of NOAA data CSVs on monthly colombia weather, has some strange inaccuracies due to the monthly collation
def get_colombia_weather_monthly():
    modern = pd.read_csv('weather_data/new_monthly_weather_colombia.csv')
    old = pd.read_csv('weather_data/colombia_old.csv')
    useless = [col for col in old.columns if col[-10:] == 'ATTRIBUTES']
    old = old.drop(columns=useless)
    colombia = pd.concat([old, modern])
    return colombia

# Make dataframes of NOAA data CSVs on daily colombia weather
def get_weather(fresh=False):
    if os.path.exists('weather_data/weather.csv') and not fresh:
        df = pd.read_csv('weather_data/weather.csv', index_col=0)
    else:
        modern = pd.read_csv('weather_data/new_daily_weather_colombia.csv')
        old = pd.read_csv('weather_data/old_daily_weather_colombia.csv')
        df = pd.concat([old, modern])
        df.to_csv('weather_data/weather.csv')
    return df

# Explanation of each column in the data
data_dict = {
    'CDSD': 'Cooling Degree Seasons to Date',
    'EMNT': 'Extreme Minimum Temperature for the Period',
    'HDSD': 'Heating Degree Seasons to Date',
    'TAVG': 'Average Temperature',
    'TMIN': 'Minimum Temperature',
    'TMAX': 'Maximum Temperature',
    'CLDD': 'Cooling Degree Days',
    'DP01': 'Number of days with greater than or equal to 0.1 inch of precipitation',
    'DP10': 'Number of days with greater than or equal to 1.0 inch of precipitation',
    'DT00': 'Number days with minimum temperature less than or equal to 0.0 F',
    'DT32': 'Number days with minimum temperature less than or equal to 32.0 F',
    'DX32': 'Number days with maximum temperature < 32 F.',
    'DX70': 'Number days with maximum temperature > 70 F (21.1C)',
    'DX90': 'Number days with maximum temperature > 90 F (32.2C)',
    'HTDD': 'Heating degree days',
    'EMXP': 'Extreme maximum precipitation for the period.',
    'PRCP': 'Precipitation'
}

# Natural language name of each weather station
stations = {
    'COM00080036': 'Alfonso Lopez Pumarejo',
    'COM00080398': 'Alfredo Vasquez Cobo',
    'COM00080035': 'Almirante Padilla',
    'COM00080084': 'Antonio Rodan Betancourt',
    'COM00080315': 'Benito Salas',
    'CO000080222': 'Bogota Eldorado',
    'CO000080259': 'Cali Alfonso Bonill',
    'COM00080097': 'Camilo Daza',
    'COM00080144': 'El Carano',
    'COM00080211': 'El Eden',
    'COM00080002': 'El Embrujo',
    'COM00080028': 'Ernesto Cortissoz',
    'COM00080112': 'Jose Maria Cordova',
    'CO000080241': 'Las Gaviotas',
    'COM00080063': 'Los Garzones',
    'COM00080210': 'Matecana',
    'COM00080110': 'Olaya Herrera',
    'COM00080094': 'Palonegro',
    'CO000080342': 'Pasto Antonio Narin',
    'COM00080214': 'Perales',
    'VE000005484': 'Puerto Carreno',
    'COM00080022': 'Rafael Nunez',
    'CO000080001': 'San Andres Isla S',
    'COM00080370': 'San Luis',
    'VE000009418': 'Santa Rosa Amanadona',
    'COM00080099': 'Santiago Perez',
    'COM00080009': 'Simon Bolivar',
    'COM00080234': 'Vanguardia',
    'COM00080091': 'Yariguies'
}

weather_stations = {
    'ANTONIO ROLDAN BETANCOURT, CO': 'Antioquia',
    'JOSE MARIA CORDOVA, CO': 'Caldas',
    'EL CARANO, CO': 'Cauca',
    'ALFONSO LOPEZ PUMAREJO, CO': 'Cesar',
    'BOGOTA ELDORADO, CO': 'Cundinamarca',
    'BENITO SALAS, CO': 'Huila',
    'SIMON BOLIVAR, CO': 'Magdalena',
    'PASTO ANTONIO NARIN, CO': 'Narino',
    'EL EDEN, CO': 'Quindio',
    'MATECANA, CO': 'Risaralda',
    'PALONEGRO, CO': 'Santander',
    'PERALES, CO': 'Tolima',
    'CALI ALFONSO BONILL, CO': 'Valle'
}