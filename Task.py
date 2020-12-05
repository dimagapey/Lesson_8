import requests
import json
import datetime
import argparse
from pprint import pprint as pp


def symbols():
    with open('symbols.json', 'r') as file:
        symbols_file = json.load(file)
    return symbols_file


def get_values(arguments, symbols_file):
    currency_from = arguments.currency_from
    if currency_from.upper() not in symbols_file['symbols']:
        print('Введите корректную валюту(по умолчанию USD)')
        currency_from = 'USD'
    currency_to = arguments.currency_to
    if currency_to.upper() not in symbols_file['symbols']:
        print('Введите корректную валюту(по умолчанию UAH)')
        currency_to = 'UAH'
    try:
        amount = float(arguments.amount)
    except ValueError:
        amount = 100.00
        print('Сумма должна быть числом(по умолчанию 100.00)')
    try:
        if arguments.start_date:
            start_date = datetime.datetime.strptime(arguments.startdate, '%Y-%m-%d')
            if start_date > datetime.datetime.now():
                start_date = datetime.datetime.now()
        else:
                start_date = datetime.datetime.now()
    except ValueError:
        start_date = datetime.datetime.now()
        print(f'Некорректная дата, вводите в формате {start_date}')
    return convert(currency_from, currency_to, amount, start_date)




def convert(currency_from, currency_to, amount, start_date):
    result = [['date', 'from', 'to', 'amount', 'rate', 'result']]
    while start_date <= datetime.datetime.now():
        request = requests.get('https://api.exchangerate.host/convert',
                               params={'from': currency_from, 'to': currency_to,
                                       'amount': amount, 'date': start_date})
        data = request.json()
        result.append([data['date'],
                       data['query']['from'],
                       data['query']['to'],
                       data['query']['amount'],
                       data['info']['rate'],
                       data['result']])
        start_date += datetime.timedelta(days=1)
        pp(result)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Exchange rates')
    parser.add_argument('currency_from')
    parser.add_argument('currency_to')
    parser.add_argument('amount')
    parser.add_argument("--start_date")
    arguments = parser.parse_args()
    get_values(arguments, symbols())
