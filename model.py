import pandas as pd
from fbprophet import Prophet
from prepare import get_data
from fbprophet.diagnostics import cross_validation, performance_metrics

data = get_data()
df = pd.DataFrame()
df['y'] = data.resample('M').inflated.mean()
df = df.reset_index()
df = df.rename(columns={'date': 'ds'})