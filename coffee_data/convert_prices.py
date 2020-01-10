#Convert prices in csv to account for inflation
from datetime import date
import pandas as pd
import cpi
df = pd.read_csv("excelso_prices.csv")


def adjust_for_inflation(df):
    final = []
    for row in df.itertuples():
        year = int(row.date[:4])
        month = int(row.date[5:7])
        price = round(int(row.excelso_price_cents_per_pound))/10
        out = round(cpi.inflate(price, date(year,month,1)))
        final.append(out)
    return final

out = adjust_for_inflation(df)

df["price_adjusted_inflation"] = out
df.to_csv("price_adjusted_inflation.csv", index=False)