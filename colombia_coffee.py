import pandas as pd
import os
import cpi

def get_coffee(fresh=False):
    if os.path.exists('coffee_data/coffee.csv') and not fresh:
        coffee = pd.read_csv('coffee_data/coffee.csv', index_col=0)
    else:
        # read in price and quantity data
        prices = pd.read_excel('coffee_data/colu_coffee_data_original.xlsx', sheet_name=3, header=5, usecols=[1,2])
        quantities = pd.read_excel('coffee_data/colu_coffee_data.xlsx', sheet_name=9, usecols=[1,2])

        # Rename into English, simple names
        prices = prices.rename(columns={'Mes': 'date', 'Precio externo ': 'price'})
        quantities = quantities.rename(columns={'month/year': 'date', 'thousands_of_60kg_bags_production': 'quantity'})

        # Adjust prices into 2018 dollars
        prices['inflated'] = prices.apply(lambda x: cpi.inflate(x.price, x.date), axis=1)

        # Set index to date
        prices = prices.set_index('date')
        quantities = quantities.set_index('date')

        # Cut to just 1960 to 2018
        prices = prices['1960' : '2018']
        quantities = quantities['1960' : '2018']

        # Combine the two into one coffee dataframe
        coffee = pd.merge(left=prices, right=quantities, on=prices.index)
        coffee.to_csv('coffee_data/coffee.csv')
    return coffee



data_dict = {
    'price': 'Export price of excelso coffee in USD per lb',
    'inflated': 'Export price adjusted for inflation into 2018 dollars',
    'quantity': 'Thousands of 60kg bags of coffee exported'
}