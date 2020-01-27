import pandas as pd
import matplotlib.pyplot as plt
import pylab as pl
import seaborn as sns
from scipy import stats
from prepare import get_prepped


# produces graphs by region of thousands of 60kg bags of coffee produced each year
def production_graph(df):
    # creates grouper object using data from 1980 onward
    # groups by year
    grouper = df[df.index >= '1980-01-01'].resample('Y')

    # aggregates total quantity sold by year
    quantity = grouper.quantity.sum()
    
    # plots quantity produced by year
    plt.figure(figsize=(10,6))
    quantity.plot(color='darkgreen', linewidth=2)
    plt.title("Thousands of 60kg Bags Produced in Colombia", size=20)
    plt.ylabel("Thousands of 60kg bags", size=15)
    plt.xlabel("Year", size=15)
    plt.show()

# produces graphs of average precipitation by year and region
def precipitation_by_region(df):
    # gets list of all mean precipitation columns
    columns = [col for col in df.columns if col.endswith('mean_precip')]

    # iterates through all regions creating a line plot of each region's annual mean precipitation
    print('Average Precipitation by Region of Colombia')
    for column in columns:
        word_list = column.split('_')
        region = word_list[0]
        df.resample('Y')[column].mean().plot(color='darkgreen', linewidth=2)
        plt.title('Average Daily Precipitation in ' + region, size=14)
        plt.ylabel('Avg Daily Precipitation (cm)', size=12)
        plt.xlabel('Year', size=12)
        plt.show()

# produces graphs of average temperature by year and region
def avg_temp_by_region(df):
    # gets list of all mean precipitation columns
    columns = [col for col in df.columns if col.endswith('mean_temp')]

    # iterates through all regions creating a line plot of each region's annual mean temperature
    print('Average Temperature by Region of Colombia')
    for column in columns:
        word_list = column.split('_')
        region = word_list[0]
        df.resample('Y')[column].mean().plot(color='darkgreen', linewidth=2)
        plt.title('Average Temperature in ' + region, size=14)
        plt.ylabel('Avg Temperature (cm)', size=12)
        plt.xlabel('Year', size=12)
        plt.show()

# Creates a dataframe containing annual maximum and minimum coffee prices in Colombia
def price_outliers(df):
    outliers = pd.DataFrame(df.groupby([pd.Grouper(freq='1Y')])['inflated'].mean())
    max_inflated = pd.DataFrame(df.groupby([pd.Grouper(freq='1Y')])['inflated'].max()).rename(columns={'inflated':'max_inflated'})
    min_inflated = pd.DataFrame(df.groupby([pd.Grouper(freq='1Y')])['inflated'].min()).rename(columns={'inflated':'min_inflated'})
    outliers = pd.merge(outliers,max_inflated,left_index=True,right_index=True)
    outliers = pd.merge(outliers,min_inflated,left_index=True,right_index=True)
    return outliers

# graph of wholesale Colombian price from 1991 to 2018
def export_price_1991_2018(df):

    ax = df['1991':]
    ax['std'] = ax.inflated.std()
    ax['mean'] = ax.inflated.mean()
    ax['dist_from_mean'] = ax['inflated'] - ax['mean']
    ax = ax[['quantity','inflated','std','mean','dist_from_mean']]

    inflated_mean = ax.inflated.mean()
    plt.figure(figsize=(10,6))
    ax.inflated.plot(linewidth=2,color='darkgreen')

    plt.hlines(ax['inflated'].mean(),0,4000,color='limegreen',linewidth=2)
    plt.hlines(ax['mean'] + (ax['std'] * 1.5),0,4000,color='firebrick',linewidth=2)
    plt.hlines(ax['mean'] - (ax['std'] * 1.5),0,4000,color='firebrick',linewidth=2)
    plt.hlines(ax['mean'] + (ax['std'] * .5),0,4000,color='b',linewidth=2)
    plt.hlines(ax['mean'] - (ax['std'] * .5),0,4000,color='b',linewidth=2)
    plt.ylabel("Export price (2018 cents)",size=15)
    plt.xlabel("Year",size=15)
    plt.title("Export price of Colombian coffee 1994 to 2018",size=20)
    std_dev_above = "1.5 std_dev above mean"
    std_dev_below = "1.5 std_dev below mean"
    std_dev_below_half = ".5 std_dev below mean"
    std_dev_above_half = ".5 std_dev above mean"

    pl.text(600,278,std_dev_above,size=15)
    pl.text(600,78,std_dev_below,size=15)
    pl.text(600,178,"mean",size=15)
    pl.text(600,144,std_dev_below_half,size=15)
    pl.text(600,212,std_dev_above_half,size=15)
    plt.show()

# graph the top five major spikes impacting price over time
# finish annotating
# Look at five major events over time
def events_over_time(df):   
    plt.figure(figsize=(10,6))
    plt.plot(df.inflated, color='darkgreen', linewidth=2)
    date_ = '1975'
    plt.axvline(pd.to_datetime(date_), linewidth=2, color='navy')
    date_ = '1979'
    plt.axvline(pd.to_datetime(date_), linewidth=2, color='navy')
    date_ = '1985'
    plt.axvline(pd.to_datetime(date_), linewidth=2, color='navy')
    date_ = '1992'
    plt.axvline(pd.to_datetime(date_), linewidth=2, color='navy')
    date_ = '2012'
    plt.axvline(pd.to_datetime(date_), linewidth=2, color='navy')
    plt.title('Top Five Fluctations in Coffee Prices', size=20)
    plt.xlabel('Year', size=15)
    plt.ylabel('Inflated Price', size=15)
    plt.show()

