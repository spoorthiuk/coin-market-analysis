from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import pandas as pd
url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
parameters = {
#  'start':'1',
  'limit':'5000',
#  'convert':'USD'
}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': '3accd41e-fe27-47aa-83f1-a1abc9e9ddf3',
}

session = Session()
session.headers.update(headers)

try:
    response = session.get(url, params=parameters)
    data = json.loads(response.text)
  #print(data)
except (ConnectionError, Timeout, TooManyRedirects) as e:
    print(e)
print(data)
column_keys = list(data['data'][0].keys())
column = list(data['data'][0].keys())
column.extend(list(data['data'][0]['quote']['USD'].keys()))
column_quote_keys = list(data['data'][0]['quote']['USD'].keys())
#column_keys.remove('quote')
result = {}
for col in column:
    if col != 'quote':
        result[col] = []
print(column_quote_keys)
print(column_keys)
print(column)
print(result)
for d in data['data']:
    for col in column_keys:
        if col == 'quote':
            for quote_col in column_quote_keys:
                try:
                    result[quote_col].append(d['quote']['USD'][quote_col])
                except:
                    result[quote_col].append('')
        else:
            if(col != 'last_updated'):
                try:
                    result[col].append(d[col])
                except:
                    result[col].append('')
for key in result.keys():
    print(len(result[key]))
    if len(result[key]) != 100:
        print(key)
dataframe = pd.DataFrame(result)
dataframe.to_csv('coin-market-historical.csv')
print(dataframe.head())