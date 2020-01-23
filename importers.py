import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler



def compare_brazil():
    co = pd.read_csv("coffee_data/colombia_imports.csv")
    br = pd.read_csv("coffee_data/brazil_imports.csv")
    co.export_val.sum()#$113.427,270,963.50
    br.export_val.sum()#$190,002,767,993.00
    cog = pd.DataFrame(co.groupby(co.year).sum().export_val)#Colombia graph data
    brg = pd.DataFrame(br.groupby(br.year).sum().export_val)#Brazil graph data
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

def compare_import_change():
    df = pd.read_csv("coffee_data/colombia_imports.csv")
    df = df[df["dest"] != "World"]
    df.drop(df[df.dest == "Democratic Republic of Germany"].index, inplace=True)
    df.drop(df[df.dest == "Federal Republic of Germany"].index, inplace=True)
    #Dropped East and West Germany due to consolidation in occurring in country labled "Germany"
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
    df2 = pd.DataFrame(df2.groupby("cat").Y2017.sum().sort_values())
    df =  pd.DataFrame(df.groupby("cat").Y1962.sum().sort_values())
    sns.barplot(df.Y1962, df.index, estimator=np.sum, ci=None,palette=("BuGn_d"))
    plt.title("Top 10 importers of Colombian Coffee 1962")
    plt.xlabel("Millions of USD")
    plt.ylabel("")
    plt.show()
    sns.barplot(df2.Y2017, df2.index, estimator=np.sum, ci=None,palette=("BuGn_d"))
    plt.title("Top 10 importers of Colombian Coffee 1962")
    plt.xlabel("Millions of USD")
    plt.ylabel("")
    plt.show()
def breakdown_other():
    df = pd.read_csv("coffee_data/colombia_imports.csv")
    df = df[df["dest"] != "World"]
    df.drop(df[df.dest == "Democratic Republic of Germany"].index, inplace=True)
    df.drop(df[df.dest == "Federal Republic of Germany"].index, inplace=True)
    #Dropped East and West Germany due to consolidation in occurring in country labled "Germany"
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
    df["cat"] = np.where(~df.dest.isin(top_10_1962),df.dest,np.nan)
    df2["cat"] = np.where(~df2.dest.isin(top_10_2017),df2.dest,np.nan)
    df2.dropna(inplace=True)
    df.dropna(inplace=True)
    df.drop(columns=["dest", "Y2017"], inplace=True)
    df2.drop(columns=["dest", "Y1962"], inplace=True)
    top_10_df = df.Y1962.sort_values()[-10:].index.tolist()
    top_10_df2 = df2.Y2017.sort_values()[-10:].index.tolist()
    df["cat"] = np.where(df.index.isin(top_10_df),df.cat,"Other")
    df2["cat"] = np.where(df2.index.isin(top_10_df2),df2.cat,"Other")
    df2 = pd.DataFrame(df2.groupby("cat").Y2017.sum().sort_values())
    df =  pd.DataFrame(df.groupby("cat").Y1962.sum().sort_values())
    sns.barplot(df.Y1962, df.index, estimator=np.sum, ci=None,palette=("BuGn_d"))
    sns.barplot(df2.Y2017, df2.index, estimator=np.sum, ci=None,palette=("BuGn_d"))



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