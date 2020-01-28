from scipy.stats import shapiro
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

def get_temp_chart():
    plt.figure(figsize=(10,6))
    sns.regplot("date","mean_temp", data = df, ci=False, color="darkgreen", robust=True)
    plt.title("Average Temperature in Colombia", size=15)
    plt.xlabel("Date", size=13)
    plt.ylabel("Temperature in Fahrenheit ", size=13)
    plt.show()

def get_price_chart():
    plt.figure(figsize=(10,6))
    sns.regplot("date", "inflated", data=df, ci=False, color="darkgreen", robust=True)
    plt.title("Price of Colombain Coffe per Pound in USD", size=15)
    plt.xlabel("Date", size=13)
    plt.ylabel("Price in Cents", size=13)
    plt.show()


def get_stockpile_chart():
    df2 = pd.read_csv("coffee_data/ico_data_pandas/stockpile.csv")
    df2[df2.country_name == "Colombia"]
    df2.dropna(inplace=True)
    df2.year = df2.year.str[:4]
    df2.drop(columns=["country_name", "coffee_type", "production_month"], inplace=True)
    df2.year = pd.to_datetime(df2.year)
    df2.set_index(df2.year, inplace=True)
    df2 = df2.resample("Y").sum()
    df2["date"] = df2.index.astype(str).str[:4].astype(int)
    plt.figure(figsize=(10,6))
    sns.lmplot("date", "beginning_stockpile",data = df2)
    plt.title("Stockpiles of Coffee Colombia")
    plt.xlabel("Date")
    plt.ylabel("Stockpile")
    plt.show()



def get_precip_chart():
    plt.figure(figsize=(10,6))
    sns.regplot("date","mean_precip", data = df, ci=False, color="darkgreen", robust=True)
    plt.title("Average Precipitation in Colombia", size=15)
    plt.xlabel("Date", size=13)
    plt.ylabel("Precipitation in Centimeters ", size=13)
    plt.show()