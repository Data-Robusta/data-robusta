from scipy.stats import shapiro
from prepare import make_weighted, make_weighted_monthly, get_weights, get_prepped
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np



df = pd.read_csv("data.csv")
df.drop(columns=["region", "quantity"], inplace=True)
df.date = pd.to_datetime(df.date)
df.set_index(df.date, inplace=True)
df = df.resample("Y").mean()
df.dropna(inplace=True)
df.index = df.index.astype(str).str[:4]
df["date"] = df.index.astype(int)


sns.regplot("date","mean_temp", data = df, ci=False, color="darkgreen", robust=True)
plt.title("Average Temperature in Colombia")
plt.xlabel("Date")
plt.ylabel("Temperature in Fahrenheit ")
plt.show()

sns.regplot("date", "inflated", data=df, ci=False, color="darkgreen", robust=True)
plt.title("Price of Colombain Coffe per Pound in USD")
plt.xlabel("Date")
plt.ylabel("Price in Cents")
plt.show()

df2 = pd.read_csv("coffee_data/ico_data_pandas/stockpile.csv")
df2[df2.country_name == "Colombia"]
df2.dropna(inplace=True)
df2.year = df2.year.str[:4]
df2.drop(columns=["country_name", "coffee_type", "production_month"], inplace=True)
df2.year = pd.to_datetime(df2.year)
df2.set_index(df2.year, inplace=True)
df2 = df2.resample("Y").sum()
df2["date"] = df2.index.astype(str).str[:4].astype(int)
sns.lmplot("date", "beginning_stockpile",data = df2)
plt.title("Stockpiles of Coffee Colombia")
plt.xlabel("Date")
plt.ylabel("Stockpile")
plt.show()

sns.regplot("")

sns.scatterplot(y = "mean_precip", x = "inflated", data=df)
sns.scatterplot(y = "mean_temp", x = "inflated", data=df)

dft = get_prepped()

sns.lineplot("date", "inflated", data = df)
df.inflated.hist()
dft

dist_check_post_1994 = pd.DataFrame(dft[dft.index > "01-01-1994"].inflated)

dist_check_pre_1994 = pd.DataFrame(dft[dft.index < "01-01-1994"].inflated)

def check_normal_dist(df):
    if len(df) >= 5000:
        raise ValueError("Shaprio-Wilks test should be used on data less than 5000 values")
    df = df.loc[:, df.dtypes != "category"]
    cols = df.columns.tolist()
    n = 0
    for col in cols:
        stat, p = shapiro(df[col])
        print(p)
        if p > 0.05:
            n += 1
            print(f"Not normally distributed: {col}")
    print(f"finished {n} variables are not normally distributed")

check_normal_dist(dist_check_pre_1994)#Normally Dist. 
check_normal_dist(dist_check_post_1994)#Normally Dist.


df = make_weighted()
df = make_weighted_monthly()
df = get_weights()

df = df[((df.index > '1995-11-01') & (df.index < '1997-02-01'))\
     | ((df.index > '1998-05-01') & (df.index < '2000-09-01')) |\
          ((df.index > '2005-01-01') & (df.index < '2009-06-01'))\
               | (df.index > '2012-05-01')]

df.weighted_mean_temp = df.weighted_mean_temp.astype("float64")
df.weighted_mean_precip = df.weighted_mean_precip.astype("float64")
df.weighted_mean_temp.corr(df.price)
df.weighted_mean_precip.corr(df.price)
df.index = df.index.astype(str).str[:4]
df.index = df.index.astype(int)
df["date"] = df.index

sns.regplot(y = "weighted_mean_temp", x = "date", data=df)
sns.regplot(y = "price", x = "date", data=df, robust=True)
sns.regplot(y = "price", x = "weighted_mean_temp", data=df)
sns.scatterplot(y = "price", x = "weighted_mean_temp", data=df)

df.weighted_mean_temp.corr(df.price)




# GET PERCENT WEIGHTS AND READABLE TEMPREATURE
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

df["totals"] = df.Antioquia_weight + df.Caldas_weight + df.Cauca_weight + df.Huila_weight + df.Tolima_weight

top_5 = ["Antioquia_weight", "Caldas_weight", "Cauca_weight", "Huila_weight", "Tolima_weight"]
for n in top_5:
    df[f'{n}_pct'] =  df[f"{n}"]/ df.totals

top_5_states = "Antioquia", "Caldas", "Cauca", "Huila", "Tolima"
keep_list = ["price", "quantity","inflated"]
for x in top_5_states:
    for n in df.columns:
        if n.startswith(x) == True:
            keep_list.append(n)

df = df[keep_list]

df.drop(columns=["Antioquia_weight", "Caldas_weight", "Cauca_weight", "Huila_weight", "Tolima_weight"], inplace=True)

#Calculate mean temps with each state contributing its portion to the mean
mean = pd.DataFrame()

mean_temp_states = []

for state in top_5_states:
    mean_temp_states.append(state + "_mean_temp")

for idx, row in df.iterrows():
    mean_list = []
    for state in mean_temp_states:
       print(row.loc['Antioquia_mean_temp'])

df.describe()