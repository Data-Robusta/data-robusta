import pandas as pd 
df = pd.read_csv("coffee_export_numbers.csv")
df = df.fillna(0)


