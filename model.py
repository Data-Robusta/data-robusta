import pandas as pd
import numpy as np
from fbprophet import Prophet
from prepare import get_data, get_prepped, make_weighted, make_weighted_monthly
from fbprophet.diagnostics import cross_validation, performance_metrics
from sklearn.model_selection import ParameterGrid
from sklearn.preprocessing import StandardScaler
import pickle
import matplotlib.pyplot as plt
from predictions import get_model, store_model

# gets data without imputed weather values
data = get_data()

# creates new dataframe with Prophet-friendly column names
df = pd.DataFrame()
df['y'] = data.resample('M').inflated.mean()
df = df.reset_index()
df = df.rename(columns={'date': 'ds'})

# creates linear prophet model to fit only on the inflated price
m = Prophet(growth='linear')
m.fit(df)

future = m.make_future_dataframe(freq='D', periods=365*8)

forecast = m.predict(future)

cv = cross_validation(m, horizon='298 days')

performance_metrics(cv).rmse.mean() # RMSE: 135.51

# same as above, but multiplicative seasonality instead of additive
mult = Prophet(growth='linear', seasonality_mode='multiplicative')
mult.fit(df)

future_mult = mult.make_future_dataframe(freq='D', periods=365*8)

forecast_mult = mult.predict(future_mult)

cv_mult = cross_validation(mult, horizon='298 days')

performance_metrics(cv_mult).rmse.mean() # RMSE: 137.39

# creates dataframe for logistic Prophet model
df_log = df
df_log['floor'] = 0
df_log['cap'] = 1400

# creates and fits logistic Prophet model
m_log = Prophet(growth='logistic')
m_log.fit(df_log)

future_log = m_log.make_future_dataframe(freq='D', periods=365*8)
future_log['cap'] = 1400
future_log['floor'] = 0

forecast_log = m_log.predict(future_log)

cv_log = cross_validation(m_log, horizon='298 days')

performance_metrics(cv_log).rmse.mean() # RMSE: 137.53

# gets data with imputed missing values for multi-variate Prophet regressions
data = get_prepped()

# makes df for Prophet, drops the uninflated price column
df = pd.DataFrame()
df = data.drop(columns='price')
df = df.reset_index()

# renames columns to accomodate for Prophet
df = df.rename(columns={'date': 'ds', 'inflated': 'y'})

mv = Prophet()

# adds each column of weather data as a regressor
for col in df.drop(columns=['ds', 'y']):
    mv.add_regressor(col)

# fits and evaluates the Prophet model
mv.fit(df)

cv_mv = cross_validation(mv, horizon='298 days')

performance_metrics(cv_mv).rmse.mean() # RMSE: 209.81

# Creates dataframe with just date, inflated price, and quantity produced
dfq = df[['ds', 'y', 'quantity']]

q = Prophet()

q.add_regressor('quantity')

# fits and evaluates model on inflated price with quantity regressor
q.fit(dfq)

cv_q = cross_validation(q, horizon='298 days')

performance_metrics(cv_q).rmse.mean() # RMSE: 134.50

# creates dataframe with weather data shifted 12 months AND normal weather data
shifted_df = df

for col in shifted_df.drop(columns=['ds', 'y', 'quantity']):
    shifted_df[col +'_shifted'] = shifted_df[col].shift(12)

shifted_df = shifted_df.iloc[12:]

shifted = Prophet()

for col in shifted_df.drop(columns=['ds', 'y']):
    shifted.add_regressor(col)

shifted.fit(shifted_df)

cv_shift = cross_validation(shifted, horizon='298 days')

performance_metrics(cv_shift).rmse.mean() # RMSE: 1625.05

# same as above but with only shifted data
just_shift_df = df[['ds', 'y', 'quantity']]

for col in df.drop(columns=['ds', 'y', 'quantity']):
    just_shift_df[col +'_shifted'] = df[col].shift(12)

just_shift_df = just_shift_df.iloc[12:]

just = Prophet()

for col in just_shift_df.drop(columns=['ds', 'y']):
    just.add_regressor(col)

just.fit(just_shift_df)

cv_just = cross_validation(just, horizon='298 days')

performance_metrics(cv_just).rmse.mean() # RMSE 3516.03

# Model with scaled weather data from 95 to present
df = get_prepped()['1995':].drop(columns=['price'])

precip = [col for col in df.columns if col.endswith('precip')]

for col in precip:
    df.loc[df[df[col] < 0].index, col] = 0

cols = df.drop(columns='inflated').columns
scaler = StandardScaler().fit(df[cols])
df_scaled = pd.DataFrame(scaler.transform(df[cols]), columns=cols).set_index(df.index)
df_scaled['y'] = df.inflated
df_scaled = df_scaled.reset_index().rename(columns={'date':'ds'})

scal = Prophet()

