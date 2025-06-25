import json
import logging
import os
from datetime import datetime

import pandas as pd
import requests
from dotenv import load_dotenv

from src.views import hi_time

# path1 = os.path.abspath(os.path.join('logs', 'utils.log'))
# path2 = os.path.abspath(os.path.join('date', 'operations.xlsx'))
# path3 = os.path.abspath(os.path.join('user_settings.json'))
path1 = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs', 'utils.log')
path2 = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'date', 'operations.xlsx')
path3 = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'user_settings.json')

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(path1, encoding='utf-8')
file_formatter = logging.Formatter('%(asctime)s %(filename)s %(levelname)s: %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

"""Загрузка переменных"""
load_dotenv()

'''Формируем приветственную фразу'''
current_date = datetime.now()
greeting = hi_time()


def get_external_xls(path: str) -> pd.DataFrame:
    '''Функция принимает файл Excel и возвращает датафрейм с переименованными столбцами'''
#    my_dict = {}
#    my_list = []
    try:
        logger.info(f'Файо найден {path}')
        excel_data = pd.read_excel(path)
        df_full = excel_data.copy()
        list_del = [1, 3, 4, 7, 10, 12, 13]
        df = df_full.drop(df_full.columns[list_del], axis=1)
#        df = excel_data.iloc[:, [0, 2, 5, 6, 8, 9, 11, 14]]
        newcols = {'Дата операции': 'date',
                   'Номер карты': 'cards',
                   'Сумма операции с округлением': 'amount',
                   'Валюта операции': 'currency',
                   'Сумма платежа': 'payments',
                   'Кэшбэк': 'cashback',
                   'Категория': 'category',
                   'Описание': 'description'
                   }
        df.rename(columns=newcols, inplace=True)
    except FileNotFoundError:
        logger.error(f'Файл не найден')
        raise FileNotFoundError("Файл не найден")

    return df


def filter_for_date(df: pd.DataFrame, date_begin: str, date_out: str) -> pd.DataFrame:
    '''Отфильтровываем датафрейм по диапазону дат и убираем значение NaN'''

    date_begin = datetime.strptime(date_begin, '%Y-%m-%d %H:%M:%S')
    date_out = datetime.strptime(date_out, '%Y-%m-%d %H:%M:%S')
    df.date = pd.to_datetime(df.date)
    df_filt_data = df.loc[(df.date >= date_begin) & (df.date <= date_out)]
    print(type(df.date))
    print(df_filt_data)
    df_filter = df_filt_data.loc[df_filt_data.cards.notnull()]
    df_filter['cashback'].fillna(0, inplace=False)
    logger.info('Датафрейм отфильтрован в выбранном диапазоне, убран NaN')
    return df_filter


def grupp_in_cards(df: pd.DataFrame) -> dict:
    '''Группируем транзакции по номерам карт'''
    df_grupp = df.groupby('cards').agg({
        "amount": 'sum',
        "cashback": 'sum'
    })
    list_cards = df_grupp.reset_index().to_dict(orient='records')
    logger.info('Транзакции сгруппированы по номерам карт')
    card_list = []
    resul = {}

    for i in list_cards:
        mask = get_mask_card_numb(i["cards"])
        resul = {
            "last_digits": mask, "total_spent": i["amount"], "cashback": i["cashback"]}
        card_list.append(resul)
        logger.info('Сформирован список сумм платежей и кэшбека для каждой карты')
#   result = {
#        "greeting": greeting, "cards": card_list, "top_transactions": trans_list, "currency_rates": list_currency,
#        "stock_prices": list_stocks
#    }
#    logger.info(f'Сформирован словарь для передачи в JSON')
    return card_list


def get_mask_card_numb(number_card: str) -> str:
    """Функция возвращает маску номера банковской карты"""
    logger.info('Маска банковской карты выполнена')
    return str(number_card)[1:]


# def format_date(date: str) -> str:
#     '''Изменяем формат даты'''
#     date_now = date.strftime("%d.%m.%Y")
#     logger.info(f'Дата операции преобразована в строку {date_now}')
#     return date_now


def sorted_by_amount(df: pd.DataFrame) -> list:
    '''Сортируем датафрейм по сумме'''
    df_amount = df.sort_values(by='amount', ascending=False)
    logger.info('Датафрейм отсортирован по сумме платежа')
    trans_list = []
    resul = {}
    list_tr = df_amount.head(5).to_dict(orient='records')
    for i in list_tr:
        resul = {
            "date": i["date"], "amount": i["amount"], "category": i["category"],
            "description": i["description"]
        }
        trans_list.append(resul)
        logger.info('Сформирован список топ-5 транзакций')
    return trans_list


with open(path3, 'r') as file:
    data = json.load(file)
    currency = data["user_currencies"]
    symbols = ",".join(currency)
    user_stocks = data["user_stocks"]
    logger.info('Определены параметры для запросов к API {symbols}, {user_stocks}')


def get_user_latest(symbols: str) -> list:
    '''Функция запрашивает курсы валют и преобразует в список словарей'''
    logger.info('Направлен запрос на получение курса валют')
    url = f"https://api.apilayer.com/exchangerates_data/latest?symbols={symbols}&base=RUB"
    headers = {'apikey': os.getenv('API_KEY')}
    response = requests.get(url, headers=headers)
    result = response.json()
    my_list = []
    my_dict = result["rates"]
    for key, value in my_dict.items():
        new_dict = {"currency": key, "rate": value}
        my_list.append(new_dict)
    if response.status_code != 200:
        logger.error('Ошибка обращения к API')
        return 'Ошибка при обращении к API 400 - error'

    return my_list


def get_user_stocks(user_stocks: list) -> list:
    '''Функция получает с API котировки акций и преобразует в список словарей '''
    logger.info('Направляем запросы на получение курса акций')
    my_list = []
    for stock in user_stocks:
        url = (f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={stock}&apikey='
               f'{os.getenv('API__KEY')}')
        r = requests.get(url)
        data = r.json()
        m_dict = data.get('Global Quote')
        my_dict = {"stock": m_dict['01. symbol'], "price": m_dict['05. price']}
        my_list.append(my_dict)

        if r.status_code != 200:
            print(f"{r.status_code}Ошибка при обращении к API 400 - error")
            logger.error('Ошибка обращения к API')
            return 'Ошибка при обращении к API 400 - error'
    return my_list


if __name__ == "__main__":
    df = get_external_xls(path2)
    df_filtr = filter_for_date(df, '2021-05-01 00:00:00', '2021-05-05 00:00:00')
    print(df_filtr)
#     res = get_user_stocks("AAPL")
#     print(res)

#    result = get_external_xls(path2)
#    print(result)

#
#
#    list_card = grupp_in_cards(df_filtr)
#    print(list_card)
# print(get_mask_card_number("*3611"))
