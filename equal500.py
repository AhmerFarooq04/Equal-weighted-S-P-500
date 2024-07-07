import numpy as np
import pandas as pd
import math
import xlsxwriter
import requests
API_TOKEN = '(Your API token here)'

def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]
        

stocks = pd.read_csv('sp_500_stocks.csv')
my_columns = ['Ticker', 'Price','Volume', 'Number Of Shares to Buy']
symbol_groups = list(chunks(stocks['Ticker'], 100))
symbol_strings = []
for i in range(0, len(symbol_groups)):
    symbol_strings.append(','.join(symbol_groups[i]))
  
final_dataframe = pd.DataFrame(columns = my_columns)

for symbol in stocks['Ticker'][:5]:
    url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={API_TOKEN}'
    data = requests.get(url).json()
    print(data)
    final_dataframe = final_dataframe._append(
                                        pd.Series([symbol, 
                                                   data['Global Quote']['05. price'], 
                                                   data['Global Quote']['06. volume'], 
                                                   'N/A'], 
                                                  index = my_columns), 
                                        ignore_index = True)
#print (final_dataframe)
portfolio_size = input("Enter the value of your portfolio:")

try:
    val = float(portfolio_size)
except ValueError:
    print("That's not a number! \n Try again:")
    portfolio_size = input("Enter the value of your portfolio:")
    
position_size = float(portfolio_size) / len(final_dataframe.index)
for i in range(0, len(final_dataframe['Ticker'])):
    final_dataframe.loc[i, 'Number Of Shares to Buy'] = math.floor(position_size / float(final_dataframe['Price'][i]))
print(final_dataframe)