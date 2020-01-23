import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
pd.set_option("display.float_format", lambda x: "%.5f" % x)


#Find out if data corr"s with coffee data------------
# cf = pd.read_csv("coffee_data/coffee.csv")
# cf.drop(columns=["Unnamed: 0"], inplace=True)
# cf.rename(columns={"key_0":"date"}, inplace=True)
# cf.set_index("date", inplace=True)
# cf.quantity = cf.quantity.apply(lambda x: x * 1000 * 60 * 2.204623)
# total = []
# for row in cf.itertuples():
#     total.append((row.price * row.quantity)/100)

# sum(total)
#$113.427,270,963.50 - OEC
#$100,531,514,658.75 - Fedcaf
#---------------------------------
# brazil = pd.read_csv("brazil.tsv", sep="\t")
# brazil[brazil.origin == "bra"].to_csv("brazil_imports.csv", index = False)
# brazil[brazil.origin == "col"].to_csv("colombia_imports-s.csv", index = False)

# df = pd.read_csv("coffee_data/brazil_imports.csv")
# dfc = pd.read_csv("coffee_data/colombia_imports.csv")
# key = pd.read_csv("coffee_data/country_names.tsv", sep= "\t")
# key.drop(columns=["id"], inplace=True)
# key.rename(columns={"id_3char":"id"}, inplace=True)
# df = df[(df.sitc4 == 712)|(df.sitc4 == 711)]
# dfc = dfc[(dfc.sitc4 == 712)|(dfc.sitc4 == 711)]
# df = df.merge(key,left_on="dest", right_on="id", how="inner")
# dfc = dfc.merge(key,left_on="dest", right_on="id", how="inner")
# dfc.drop(columns=["dest", "id", "sitc4"], inplace=True)
# dfc.rename(columns={"name":"dest"}, inplace=True)
# df.drop(columns=["dest", "id", "sitc4"], inplace=True)
# df.rename(columns={"name":"dest"}, inplace=True)
# df.origin = ["brazil"]*len(df.origin)
# df.fillna(0, inplace=True)
# dfc.origin = ["colombia"]*len(dfc.origin)
# df.to_csv("coffee_data/brazil_imports.csv", index=False)
# dfc.to_csv("coffee_data/colombia_imports.csv", index=False)
#colombia and brazil export calculations------
def compare_brazil():
    co = pd.read_csv("coffee_data/colombia_imports.csv")
    br = pd.read_csv("coffee_data/brazil_imports.csv")
    co.export_val.sum()#$113.427,270,963.50
    br.export_val.sum()#$190,002,767,993.00
    cog = pd.DataFrame(co.groupby(co.year).sum().export_val)#Colombia graph data
    brg = pd.DataFrame(br.groupby(br.year).sum().export_val)#Brazil graph data
    # gdf = cog.merge(brg, how="inner", on=brg.index)#graph data frame
    # gdf.rename(columns={"key_0":"year", "export_val_x":"export_val_co", "export_val_y":"export_val_br"}, inplace=True)
    # plt.plot( "year", "export_val_co",data=gdf, linewidth=2)
    # plt.plot( "year", "export_val_br", data=gdf, linewidth=2)
    # plt.legend()
    #------------------------------------------------------------------
    #Scaling and further graphing-----------------
    import datetime as dt
    scaler = MinMaxScaler()
    scog = cog.copy()#Creating copy for scaling
    sbrg = brg.copy()#Creating copy for scaling
    scog["export_val"] = scaler.fit_transform(np.array(scog.export_val).reshape(-1,1))
    sbrg["export_val"] = scaler.fit_transform(np.array(sbrg.export_val).reshape(-1,1))
    sgdf = scog.merge(sbrg, how="inner", on=sbrg.index)#graph data frame
    sgdf.rename(columns={"key_0":"year", "export_val_x":"Colombian_exports_scaled", "export_val_y":"Brazilian_exports_scaled"}, inplace=True)
    plt.plot( "year", "Colombian_exports_scaled",data=sgdf, linewidth=2)
    plt.plot( "year", "Brazilian_exports_scaled", data=sgdf, linewidth=2)
    plt.legend()#Outputs are proportionally higher with colombia between 1970 and 2003/5
    #Shifting Brazilian data will not be useful in predicting Colombian coffee prices/outputs