for col in df_scaled.drop(columns=['ds', 'y']):
    scal.add_regressor(col)

scal.fit(df_scaled)

cv_scal = cross_validation(scal, horizon='298 days')

performance_metrics(cv_scal).rmse.mean() # RMSE: 352.43

df = get_prepped()['1995':]
df = df[['inflated', 'quantity']].reset_index().rename(columns={'inflated': 'y', 'date': 'ds'})
best_model = Prophet()
best_model.add_regressor('quantity')
best_model.fit(df)
best_cv = cross_validation(best_model, horizon='365 days')
store_model(best_model, 'best_model.p')
store_model(best_cv, 'best_cv.p')
best_performance = performance_metrics(best_cv)
store_model(best_performance, 'best_performance.p')

df = get_prepped()['1995':]
df = df.drop(columns='price').reset_index().rename(columns={'inflated': 'y', 'date': 'ds'})
weather_model = Prophet(growth='logistic')
df['floor'] = 50
df['cap'] = 350
for column in df.drop(columns={'y', 'ds', 'floor', 'cap'}).columns:
    weather_model.add_regressor(column)

weather_model.fit(df)
weather_cv = cross_validation(weather_model, horizon='365 days')
weather_performance = performance_metrics(weather_cv)

# weighted = make_weighted()
# weighted = weighted.reset_index()
# weighted = weighted.rename(columns={'date': 'ds', 'price': 'y'})
# weather = Prophet()
# for col in weighted.drop(columns=['y', 'ds']).columns:
#     weather.add_regressor(col)
# weather.fit(weighted)
# store_model(weather, 'weather_model.p')
# store_model(weather_cv, 'weaher_cv.p')
# weather_cv = cross_validation(weather, horizon='365 days')
# weather_performance = performance_metrics(weather_cv)
# store_model(weather_performance, 'weather_performance.p')

# weighted = make_weighted_monthly()
# weighted = weighted.reset_index()
# weighted = weighted.rename(columns={'date': 'ds', 'price': 'y'})
# weather_monthly = Prophet()
# for col in weighted.drop(columns=['y', 'ds']).columns:
#     weather_monthly.add_regressor(col)
# weather_monthly.fit(weighted)
# store_model(weather_monthly, 'weather_monthly_model.p')
# weather_monthly_cv = cross_validation(weather, horizon='365 days')
# store_model(weather_monthly_cv, 'weather_monthly_cv.p')
# weather_monthly_performance = performance_metrics(weather_monthly_cv)
# store_model(weather_monthly_performance, 'weather_monthly_performance.p')

# weighted = make_weighted()
# weighted = weighted.reset_index()
# weighted = weighted.rename(columns={'date': 'ds', 'price': 'y'})
# weather = Prophet()
# for col in weighted.drop(columns=['y', 'ds']).columns:
#     weather.add_regressor(col)
# weather.fit(weighted)
# store_model(weather, 'weather_model.p')
# weather_cv = cross_validation(weather, horizon='365 days')
# store_model(weather_cv, 'weather_cv.p')
# weather_performance = performance_metrics(weather_cv)
# store_model(weather_performance, 'weather_performance.p')

# weighted = make_weighted_monthly()
# weighted = weighted.reset_index()
# weighted = weighted.rename(columns={'date': 'ds', 'price': 'y'})
# weather_monthly = Prophet()
# for col in weighted.drop(columns=['y', 'ds']).columns:
#     weather_monthly.add_regressor(col)
# weather_monthly.fit(weighted)
# store_model(weather, 'weather_monthly_model.p')
# weather_monthly_cv = cross_validation(weather, horizon='365 days')
# store_model(weather_cv, 'weaher_monthly_cv.p')
# weather_monthly_performance = performance_metrics(weather_monthly_cv)
# store_model(weather_monthly_performance, 'weather_monthly_performance.p')

def run_weighted_model(monthly=False, quantity=False):
    if monthly:
        weighted = make_weighted_monthly(quantity)
        name = 'weather_monthly' + ('_quantity' * quantity)
    else:
        weighted = make_weighted(quantity)
        name = 'weather' + ('_quantity' * quantity)
    weighted = weighted.reset_index()
    weighted = weighted.rename(columns={'date': 'ds', 'price': 'y'})
    model = Prophet()
    for col in weighted.drop(columns=['y', 'ds']).columns:
        model.add_regressor(col)
    model.fit(weighted)
    store_model(model, name + '_model.p')
    model_cv = cross_validation(model, horizon='365 days')
    store_model(model_cv, name + '_cv.p')
    model_performance = performance_metrics(model_cv)
    store_model(model_performance, name + '_performance.p')

run_weighted_model()
run_weighted_model(monthly=True)
run_weighted_model(quantity=True)
run_weighted_model(monthly=True, quantity=True)