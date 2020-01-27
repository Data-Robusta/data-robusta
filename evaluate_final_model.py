from predictions import get_model
from prepare import get_prepped

def evaluate_model(model_name='best'):
    # gets predictions of our best model from 1995 to 2018
    df = get_model(model_name + '_predictions.p')

    # cuts out the only relevant features, the date and the actual predicted values
    df = df[['ds', 'yhat']]

    # goes and gets our prepared dataframe to find the actual values
    data = get_prepped()

    # cuts out the actual values and 
    data = data['inflated']
    data = data['1995':]
    df = df.set_index('ds')
    df['y'] = data
    df['residual'] = df.y - df.yhat
    df['r2'] = df.residual ** 2

    avg_price = df.y.mean()

    rmse = df.r2.mean() ** (1/2)

    pct = rmse / avg_price

    df = df[((df.index > '1995-11-01') & (df.index < '1997-02-01')) | ((df.index > '1998-05-01') & (df.index < '2000-09-01')) | ((df.index > '2005-01-01') & (df.index < '2009-06-01')) | (df.index > '2012-05-01')]

    stable_price = df.y.mean()

    rmse_stable = df.r2.mean() ** (1/2)

    pct_stable = rmse_stable / stable_price

    print(f'''The {model_name} model had an RMSE of {round(rmse, 2)}. This means on average it missed its guess by {round(pct * 100, 2)}% of the price.
During stable months, its RMSE was {round(rmse_stable, 2)}, and missed by {round(pct_stable * 100, 2)}% of the price.''')

models = ['best', 'weather', 'weather_monthly', 'weather_q', 'weather_monthly_q']