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

future = m.make_future_dataframe(freq='D', periods=365*20)

forecast = m.predict(future)

cv = cross_validation(m, horizon='298 days')

performance_metrics(cv).rmse.mean() # 135.35

df_log = df
df_log['floor'] = 0
df_log['cap'] = 1400

m_log = Prophet(growth='logistic')
m_log.fit(df_log)

future_log = m_log.make_future_dataframe(freq='D', periods=365*20)
future_log['cap'] = 1400
future_log['floor'] = 0

forecast_log = m_log.predict(future_log)

cv_log = cross_validation(m_log, horizon='298 days')

performance_metrics(cv_log).rmse.mean() # 137.86

