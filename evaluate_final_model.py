from predictions import get_model
from prepare import get_prepped

def evaluate_model(model_name='best', words=True, stability=True):
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
    
    if stability:
        stable_mask = ((df.index > '1995-11-01') & (df.index < '1997-02-01')) | ((df.index > '1998-05-01') & (df.index < '2000-09-01')) | ((df.index > '2005-01-01') & (df.index < '2009-06-01')) | (df.index > '2012-05-01')

        df_stable = df[stable_mask]

        stable_price = df_stable.y.mean()

        rmse_stable = df_stable.r2.mean() ** (1/2)

        pct_stable = rmse_stable / stable_price

        df_disaster = df[~stable_mask]

        disaster_price = df_disaster.y.mean()

        rmse_disaster = df_disaster.r2.mean() ** (1/2)

        pct_disaster = rmse_disaster / disaster_price
    
    if words:
        print(f'''The {model_name} model had an RMSE of {round(rmse, 2)}. This means on average it missed its guess by {round(pct * 100, 2)}% of the price.
During stable months, its RMSE was {round(rmse_stable, 2)}, and missed by {round(pct_stable * 100, 2)}% of the price.
During disaster months, its RMSE was {round(rmse_disaster, 2)}, and missed by {round(pct_disaster * 100, 2)}% of the price.''')
    else:
        print(model_name)
        print('RMSE:' + str(round(rmse, 2)))
        if stability:
            print('Stable:' + str(round(rmse_stable, 2)))
            print('Disaster:' + str(round(rmse_disaster, 2)))

if __name__ == '__main__':
    models = ['best', 'weather', 'weather_monthly', 'weather_quantity', 'weather_monthly_quantity', 'old_weather']
    for model in models:
        evaluate_model(model, words=False)