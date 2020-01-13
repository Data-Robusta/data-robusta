import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from fbprophet import Prophet
import warnings
warnings.filterwarnings("ignore")
from sklearn.metrics import mean_squared_error
pd.plotting.register_matplotlib_converters()
from fbprophet.diagnostics import cross_validation, performance_metrics
import numpy as np
from prepare import get_data

df = pd.read_csv("coffee.csv")
df.rename(columns=({"price_adjusted_inflation":"price"}), inplace=True)
df.drop(columns=["excelso_price_cents_per_pound", "thousands_of_60kg_bags_production"], inplace=True)
df["ds"] = pd.to_datetime(df.date)
df["y"] = df.price
df.drop(columns=["date", "price"],inplace=True)

def split_data(df, train_prop=.95): 
    train_size = int(len(df) * train_prop)
    train, test = df[0:train_size].reset_index(), df[train_size:len(df)].reset_index()
    return train, test


train, test = split_data(df, train_prop=.85)


m = Prophet()
m.fit(train)
future = m.make_future_dataframe(periods=len(test)*30)
future['cap'] = 1400
future['floor'] = 0
forecast = m.predict(future)
m.plot(forecast)
out = forecast[["ds","yhat"]]
out.set_index("ds",inplace=True)
out = out.resample("M").mean()
trainy, y_pred = split_data(out, train_prop=.85)
#baseline with mean
mean_squared_error(test.y.tolist(), [train.y.mean()]*len(test.y))
mean_squared_error(test[:-1].y.tolist(), y_pred.yhat.tolist())


