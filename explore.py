import pandas as pd
import matplotlib.pyplot as plt
import pylab as pl
import seaborn as sns

# produces graphs by region of thousands of 60kg bags of coffee produced each year
def production_graph(df):
    # creates grouper object using data from 1980 onward
    # groups by year
    grouper = df[df.index >= '1980-01-01'].resample('Y')

    # aggregates total quantity sold by year
    quantity = grouper.quantity.sum()
    
    # plots quantity produced by year
    quantity.plot()
    plt.title("Thousands of 60kg Bags Produced in Colombia")
    plt.ylabel("Thousands of 60kg bags")
    plt.xlabel("Year")
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
        df.resample('Y')[column].mean().plot()
        plt.title('Average Daily Precipitation in ' + region)
        plt.ylabel('Avg Daily Precipitation (cm)')
        plt.xlabel('Year')
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
    plt.figure(figsize=(15,12))
    ax.inflated.plot(linewidth=3,color='steelblue')

    plt.hlines(ax['inflated'].mean(),0,4000,color='limegreen',linewidth=3)
    plt.hlines(ax['mean'] + (ax['std'] * 1.5),0,4000,color='firebrick',linewidth=3)
    plt.hlines(ax['mean'] - (ax['std'] * 1.5),0,4000,color='firebrick',linewidth=3)
    plt.hlines(ax['mean'] + (ax['std'] * .5),0,4000,color='b',linewidth=3)
    plt.hlines(ax['mean'] - (ax['std'] * .5),0,4000,color='b',linewidth=3)
    plt.ylabel("Export price (2018 cents)",size=22,weight='bold')
    plt.xlabel("Year",size=22,weight='bold')
    plt.title("Export price of Colombian coffee 1994 to 2018",size=25,weight='bold')
    std_dev_above = "1.5 std_dev above mean"
    std_dev_below = "1.5 std_dev below mean"
    std_dev_below_half = ".5 std_dev below mean"
    std_dev_above_half = ".5 std_dev above mean"

    pl.text(600,278,std_dev_above,size=20)
    pl.text(600,78,std_dev_below,size=20)
    pl.text(600,178,"mean",size=20)
    pl.text(600,144,std_dev_below_half,size=20)
    pl.text(600,212,std_dev_above_half,size=20)
    plt.show()

# graph the top five major spikes impacting price over time
# finish annotating
# Look at five major events over time
def events_over_time(df):   
    plt.figure(figsize=(10,6))
    plt.plot(df.inflated, color='Green')
    date_ = '1975'
    plt.axvline(pd.to_datetime(date_), linewidth=1, color='brown')
    date_ = '1979'
    plt.axvline(pd.to_datetime(date_), linewidth=1, color='brown')
    date_ = '1985'
    plt.axvline(pd.to_datetime(date_), linewidth=1, color='brown')
    date_ = '1992'
    plt.axvline(pd.to_datetime(date_), linewidth=1, color='brown')
    date_ = '2012'
    plt.axvline(pd.to_datetime(date_), linewidth=1, color='brown')
    plt.title('Top Five Fluctations in Coffee Prices')
    plt.xlabel('Year')
    plt.ylabel('Inflated Price')
    plt.show()

# Look at the correlation between average temperature and inflated price
def corr_price_and_temp(df):
    columns = [col for col in df.columns if col.endswith('mean_temp')]
    for column in columns:
        sns.scatterplot(df[column], df.price, color='green')
        plt.title('Price vs Average Temperature')
        plt.ylabel('Price')
        plt.show()

# Look at the distribution of inflated prices
def dist_of_price(df):
    plt.figure(figsize=(10, 6))
    sns.distplot(df.inflated, color='green')
    plt.title('Inflated Price Distribution')
    plt.xlabel('Inflated Price')
    plt.show()

# Look at distribution of inflated price after 1991
def dist_after(df):
    plt.figure(figsize=(10, 6))
    sns.distplot(df.inflated.loc['1991':], color='green')
    plt.title('Inflated Price Distribution from 1992')
    plt.xlabel('Inflated Price')
    plt.show()

# Look at distribution of inflated price before 1991
def dist_before(df):
    plt.figure(figsize=(10, 6))
    sns.distplot(df.inflated.loc[:'1991'], color='green')
    plt.title('Inflated Price Distribution up to 1991')
    plt.xlabel('Inflated Price')
    plt.show()

# Look at which regions have the highest cultivation area
def area_cultivated():
    df3 = pd.read_csv('coffee_data/land_use2018.csv').rename(columns={'Unnamed: 0':'region', '2018*':'area'})
    df3.drop([22], inplace=True)
    df3 = df3.sort_values(by='area', ascending=False)
    df3.reset_index(inplace=True)
    df3.drop(columns=('index'),inplace=True)

    plt.figure(figsize=(14,4))
    sns.barplot(df3.region[:13], df3.area, palette=("BuGn_d"))
    plt.title("Which regions have the highest areas cultivated in 2018?")
    plt.xlabel('Region')
    plt.ylabel('Area Cultivated')
    plt.show()