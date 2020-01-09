import pandas as pd

# Make dataframes of NOAA data CSVs on colombia weather
def get_colombia_weather():
    modern = pd.read_csv('weather_data/colombia.csv')
    old = pd.read_csv('weather_data/colombia_old.csv')
    useless = [col for col in old.columns if col[-10:] == 'ATTRIBUTES']
    old = old.drop(columns=useless)
    colombia = pd.concat([old, modern])
    return colombia

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