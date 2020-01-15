import pandas as pd
from fbprophet import Prophet
from prepare import get_data, get_prepped
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

data = get_prepped()

df = pd.DataFrame()
df = data.drop(columns='price')
df = df.reset_index()

df = df.rename(columns={'date': 'ds', 'inflated': 'y'})

mv = Prophet()

for col in df.drop(columns=['ds', 'y']):
    mv.add_regressor(col)

mv.fit(df)

cv_mv = cross_validation(mv, horizon='298 days')

performance_metrics(cv_mv).rmse.mean() # RMSE: 209.81

dfq = df[['ds', 'y', 'quantity']]

q = Prophet()

q.add_regressor('quantity')

q.fit(dfq)

cv_q = cross_validation(q, horizon='298 days')

performance_metrics(cv_q).rmse.mean() # RMSE: 134.50

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