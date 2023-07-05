import requests
import json


API_ID = '472d516006c24ec793199e894bda8e85'

def exchange_currency():
    response = requests.get(f'https://openexchangerates.org/api/latest.json?app_id={API_ID}')

    data = json.loads(response.text)
    rates = data['rates']
    filter_rates = {
        'RUB': rates['RUB'],
        'KGS': rates['KGS'],
        'KZT': rates['KZT'],
        'TRY': rates['TRY'],
        'CNY': rates['CNY'],
        'AED': rates['AED'],
        'GBP': rates['GBP'],
        'EUR': rates['EUR'],
        'JOD': rates['JOD'],
    }
    # result_list = []
    # for key, value in filter_rates.items():
        # result = key,' - ',value
        # result_list.append(result)
    return filter_rates
# exchange_currency()