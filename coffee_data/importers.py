import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
pd.set_option('display.float_format', lambda x: '%.5f' % x)
df = pd.read_csv("coffee_export_by_country.csv")
df = df[df.year > 0]
df["year"] = df.year.astype(int)
df["origin"] = "Colombia"
df["dest"] = df.country
df.drop(columns=["country", "sitc4"], inplace=True)
df.rename(columns={"dest":"destination"}, inplace=True)
df = df[df.destination != "0"]
low = df[df.export_val < np.percentile(df.export_val, 33)]
mid = df[(df.export_val >= np.percentile(df.export_val, 33))&(df.export_val <= np.percentile(df.export_val, 66))]
high = df[df.export_val > np.percentile(df.export_val, 66)]
low.destination.nunique()#133
mid.destination.nunique()#92
high.destination.nunique()#47
year_export= df.groupby(df.year).sum()
sns.lineplot(x=year_export.index, y=year_export.export_val)#explort barplot

sns.lineplot(x=year_export.index, y=year_export.import_val)
plt.show()





#Find out if data corr's with coffee data------------
cf = pd.read_csv("coffee.csv")
cf.drop(columns=["Unnamed: 0"], inplace=True)
cf.rename(columns={"key_0":"date"}, inplace=True)
cf.set_index("date", inplace=True)
cf.quantity = cf.quantity.apply(lambda x: x * 1000 * 60 * 2.204623)
total = []
for row in cf.itertuples():
    total.append((row.price * row.quantity)/100)

sum(total)
year_export.export_val.sum()
#$108,572,065,348.50 - OEC
#$100,531,514,658.75 - Fedcaf
#---------------------------------
# brazil = pd.read_csv("brazil.tsv", sep="\t")
# brazil[brazil.origin == "bra"].to_csv("brazil_imports.csv", index = False)
# brazil[brazil.origin == "col"].to_csv("colombia_imports-s.csv", index = False)

df = pd.read_csv("brazil_imports.csv")
dfc = pd.read_csv("colombia_imports-s.csv")
key = pd.read_csv("country_names.tsv", sep= "\t")
key.drop(columns=["id"], inplace=True)
key.rename(columns={"id_3char":"id"}, inplace=True)
df = df[(df.sitc4 == 712)|(df.sitc4 == 711)]
dfc = dfc[(dfc.sitc4 == 712)|(dfc.sitc4 == 711)]
df = df.merge(key,left_on="dest", right_on="id", how="inner")
dfc = dfc.merge(key,left_on="dest", right_on="id", how="inner")
dfc.drop(columns=["dest", "id", "sitc4"], inplace=True)
dfc.rename(columns={"name":"dest"}, inplace=True)
df.drop(columns=["dest", "id", "sitc4"], inplace=True)
df.rename(columns={"name":"dest"}, inplace=True)
df.origin = ["brazil"]*len(df.origin)
df.fillna(0, inplace=True)
dfc.origin = ["colombia"]*len(dfc.origin)
df.to_csv("brazil_imports.csv", index=False)
dfc.to_csv("colombia_imports.csv", index=False)
#colombia and brazil export calculations------
co = pd.read_csv("colombia_imports.csv")
br = pd.read_csv("brazil_imports.csv")
co.export_val.sum()
br.export_val.sum()
#$113.427,270,963.50
#$190,002,767,993.00
sns.lineplot(y = co.export_val, x = co.year, ci=None)
sns.lineplot(y = br.export_val, x = br.year, ci=None)
