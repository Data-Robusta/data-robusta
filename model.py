import pandas as pd
from fbprophet import Prophet
from prepare import get_data
from fbprophet.diagnostics import cross_validation, performance_metrics
from sklearn.model_selection import ParameterGrid

data = get_data()
df = pd.DataFrame()
df['y'] = data.resample('M').inflated.mean()
df = df.reset_index()
df = df.rename(columns={'date': 'ds'})

m = Prophet(growth='linear')
m.fit(df)

future = m.make_future_dataframe(freq='D', periods=365*8)

forecast = m.predict(future)

cv = cross_validation(m, horizon='298 days')

performance_metrics(cv).rmse.mean() # RMSE: 135.51

mult = Prophet(growth='linear', seasonality_mode='multiplicative')
mult.fit(df)

future_mult = mult.make_future_dataframe(freq='D', periods=365*8)

forecast_mult = mult.predict(future_mult)

cv_mult = cross_validation(mult, horizon='298 days')

performance_metrics(cv_mult).rmse.mean() # RMSE: 137.39

df_log = df
df_log['floor'] = 0
df_log['cap'] = 1400

m_log = Prophet(growth='logistic')
m_log.fit(df_log)

future_log = m_log.make_future_dataframe(freq='D', periods=365*8)
future_log['cap'] = 1400
future_log['floor'] = 0

forecast_log = m_log.predict(future_log)

cv_log = cross_validation(m_log, horizon='298 days')

performance_metrics(cv_log).rmse.mean() # RMSE: 137.53

data = get_data()

df = pd.DataFrame()
df = data.drop(columns='price')
df = df.reset_index()

df = df.rename(columns={'date': 'ds', 'inflated': 'y'})

mv = Prophet()

for col in df.drop(columns=['ds', 'y']):
    mv.add_regressor(col)

mv.fit(df)

cv_mv = cross_validation(mv, horizon='298 days')

performance_metrics(cv_mv).rmse.mean() # RMSE: 