#------------------------------------------------------------------
#Introducing price data--------------------
# cf = pd.read_csv("coffee_data/coffee.csv")#load coffee data
# cf.drop(columns=["Unnamed: 0"], inplace=True)
# cf.rename(columns={"key_0":"year"}, inplace=True)
# cf.year = pd.to_datetime(cf.year)
# cf.set_index("year",inplace=True)
# cf = cf.resample("Y").agg({"price": "median", "quantity": "sum"})
# cf.index = cf.index.to_series().apply(lambda x: dt.datetime.strftime(x, "%Y")).tolist()
# cf.index.name = "year"
# cf = cf[2:-1]
# gdf = gdf.merge(cf, how="inner", on=cf.index)# Standard graphing
# total = []
# for row in gdf.itertuples():
#     total.append(row.price*((row.quantity*1000*60)*2.204623)/100)
# gdf["totals"]= total
# gdf.drop(columns=["key_0"], inplace=True)
# plt.plot("year","export_val_co",data=gdf, linewidth=2)#cash value of quantity 
# plt.plot("year","totals",data=gdf, linewidth=2)#cash value of quantity 

# plt.plot("year","export_val_br", data=gdf, linewidth=2)#cash value of quantity 

# #plt.plot("year","quantity", data=gdf, linewidth=2)#quantity

# #plt.plot("year","price", data=gdf, linewidth=2)#price per thousand 60 kg bags
# plt.legend()

# #Visualize Coffee imports by country------------------------
def compare_import_change():
    df = pd.read_csv("coffee_data/colombia_imports.csv")
    df = df[df["dest"] != "World"]
    df.drop(df[df.dest == "Democratic Republic of Germany"].index, inplace=True)
    df.drop(df[df.dest == "Federal Republic of Germany"].index, inplace=True)
    #Dropped East and West Germany due to consolidation in occurring in country labled "Germany"
    df.groupby(["year","dest"]).agg({"export_val":"sum"}).reset_index(inplace=True)
    df = df.pivot_table("export_val", "dest", "year")
    df.fillna(0, inplace=True)
    df = df.T
    df = pd.concat([df[:1],df[-1:]])
    df = df.T
    df.columns=["Y1962", "Y2017"]
    df2 = df.copy()
    top_10_1962 = df.Y1962.sort_values()[-10:].index.tolist()
    top_10_2017 = df.Y2017.sort_values()[-10:].index.tolist()
    df.reset_index(inplace=True)
    df2.reset_index(inplace=True)
    df["cat"] = np.where(df.dest.isin(top_10_1962),df.dest,"Other")
    df2["cat"] = np.where(df2.dest.isin(top_10_2017),df2.dest,"Other")
    df.drop(columns=["dest", "Y2017"], inplace=True)
    df2.drop(columns=["dest", "Y1962"], inplace=True)
    df["origin"] = "Colombia"
    df2["origin"] = "Colombia"
    df2 = pd.DataFrame(df2.groupby("cat").Y2017.sum().sort_values())
    df =  pd.DataFrame(df.groupby("cat").Y1962.sum().sort_values())
    sns.barplot(df.Y1962, df.index, estimator=np.sum, ci=None,palette=("BuGn_d"))
    sns.barplot(df2.Y2017, df2.index, estimator=np.sum, ci=None,palette=("BuGn_d"))

#NOTES
#Break down the Other category and what the make up is


# #Get precent make up of all sales by year per country. 
# dfs = df.groupby(["year", "dest"]).agg({"export_val": "sum"})
# df_pcts = dfs.groupby(level=0).apply(lambda x:100 * x / float(x.sum()))
# df_pcts.reset_index(inplace=True)
# df_pcts.to_csv("import_percentage2017.csv", index=False)
# #----------------------------------------------------------------





