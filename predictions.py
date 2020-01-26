import prepare
import pickle
from fbprophet import Prophet
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

def store_model(model, filename):
    pickle.dump(model, open('models/' + filename, 'wb'))

def get_model(filename):
    model = pickle.load(open('models/' + filename, 'rb'))
    return model

def graph_models_fresh():
    pd.plotting.register_matplotlib_converters()
    best = get_model('best_model.p')
    weather = get_model('weather_model.p')

    df = prepare.get_prepped()

    best_df = best.make_future_dataframe(periods=0)
    best_df['quantity'] = df['1995':].reset_index()['quantity']

    weather_df = weather.make_future_dataframe(periods=0)
    weighted = get_model('weighted.p')
    weather_df['weighted_mean_precip'] = weighted['weighted_mean_precip']
    weather_df['weighted_mean_temp'] = weighted['weighted_mean_temp']

    best_forecast = best.predict(best_df)
    store_model(best_forecast, 'best_predictions.p')

    weather_forecast = weather.predict(weather_df)
    store_model(weather_forecast, 'weather_predictions.p')

    to_graph = best_forecast[['ds', 'yhat']]
    to_graph = to_graph.rename(columns={'ds': 'date', 'yhat': 'best_model'})

    to_graph = to_graph.set_index('date').resample('YS').mean()

    weather_future = weather_forecast[['ds', 'yhat']]
    weather_future = weather_future.rename(columns={'ds': 'date', 'yhat': 'weather_model'})
    weather_future = weather_future.set_index('date')

    to_graph['weather_model'] = weather_future['weather_model']

    to_graph['actual'] = df.resample('YS')['inflated'].mean()

    store_model(to_graph, 'to_graph.p')

    for col in to_graph.columns:
        to_graph[col].plot()

def graph_models():
    pd.plotting.register_matplotlib_converters()
    to_graph = get_model('to_graph.p')
    for col in to_graph.columns:
        sns.lineplot(x=to_graph.index, y=to_graph[col])
    plt.title('Models Compared to Actual Inflated Coffee Prices')
    plt.xlabel('Year')
    plt.ylabel('Coffee Price (2018 USD per lb)')
    plt.legend(to_graph.columns)
    plt.show()