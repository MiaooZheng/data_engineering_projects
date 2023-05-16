import json
import requests
import pprint
import pandas as pd
import datetime
import os

# reference: https://www.cryptocompare.com/cryptopian/api-keys
# for mac, use export Apikey='xxx' to save credentials

# api_key = os.getenv('Apikey')
# print(api_key)


def extract_data():
    # here we do CAD as currency and choose binance coin as our cryptocurrency to predict with 1500 rows
    url = 'https://min-api.cryptocompare.com/data/v2/histoday?fsym=BNB&tsym=CAD&limit=1560'
    headers = {
        "Connection": "keep-alive",
        "Apikey": '0882e1f31ff414a8b9b48158b471a8c60a724377729ffdf2692a89c51937142d'
    }
    response = requests.get(url = url, headers = headers)
    # pprint.pprint(response.json())
    # raw_data = response.json()
    data = json.loads(response.text)['Data']['Data']
    pprint.pprint(data)
    df = pd.DataFrame.from_dict(pd.json_normalize(data), orient='columns')
    # convert epoch time to datetime
    df['time'] = df['time'].apply(lambda d: datetime.datetime.fromtimestamp(int(d)).strftime('%Y-%m-%d'))
    df = df.drop(columns = ['conversionType', 'conversionSymbol'], axis=1)
    print(df.shape)
    df.to_csv('datasci3ml_final_project_test.csv')
    return 'save the dataset successfully!'


def read_dataset():
    dataset = pd.read_csv('datasci3ml_final_project_dataset.csv')
    print(dataset.head(10))
    print(dataset.tail(10))

extract_data()

# reference: https://www.kaggle.com/code/meetnagadia/bitcoin-price-prediction-using-lstm