# #Top movers - determed by largest growth year over year.
def compare_volatility():
    df = pd.read_csv("coffee_data/colombia_imports.csv")
    df = df[df["dest"] != "World"]
    df.drop(df[df.dest == "Democratic Republic of Germany"].index, inplace=True)
    df.drop(df[df.dest == "Federal Republic of Germany"].index, inplace=True)
    #Dropped East and West Germany due to consolidation in occurring in country labled "Germany"
    df.groupby(["year","dest"]).agg({"export_val":"sum"}).reset_index(inplace=True)
    df = df.pivot_table("export_val", "dest", "year")
    df.fillna(0, inplace=True)
    df = df.T
    # df = df.pct_change(periods=4)
    # df = df.replace([np.inf, -np.inf], np.nan)
    # df.fillna(0, inplace=True)
    # df["totals"] = df.sum(axis=1)
    df.index = df.index.astype(int)
    cols = df.columns.tolist()
    volListE = []
    for n in cols:
        volListE.append(df[n].rolling(2).std(ddof=0))
    df = pd.DataFrame(volListE)
    df = df.T
    df.fillna(0, inplace=True)
    # Creating Dataframe for getting percentage makeup of market
    df2 = pd.read_csv("coffee_data/colombia_imports.csv")
    df2 = df2[df2["dest"] != "World"]
    df2.drop(df2[df2.dest == "Democratic Republic of Germany"].index, inplace=True)
    df2.drop(df2[df2.dest == "Federal Republic of Germany"].index, inplace=True)
    #Dropped East and West Germany due to consolidation in occurring in country labled "Germany"
    df2.groupby(["year","dest"]).agg({"export_val":"sum"}).reset_index(inplace=True)
    df2 = df2.pivot_table("export_val", "dest", "year")
    df2.fillna(0, inplace=True)
    df2 = df2.T
    # Combine dataframes so as to scale the data by percent makeup
    df_comb = pd.DataFrame(df.values*df2.values, columns=df.columns, index=df.index)
    df_comb["totals"] = df_comb.sum(axis=1)
    vollist_imports = df_comb.totals
    #Get Coffee Data
    cf = pd.read_csv("coffee_data/coffee.csv")
    cf.drop(columns=["Unnamed: 0"], inplace=True)
    cf.rename(columns={"key_0":"date"}, inplace=True)
    cf.set_index("date", inplace=True)
    cf.index = pd.to_datetime(cf.index)
    cf = cf.resample("Y").mean()
    cf.index = cf.index.astype(str).str[:4].astype(int)
    cf.drop(columns=["quantity"], inplace=True)
    cf.drop(cf[cf.index > 2017].index, inplace=True)
    vollist_price = cf.price.rolling(2).std(ddof=0)
    #vollist_price[4:].hist() #Data is skewed to the left
    #vollist_imports[:-1][1:].hist() #Data is skewed to the left
    return vollist_price[4:],vollist_imports[:-1][1:], vollist_imports[:-1][1:].corr(vollist_price[4:], method="spearman")


def get_volatility_graph():
    vollist_price,vollist_imports,z = compare_volatility()
    scaler = MinMaxScaler()
    df = pd.concat([vollist_price,vollist_imports], axis=1, ignore_index=True)
    df[1] = df[1].shift()
    df = df[1:]
    df.columns=["price_vol", "imports_vol"]
    index = df.index
    df = pd.DataFrame(scaler.fit_transform(df))
    df.index = index
    plt.scatter(df.index,df[0], label="Price Volatility")
    plt.scatter(df.index,df[1], label="Imports Volatility")
    plt.title("Volatility in Colombian Markets")
    plt.xlabel("Year")
    plt.ylabel("Scaled Volatility Level")
    plt.legend()
    plt.show()