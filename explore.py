import pandas as pd
import matplotlib.pyplot as plt

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
        plt.title("Average Precipitation in mm " + r)
        plt.ylabel("Avg Precipitation (mm)")
        plt.xlabel("Year")
        plt.show()

def price_outliers(df):
    outliers = pd.DataFrame(df.groupby([pd.Grouper(freq='1Y')])['inflated'].mean())
    max_inflated = pd.DataFrame(df.groupby([pd.Grouper(freq='1Y')])['inflated'].max()).rename(columns={'inflated':'max_inflated'})
    min_inflated = pd.DataFrame(df.groupby([pd.Grouper(freq='1Y')])['inflated'].min()).rename(columns={'inflated':'min_inflated'})
    outliers = pd.merge(outliers,max_inflated,left_index=True,right_index=True)
    outliers = pd.merge(outliers,min_inflated,left_index=True,right_index=True)
    return outliers