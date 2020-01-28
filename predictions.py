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

def make_predictions(model_dict, monthly=True):
    model_name = model_dict['name']
    model = get_model(model_name + '_model.p')

    model_data = model_dict['data']
    model_data = model_data.reset_index()
    model_df = model.make_future_dataframe(periods=0)

    if len(model_df) > 288:
        model_df = model_df.iloc[-288:]
        model_df = model_df.reset_index()

    regressors = model.train_component_cols.drop(columns=['additive_terms', 'extra_regressors_additive', 'yearly', 'multiplicative_terms']).columns
    for regressor in regressors:
        model_df[regressor] = model_data[regressor]

    model_forecast = model.predict(model_df)
    store_model(model_forecast, model_name + '_predictions.p')

    to_graph = model_forecast[['ds', 'yhat']]
    to_graph = to_graph.rename(columns={'ds':'date', 'yhat': model_name})
    to_graph = to_graph.set_index('date')

    if not monthly:
        to_graph = to_graph.resample('QS').mean()

    return model_forecast, to_graph

def prep_models_fresh(monthly=False, final=False):
    df = prepare.get_prepped()
    weighted = prepare.make_weighted()
    weighted_monthly = prepare.make_weighted_monthly()
    weighted_q = prepare.make_weighted(quantity=True)
    weighted_monthly_q = prepare.make_weighted_monthly(quantity=True)

    models= [{'name': 'best', 'data': df['1995':]}, 
            {'name': 'weather', 'data': weighted}, 
            {'name': 'weather_monthly', 'data': weighted_monthly}, 
            {'name': 'weather_quantity', 'data': weighted_q}, 
            {'name': 'weather_monthly_quantity', 'data': weighted_monthly_q},
            {'name': 'old_weather', 'data': df['1995':]},
            {'name': 'entire_time', 'data': df}]

    if final:
        models = [models[5], models[6]]

    elif monthly:
        models = [models[0], models[2], models[4], models[5], models[6]]

    for model in models:
        model['forecast'], model['graph'] = make_predictions(model, monthly=monthly)

    to_graph = pd.DataFrame()
    
    to_graph['date'] = models[0]['graph'].index
    to_graph = to_graph.set_index('date')

    for model in models:
        name = model['name']
        to_graph[name] = model['graph']
    
    if monthly:
        to_graph['actual'] = df['inflated']
    else:
        to_graph['actual'] = df.resample('QS')['inflated'].mean()

    store_model(to_graph, 'to_graph.p')

def graph_models(fresh=False, monthly=True, final=True):
    pd.plotting.register_matplotlib_converters()
    if fresh:
        prep_models_fresh(monthly=monthly, final=final)
    to_graph = get_model('to_graph.p')
    for col in to_graph.columns:
        sns.lineplot(x=to_graph.index, y=to_graph[col])
    plt.title('Models Compared to Actual Inflated Coffee Prices')
    if monthly:
        plt.xlabel('Date')
    else:
        plt.xlabel('Year')
    plt.ylabel('Coffee Price (2018 USD per lb)')
    plt.legend(to_graph.columns)
    plt.show()

def graph_model(model_name, model_title):
    pd.plotting.register_matplotlib_converters()
    to_graph = get_model('to_graph.p')
    to_graph = to_graph.resample('QS').mean()
    sns.lineplot(x=to_graph.index, y=to_graph[model_name], color='olivedrab', linewidth=3)
    sns.lineplot(x=to_graph.index, y=to_graph['actual'], color='burlywood')
    plt.title('Models Compared to Actual Inflated Coffee Prices', size=15)
    plt.ylabel('Coffee Price (2018 USD per lb)', size=13)
    plt.xlabel('Date', size=13)
    plt.legend(labels=[model_title, 'Actual Prices'])
    plt.show()

def graph_two_models(names, titles):
    pd.plotting.register_matplotlib_converters()
    to_graph = get_model('to_graph.p')
    to_graph = to_graph.resample('QS').mean()
    
    sns.lineplot(x=to_graph.index, y=to_graph[names[0]], color='silver')
    sns.lineplot(x=to_graph.index, y=to_graph[names[1]], color='olivedrab', linewidth=3)
    sns.lineplot(x=to_graph.index, y=to_graph['actual'], color='burlywood')
    plt.title('Models Compared to Actual Inflated Coffee Prices', size=15)
    plt.ylabel('Coffee Price (2018 USD per lb)', size=13)
    plt.xlabel('Date', size=13)
    plt.legend(labels=[titles[0], titles[1], 'Actual Prices'])
    plt.show()