# Look at the correlation between average temperature and inflated price
def corr_price_and_temp(df):
    columns = [col for col in df.columns if col.endswith('mean_temp')]
    for col in columns:
        word_list = col.split('_')
        region = word_list[0]
        sns.scatterplot(df[col], df.price, color='darkgreen')
        plt.title('Average Temperature in ' + region, size=14)
        plt.ylabel('Price', size=12)
        plt.xlabel('Temperature (degrees F)', size='12')
        plt.show()

# Look at the correlation between avg precipication and inflated price
def corr_price_and_precip(df):
    columns = [col for col in df.columns if col.endswith('mean_precip')]
    for col in columns:
        word_list = col.split('_')
        region = word_list[0]
        sns.scatterplot(df[col], df.price, color='darkgreen')
        plt.title('Average Precipitation in ' + region, size=14)
        plt.ylabel('Price', size=12)
        plt.xlabel('Precipitation (cm)', size=12)
        plt.show()

# Look at the distribution of inflated prices
def dist_of_price(df):
    plt.figure(figsize=(10, 6))
    sns.distplot(df.inflated, color='darkgreen')
    plt.title('Price Distribution 1960 to 2018',size=20)
    plt.xlabel('Price (in 2018 dollars)', size=15)
    plt.ylabel('Expected Probability', size=15)
    plt.show()

# Look at distribution of inflated price after 1991
def dist_after(df):
    plt.figure(figsize=(10, 6))
    sns.distplot(df.inflated.loc['1992':], color='darkgreen')
    plt.title('Price Distribution 1992 to 2018', size=20)
    plt.xlabel('Price (in 2018 dollars)', size=15)
    plt.ylabel('Expected Probability', size=15)
    plt.show()

# Look at distribution of inflated price before 1991
def dist_before(df):
    plt.figure(figsize=(10, 6))
    sns.distplot(df.inflated.loc[:'1992'], color='darkgreen')
    plt.title('Price Distribution 1960 to 1991', size=20)
    plt.xlabel('Price (in 2018 dollars)', size=15)
    plt.ylabel('Expected Probability', size=15)
    plt.show()

# Look at which regions have the highest cultivation area
def area_cultivated():
    df3 = pd.read_csv('coffee_data/land_use2018.csv').rename(columns={'Unnamed: 0':'region', '2018*':'area'})
    df3 = df3.sort_values(by='area', ascending=False)
    df3.drop([15, 22], inplace=True)
    df3.reset_index(inplace=True)
    df3.drop(columns=('index'),inplace=True)

    plt.figure(figsize=(14,6))
    sns.barplot(df3.region[:13], df3.area, color='darkgreen')
    plt.title("Which regions have the highest areas cultivated in 2018?", size=20)
    plt.xlabel('Region', size=15)
    plt.ylabel('Area Cultivated', size=15)
    plt.show()

# correlation testing between precipitation and price
def corr_temp_price(df):
    columns = [col for col in df.columns if col.endswith('mean_temp')]
    for col in columns:
        x = df[col]
    y = df.inflated
    corr, p = stats.pearsonr(x,y)
    print(f'r = {corr}')
    print(f'p = {p}')

# correlation testing between mean temp and price
def corr_precip_price(df):
    columns = [col for col in df.columns if col.endswith('mean_precip')]
    for col in columns:
        x = df[col]
    y = df.inflated
    r, p = stats.pearsonr(x, y)
    print(f'r = {r}')
    print(f'P = {p}')

# describes how volatility differs in years with disastrous weather events compared to those without
def describe_volatility():
    # acquires inflation-adjusted prices and calculates differences in price from year-to-year
    df = get_prepped()
    df = df[['inflated']]
    df = df.resample('YS').mean()
    df['difference'] = df.inflated - df.inflated.shift(1)
    df['difference'] = df.difference.apply(lambda x: abs(x))
    df['percent_change'] = df.difference / df.inflated

    # creates mask of years in which price was majorly affected by severe weather events
    weather_events = ((df.index >= '1976') & (df.index <= '1978')) | (df.index == '1986') | (df.index == '1987') | (df.index == '1997') | (df.index == '1998')

    # calculates average price in years which were unaffected by disastrous weather
    typical_price = df[~weather_events].inflated.mean()

    # calculates average price in years which were unaffected by disastrous weather
    disaster_price = df[weather_events].inflated.mean()

    
    disaster_volatility = df[weather_events].difference.mean() / disaster_price

    typical_volatility = df[~(weather_events)].difference.mean() / typical_price

    print(f'''In typical years, price changed by an average of {round(typical_volatility * 100, 2)}%. 
In years with disastrous weather events, price changed by an average of {round(disaster_volatility * 100, 2)}%.
This represents a {round((disaster_volatility / typical_volatility * 100), 2)}% increase in year-to-year price volatility.''')

# creates a scatter plot comparing temperature vs price across all regions
def temp_vs_price():
    df = get_prepped()
    df = df['1994':]
    to_plot = [col for col in df.columns if col.endswith('mean_temp')]
    for region in to_plot:
        sns.scatterplot(x=df[region], y=df.inflated, color='darkgreen', alpha=0.5)
    plt.show()

# creates a scatter plot comparing precipitation vs price across all regions
def precip_vs_price():
    df = get_prepped()
    df = df['1994':]
    to_plot = [col for col in df.columns if col.endswith('mean_precip')]
    for region in to_plot:
        sns.scatterplot(x=df[region], y=df.inflated, color='darkgreen', alpha=0.5)
    plt.show()