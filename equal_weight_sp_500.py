import numpy as np
import pandas as pd
import requests
import xlsxwriter
import math

from secrets import IEX_CLOUD_API_TOKEN

def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

portfolio_size = input('Enter value of your portfolio: ')

try:
    val = float(portfolio_size)
except ValueError:
    print("That's not a number!\nPlease try again:")
    portfolio_size = input('Enter value of your portfolio: ')
    val = float(portfolio_size)

stocks = pd.read_csv('sp_500_stocks.csv')

my_columns = ['Ticker', 'Stock Price', 'Market Capitalisation', 'Number of Shares to Buy']
symbol_groups = list(chunks(stocks['Ticker'], 100))
symbol_strings = []

for i in range(0, len(symbol_groups)):
    symbol_strings.append(','.join(symbol_groups[i]))

final_dataframe = pd.DataFrame(columns=my_columns)

for symbol_string in symbol_strings:
    batch_api_call_url = f'https://sandbox.iexapis.com/stable/stock/market/batch?symbols={symbol_string}&types=quote&token={IEX_CLOUD_API_TOKEN}'
    data = requests.get(batch_api_call_url).json()

    for symbol in symbol_string.split(','):
        final_dataframe = final_dataframe.append(pd.Series([symbol, 
        data[symbol]['quote']['latestPrice'], 
        data[symbol]['quote']['marketCap'], 'N/A'], 
        index=my_columns), ignore_index=True) 

position_size = val/len(final_dataframe.index)
for i in range(0, len(final_dataframe.index)):
    final_dataframe.loc[i, 'Number of Shares to Buy'] = math.floor(position_size/final_dataframe.loc[i, 'Stock Price'])

writer = pd.ExcelWriter('recommended_trades.xlsx', engine='xlsxwriter')
final_dataframe.to_excel(writer, 'Recommended Trades', index=False)

print(final_dataframe)