import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
pd.set_option('display.float_format', lambda x: '%.5f' % x)


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
#$113.427,270,963.50 - OEC
#$100,531,514,658.75 - Fedcaf
#---------------------------------
# brazil = pd.read_csv("brazil.tsv", sep="\t")
# brazil[brazil.origin == "bra"].to_csv("brazil_imports.csv", index = False)
# brazil[brazil.origin == "col"].to_csv("colombia_imports-s.csv", index = False)

df = pd.read_csv("brazil_imports.csv")
dfc = pd.read_csv("colombia_imports.csv")
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
co.export_val.sum()#$113.427,270,963.50
br.export_val.sum()#$190,002,767,993.00
cog = pd.DataFrame(co.groupby(co.year).sum().export_val)#Colombia graph data
brg = pd.DataFrame(br.groupby(br.year).sum().export_val)#Brazil graph data
gdf = cog.merge(brg, how="inner", on=brg.index)#graph data frame
gdf.rename(columns={"key_0":"year", "export_val_x":"export_val_co", "export_val_y":"export_val_br"}, inplace=True)
plt.plot( "year", "export_val_co",data=gdf, linewidth=2)
plt.plot( "year", "export_val_br", data=gdf, linewidth=2)
plt.legend()
#------------------------------------------------------------------
#Scaling and further graphing-----------------
from sklearn.preprocessing import MinMaxScaler
import datetime as dt
scaler = MinMaxScaler()
scog = cog.copy()#Creating copy for scaling
sbrg = brg.copy()#Creating copy for scaling
scog["export_val"] = scaler.fit_transform(np.array(scog.export_val).reshape(-1,1))
sbrg["export_val"] = scaler.fit_transform(np.array(sbrg.export_val).reshape(-1,1))
sgdf = scog.merge(sbrg, how="inner", on=sbrg.index)#graph data frame
sgdf.rename(columns={"key_0":"year", "export_val_x":"export_val_co", "export_val_y":"export_val_br"}, inplace=True)
plt.plot( "year", "export_val_co",data=sgdf, linewidth=2)
plt.plot( "year", "export_val_br", data=sgdf, linewidth=2)
plt.legend()#Outputs are proportionally higher with colombia between 1970 and 2003/5
#Shifting Brazilian data will not be useful in predicting Colombian coffee prices/outputs
#------------------------------------------------------------------
#Introducing price data--------------------
cf = pd.read_csv("coffee.csv")#load coffee data
cf.drop(columns=["Unnamed: 0"], inplace=True)
cf.rename(columns={"key_0":"year"}, inplace=True)
cf.year = pd.to_datetime(cf.year)
cf.set_index("year",inplace=True)
cf = cf.resample("Y").agg({"price": "median", "quantity": "sum"})
cf.index = cf.index.to_series().apply(lambda x: dt.datetime.strftime(x, '%Y')).tolist()
cf.index.name = "year"
cf = cf[2:-1]
gdf = gdf.merge(cf, how="inner", on=cf.index)# Standard graphing
total = []
for row in gdf.itertuples():
    total.append(row.price*((row.quantity*1000*60)*2.204623)/100)
gdf["totals"]= total
gdf.drop(columns=["key_0"], inplace=True)
plt.plot("year","export_val_co",data=gdf, linewidth=2)#cash value of quantity 
plt.plot("year","totals",data=gdf, linewidth=2)#cash value of quantity 

plt.plot("year","export_val_br", data=gdf, linewidth=2)#cash value of quantity 

#plt.plot("year","quantity", data=gdf, linewidth=2)#quantity

#plt.plot("year","price", data=gdf, linewidth=2)#price per thousand 60 kg bags
plt.legend()

#Visualize Coffee imports by country------------------------
#Drop germany from all years pre-1980 as it is a combination
# of east and west Germany
import plotly.graph_objects as go
import plotly
df = pd.read_csv("colombia_imports.csv")
df = df[df["dest"] != "World"]
df.index = df.year
df.index = pd.to_datetime(df.index,format="%Y")
df.drop(df[df.dest == "Democratic Republic of Germany"].index, inplace=True)
df.drop(df[df.dest == "Federal Republic of Germany"].index, inplace=True)
df["decade"] = df.year.astype(str).apply(lambda x: x[:3]+"0")
low = df[df.export_val < df[df.dest == "South Korea"].export_val]

def get_decade(df, decade):
    out = df[df.decade == decade]
    return out

def genSankey(df,cat_cols=[],value_cols='',title='Sankey Diagram'):
    # maximum of 6 value cols -> 6 colors
    colorPalette = ['#4B8BBE','#306998','#FFE873','#FFD43B','#646464']
    labelList = []
    colorNumList = []
    for catCol in cat_cols:
        labelListTemp =  list(set(df[catCol].values))
        colorNumList.append(len(labelListTemp))
        labelList = labelList + labelListTemp
        
    # remove duplicates from labelList
    labelList = list(dict.fromkeys(labelList))
    
    # define colors based on number of levels
    colorList = []
    for idx, colorNum in enumerate(colorNumList):
        colorList = colorList + [colorPalette[idx]]*colorNum
        
    # transform df into a source-target pair
    for i in range(len(cat_cols)-1):
        if i==0:
            sourceTargetDf = df[[cat_cols[i],cat_cols[i+1],value_cols]]
            sourceTargetDf.columns = ['source','target','count']
        else:
            tempDf = df[[cat_cols[i],cat_cols[i+1],value_cols]]
            tempDf.columns = ['source','target','count']
            sourceTargetDf = pd.concat([sourceTargetDf,tempDf])
        sourceTargetDf = sourceTargetDf.groupby(['source','target']).agg({'count':'sum'}).reset_index()
        
    # add index for source-target pair
    sourceTargetDf['sourceID'] = sourceTargetDf['source'].apply(lambda x: labelList.index(x))
    sourceTargetDf['targetID'] = sourceTargetDf['target'].apply(lambda x: labelList.index(x))
    
    # creating the sankey diagram
    data = dict(
        type='sankey',
        node = dict(
          pad = 15,
          thickness = 20,
          line = dict(
            color = "black",
            width = 0.5
          ),
          label = labelList,
          color = colorList
        ),
        link = dict(
          source = sourceTargetDf['sourceID'],
          target = sourceTargetDf['targetID'],
          value = sourceTargetDf['count']
        )
      )
    
    layout =  dict(
        title = title,
        font = dict(
          size = 10
        )
    )
       
    fig = dict(data=[data], layout=layout)
    return fig







fig = genSankey(get_decade(df,"1960"),cat_cols=["origin", "dest"],value_cols='export_val',title='Coffee Imports')
plotly.offline.plot(fig, validate=False)