# Напишите на любом языке программирования следующую задачу:
# 1. Вытащить из апи Центробанка (пример http://www.cbr.ru/scripts/XML_daily_eng.asp?date_req=11/11/2020) данные по переводу различных валют в рубли за последние 90 дней.
# 2. Результатом работы программы:  
#  - нужно указать значение максимального курса валюты, название этой валюты и дату этого максимального значения.
#  - нужно указать значение минимального курса валюты, название этой валюты и дату этого минимального значения.
#  - нужно указать среднее значение курса рубля за весь период по всем валютам.
import requests
from datetime import date, timedelta
from xml.etree import ElementTree


def get_currency_rates(start_date, end_date):
    url_template = 'http://www.cbr.ru/scripts/XML_daily_eng.asp?date_req={}'
    delta = timedelta(days=1)
    currency_rates = []

    while start_date <= end_date:
        url = url_template.format(start_date.strftime('%d/%m/%Y'))
        response = requests.get(url)
        xml_root = ElementTree.fromstring(response.content)
        for currency in xml_root.findall('.//Valute'):
            currency_name = currency.find('Name').text
            currency_code = currency.find('CharCode').text
            currency_rate = float(currency.find('Value').text.replace(',', '.'))
            currency_date = start_date
            currency_rates.append((currency_name, currency_code, currency_rate, currency_date))
        start_date += delta

    return currency_rates


def get_max_rate(currency_rates):
    max_rate = 0
    max_currency_name = ''
    max_currency_date = None
    for name, code, rate, date in currency_rates:
        if rate > max_rate:
            max_rate = rate
            max_currency_name = name
            max_currency_date = date
    return max_rate, max_currency_name, max_currency_date


def get_min_rate(currency_rates):
    min_rate = float('inf')
    min_currency_name = ''
    min_currency_date = None
    for name, code, rate, date in currency_rates:
        if rate < min_rate:
            min_rate = rate
            min_currency_name = name
            min_currency_date = date
    return min_rate, min_currency_name, min_currency_date


def get_mean_rate(currency_rates):
    total_rate = 0
    count = 0
    for name, code, rate, date in currency_rates:
        total_rate += rate
        count += 1
    mean_rate = total_rate / count
    return mean_rate


if __name__ == '__main__':
    start_date = date.today() - timedelta(days=90)
    end_date = date.today()
    currency_rates = get_currency_rates(start_date, end_date)

    max_rate, max_currency_name, max_currency_date = get_max_rate(currency_rates)
    print('Максимальный курс:', max_rate, 'рублей - валюты', max_currency_name, 'от', max_currency_date.strftime("%d-%m-%Y"))

    min_rate, min_currency_name, min_currency_date = get_min_rate(currency_rates)
    print('Минимальный курс:', min_rate, 'рублей - валюты', min_currency_name, 'от', min_currency_date.strftime("%d-%m-%Y"))

    mean_rate = get_mean_rate(currency_rates)
    print('Средний курс:', "{:10.4f}".format(mean_rate), 'рублей.')