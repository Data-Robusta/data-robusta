from scipy.stats import shapiro
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd



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


