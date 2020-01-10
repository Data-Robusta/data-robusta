import pandas as pd 
#Numbers are in thousands of 60KG bags

#Total Production--------------------------------
total_p = pd.read_excel("coffee_data/ico_data/total_prod.xlsx")
total_p.rename(columns={"Unnamed: 1":"coffee_type", "Crop year":"country_name"},inplace=True)
total_p_hold = total_p[["country_name", "coffee_type", "production_month"]]
total_p_hold = total_p_hold.iloc[1:]
total_p.drop(columns=["coffee_type", "production_month"],inplace=True)
total_p = total_p.iloc[1:]
total_p = total_p.melt(id_vars='country_name', var_name='year')
total_p = total_p.merge(total_p_hold, on='country_name', how='left')
total_p.rename(columns={"value":"total_production"},inplace=True)
total_p.dropna(subset=["country_name"], inplace=True)
total_p.to_csv("total_production.csv",index=False)
#-------------------------------------
#Domestic Consumption----------------------------
dom_con = pd.read_excel("coffee_data/ico_data/dom_con.xlsx")
dom_con.rename(columns={"Unnamed: 1":"coffee_type", "Crop year":"country_name"},inplace=True)
dom_con_hold = dom_con[["country_name", "coffee_type", "production_month"]]
dom_con_hold = dom_con_hold.iloc[1:]
dom_con.drop(columns=["coffee_type", "production_month"],inplace=True)
dom_con = dom_con.iloc[1:]
dom_con = dom_con.melt(id_vars='country_name', var_name='year')
dom_con = dom_con.merge(dom_con_hold, on='country_name', how='left')
dom_con.rename(columns={"value":"consumption"},inplace=True)
dom_con.dropna(subset=["country_name"], inplace=True)
dom_con.to_csv("domestic_consumption.csv",index=False)
#-------------------------------------
#Exportable Production--------------------------
export_p = pd.read_excel("coffee_data/ico_data/exp_prod.xlsx")
export_p.rename(columns={"Unnamed: 1":"coffee_type", "Crop year":"country_name"},inplace=True)
export_p_hold = export_p[["country_name", "coffee_type", "production_month"]]
export_p_hold = export_p_hold.iloc[1:]
export_p.drop(columns=["coffee_type", "production_month"],inplace=True)
export_p = export_p.iloc[1:]
export_p = export_p.melt(id_vars='country_name', var_name='year') #If returns error run by itself!
export_p = export_p.merge(export_p_hold, on='country_name', how='left') #If returns error run by itself!
export_p.rename(columns={"value":"exportable_consumption"},inplace=True)
export_p.dropna(subset=["country_name"], inplace=True)
export_p.to_csv("exportable_production.csv",index=False)
#-------------------------------------
#Gross opening stockpiles in all exporting countries
stock_pile = pd.read_excel("coffee_data/ico_data/gross_open.xlsx")
stock_pile.rename(columns={"Unnamed: 1":"coffee_type", "Crop year":"country_name"},inplace=True)
stock_pile_hold = stock_pile[["country_name", "coffee_type", "production_month"]]
stock_pile_hold = stock_pile_hold.iloc[1:]
stock_pile.drop(columns=["coffee_type", "production_month"],inplace=True)
stock_pile = stock_pile.iloc[1:]
stock_pile = stock_pile.melt(id_vars='country_name', var_name='year') #If returns error run by itself!
stock_pile = stock_pile.merge(stock_pile_hold, on='country_name', how='left') #If returns error run by itself!
stock_pile.rename(columns={"value":"beginning_stockpile"},inplace=True)
stock_pile.dropna(subset=["country_name"], inplace=True)
stock_pile.to_csv("beginning_stockpile.csv",index=False)
#-------------------------------------
#Total Exports-----------------------------------
exports = pd.read_excel("coffee_data/ico_data/exports.xlsx")
exports.rename(columns={"Unnamed: 1":"coffee_type", "Crop year":"country_name"},inplace=True)
exports_hold = exports[["country_name", "coffee_type", "production_month"]]
exports_hold = exports_hold.iloc[1:]
exports.drop(columns=["coffee_type", "production_month"],inplace=True)
exports = exports.iloc[1:]
exports = exports.melt(id_vars='country_name', var_name='year') #If returns error run by itself!
exports = exports.merge(exports_hold, on='country_name', how='left') #If returns error run by itself!
exports.rename(columns={"value":"total_exports"},inplace=True)
exports.dropna(subset=["country_name"], inplace=True)
exports.to_csv("total_exports.csv",index=False)
#-------------------------------------
#Imports--------------------------------------
imports = pd.read_excel("coffee_data/ico_data/imports.xlsx")
imports = imports.melt(id_vars='country_name', var_name='year')#If returns error run by itself!
imports = imports.iloc[1:]
imports.dropna(subset=["country_name"], inplace=True)
imports.to_csv("total_imports.csv",index=False)
#-------------------------------------
#Re-Exports-----------------------------------
re_exports = pd.read_excel("coffee_data/ico_data/re_exports.xlsx")
re_exports = re_exports.melt(id_vars='country_name', var_name='year')#If returns error run by itself!
re_exports = re_exports.iloc[1:]
re_exports.dropna(subset=["country_name"], inplace=True)
re_exports.to_csv("total_re_exports.csv",index=False)
#-------------------------------------
#Amount paid to Growers in USDCent per Pound--
prices = pd.read_excel("coffee_data/ico_data/prices_paid_to_growers.xlsx")
prices_hold = prices[["country_name", "Unnamed: 29"]]
prices.drop(columns=["Unnamed: 29"],inplace=True)
prices = prices.melt(id_vars='country_name', var_name='year') #If returns error run by itself!
prices = prices.merge(prices_hold, on='country_name', how='left') #If returns error run by itself!
prices.rename(columns={"value":"cents_per_lbs"},inplace=True)
prices.dropna(subset=["country_name"], inplace=True)
prices.to_csv("paid_to_growers.csv",index=False)
#-------------------------------------
#Retail Price of Coffee in USD per Pound-----
retail_prices = pd.read_excel("coffee_data/ico_data/retail_price.xlsx")
retail_prices = retail_prices.melt(id_vars='country_name', var_name='year') #If returns error run by itself!
retail_prices.rename(columns={"value":"dollars_per_lbs"},inplace=True)
retail_prices.dropna(subset=["country_name"], inplace=True)
retail_prices.to_csv("retail_prices.csv", index=False)
#--------------------------------------
#Columbian Coffee Price Per Month------------
col_prices = pd.read_excel("coffee_data/colu_coffee_data.xlsx", sheet_name="sheet3")
col_prices = col_prices.iloc[1:]
col_prices.drop(columns=["Unnamed: 0"], inplace=True)
col_prices.rename(columns={"Month-year":"date", "Unnamed: 2":"excelso_price_USDcents_per_lbs"}, inplace=True)
col_prices.to_csv("columbian_excelso_prices.csv",index=False)

col_production = pd.read_excel("coffee_data/colu_coffee_data.xlsx", sheet_name="sheet9")
col_production.drop(columns=["Unnamed: 0", "Unnamed: 3"], inplace=True)
col_production.to_csv("columbian_excelso_production.csv",index=False)
#-------------------------------------