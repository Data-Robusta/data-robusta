import pandas as pd
import matplotlib.pyplot as plt
import pylab as pl

#produces graphs by region of thousands of 60kg bags of coffee produced each year
def production_by_region(df):
    #df = df.drop(index = '1971-04-01')
    grouper = df[df.index >= '1980-01-01'].groupby([pd.Grouper(freq='1Y'),'region'])
    region_quantity = grouper.quantity.sum()
    region_quantity = region_quantity.reset_index()
    region_quantity.set_index('date',inplace=True)
     
    print("Top Coffee Producing Regions of Colombia")
    for r in region_quantity.region.unique():
        region_quantity[region_quantity.region == r].quantity.plot()
        plt.title("Thousands of 60kg bags produced by " + r)
        plt.ylabel("Thousands of 60kg bags")
        plt.xlabel("Year")
        plt.show()

#produces graphs of average precipitation by year and region
def precipitation_by_region(df):
    #df = df[df.index != '1971-04-01']
    grouper = df[df.index >= '1980-01-01'].groupby([pd.Grouper(freq='1Y'),'region'])
    region_precip = grouper.mean_precip.sum()
    region_precip = region_precip.reset_index()
    region_precip.set_index('date',inplace=True)

    print("Average precipitation by Region of Colombia")
    for r in region_precip.region.unique():
        region_precip[region_precip.region == r].mean_precip.plot()
        plt.title("Average Precipitation in cm " + r)
        plt.ylabel("Avg Precipitation (cm)")
        plt.xlabel("Year")
        plt.show()

def price_outliers(df):
    outliers = pd.DataFrame(df.groupby([pd.Grouper(freq='1Y')])['inflated'].mean())
    max_inflated = pd.DataFrame(df.groupby([pd.Grouper(freq='1Y')])['inflated'].max()).rename(columns={'inflated':'max_inflated'})
    min_inflated = pd.DataFrame(df.groupby([pd.Grouper(freq='1Y')])['inflated'].min()).rename(columns={'inflated':'min_inflated'})
    outliers = pd.merge(outliers,max_inflated,left_index=True,right_index=True)
    outliers = pd.merge(outliers,min_inflated,left_index=True,right_index=True)
    return outliers

# graph of wholesale Colombian price 1991 to 2018
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
def events_over_time(df):   
    plt.figure(figsize=(12,6))
    plt.plot(df.inflated)
    date_ = '1975'
    plt.axvline(pd.to_datetime(date_), linewidth=1, color='red')
    datetime = '1979'
    plt.axvline(pd.to_datetime(datetime), linewidth=1, color='red')
    date = '1985'
    plt.axvline(pd.to_datetime(date), linewidth=1, color='red')
    dateevent = '1992'
    plt.axvline(pd.to_datetime(dateevent), linewidth=1, color='red')
    datet = '2014'
    plt.axvline(pd.to_datetime(datet), linewidth=1, color='red')
    plt.title('Top five major events that affected inflation')
    plt.xlabel('Year')
    plt.ylabel('Inflation Price')
    plt.show()