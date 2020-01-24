import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

df = pd.read_csv("coffee_data/coffee.csv")
df.drop(columns=["Unnamed: 0", "quantity"], inplace=True)
df.rename(columns={"key_0":"date"}, inplace=True)
df.date = df.date.str[:4]
df = df.groupby("date").mean()
df.index = df.index.astype(int)
cols = df.columns.tolist()
volListE = []
for n in cols:
    volListE.append(df[n].rolling(2).std(ddof=0))
df2 = pd.DataFrame(volListE).T
df76 = df2[df2.index < 1984]
df76 = df76[df76.index > 1970]
price_before76 = df76.price[:5].mean()
price_after76 = df76.price[10:].mean()
price_during76 = df76.price[5:10].mean()
predicted_inter_range = (price_before76+price_after76)/2
p1 = (abs(price_during76 - predicted_inter_range) / predicted_inter_range) * 100.0


df86 = df2[df2.index > 1982]
df86 = df86[df86.index < 1990]
price_before86 = df86.price[:3].mean()
price_after86 = df86.price[5:].mean()
price_during86 = df86.price[3:5].mean()
predicted_inter_range = (price_before86+price_after86)/2
p2 = (abs(price_during86 - predicted_inter_range) / predicted_inter_range) * 100.0

df97 = df2[df2.index > 1994]
df97 = df97[df97.index < 2002]
price_before97 = df97.price[:2].mean()
price_after97 = df97.price[4:].mean()
price_during97 = df97.price[2:4].mean()
predicted_inter_range = (price_before97+price_after97)/2
p3 = (abs(price_during97 - predicted_inter_range) / predicted_inter_range) * 100.0

p1+p2+p3