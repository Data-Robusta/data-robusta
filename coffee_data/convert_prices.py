#Convert prices in csv to account for inflation
from datetime import date
import pandas as pd
import cpi
df = pd.read_csv("excelso_prices.csv")


def adjust_for_inflation(df):
    adj = []
    rounded_non_adj = []
    for row in df.itertuples():
        year = int(row.date[:4])
        month = int(row.date[5:7])
        price = round(int(row.excelso_price_cents_per_pound),2)
        out = round(cpi.inflate(price, date(year,month,1)))
        adj.append(out)
        rounded_non_adj.append(price)
    return adj, rounded_non_adj

adj,non_adj = adjust_for_inflation(df)

df["price_adjusted_inflation"] = adj
df["excelso_price_cents_per_pound"] = non_adj 
dffinal.rename(columns={"month/year":"date"},inplace=True)
merge=pd.merge(dffinal,df, how='inner')
merge.to_csv("coffee.csv")
