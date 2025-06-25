import json
import logging
import os
from datetime import datetime
from dotenv import load_dotenv
from src.reports import filter_period, spending_by_category
from src.services import get_searh_to_string
from src.utils import (filter_for_date, get_external_xls, get_user_latest, get_user_stocks, grupp_in_cards,
                       sorted_by_amount)
from src.views import hi_time, find_begin_month


"""Формируем абсолютные пути к файлам"""
path1 = os.path.abspath(os.path.join("logs", "utils.log"))
path2 = os.path.abspath(os.path.join("date", "operations.xlsx"))
path3 = os.path.abspath(os.path.join("user_settings.json"))
# path1 = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs', 'main.log')
# path2 =  os.path.join(os.path.dirname(os.path.dirname(__file__)), 'date', 'operations.xlsx')
# path3 = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'user_settings.json')

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(path1, encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s %(filename)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

'''Формируем код для страницы "Главная"'''
logger.info('Формируем код для страницы "Главная"')

"""Загрузка переменных"""
load_dotenv()

"""Формируем приветственную фразу"""
current_date = datetime.now()
greeting = hi_time()
logger.info("Определено приветствие")

"""Создаем датафрейм, отфильтровываем нужные и переименовываем столбцы"""
df = get_external_xls(path2)
logger.info("Датафрейм создан. Столбцы переименованы")

"""Определяем диапазон дат для анализа"""
print("Нужно ввести дату окончания выборки транзакций в формате YYYY-MM-DD HH:MM:SS")
print("Выборка будет сделана от начала текущего месяца до указанной даты")
print("Если дата не введена - диапазон будет определяться от текущей даты")
print("Будете вводить дату? Да/Нет")
choice = input()
while choice not in ["Да", "да", "Нет", "нет"]:
    print("Некорректный термин. Введите заново")
    choice = input()
if choice in ["Нет", "нет"]:
    data_time = datetime.now()
    data_out = data_time.strftime("%Y-%m-%d %H:%M:%S")

else:
    print("Введите дату в формате YYYY-MM-DD HH:MM:SS")
    data_out = input()


date_begin, date_out = find_begin_month(data_out)
logger.info("Определен диапазон дат для анализа от начала месяца до указанной даты")

"""Отфильтровываем датафрейм по диапазону дат"""
df_filter = filter_for_date(df, date_begin, date_out)
logger.info("Датафрейм отфильтрован по выбранному диапазону дат")

"""Сортируем датафрейм по сумме и преобразуем в список словарей"""
list_trans = sorted_by_amount(df_filter)
logger.info("Датафрейм отсортирован по сумме")
print(list_trans)

"""Получаем параметры из JSON, курс валют из API и преобразуем в список словарей"""
with open(path3, "r") as file:
    data = json.load(file)
    currency = data["user_currencies"]
    symbols = ",".join(currency)
    list_currency = get_user_latest(symbols)
    logger.info("Получены курсы валют из API")

"""Получаем параметры из JSON, котировки акций из API и преобразуем в список словарей"""
with open(path3, "r") as file:
    data = json.load(file)
    user_stocks = data["user_stocks"]
    list_stocks = get_user_stocks(user_stocks)
    logger.info("Получены курсы акций из API")

"""Группируем по номерам карт и формируем словарь для JSON"""
card_list = grupp_in_cards(df_filter)
dict_data = {
    "greeting": greeting,
    "cards": card_list,
    "top_transactions": list_trans,
    "currency_rates": list_currency,
    "stock_prices": list_stocks,
}
logger.info("Сформирован словарь для JSON-ответа")
# print(dict_data)

'''Формируем JSON-ответ для страницы "Главная"'''
json_data = json.dumps(dict_data, indent=4, ensure_ascii=False)
logger.info('Сформирован JSON-ответ для страницы "Главная"')
print(json_data)

"""Запускаем сервис "Поиск транзакций" по ключевому слову в категории или описании"""

print("Введите ключевое слово для поиска в категориях или описании транзакций!")
print("Например, фастфуд или Супермаркеты")
word_key = input()

"""Формируем список для JSON"""
list_data = get_searh_to_string(path2, word_key)
while len(list_data) == 0:
     print("Нет таких слов в категориях или описании транзакций. Введите другое слово!")
     word_key = input()
     logger.info('Транзакции по ключевому слову не найдены')
     list_data = get_searh_to_string(path2, word_key)
logger.info("Сформирован список отфильтрованный по ключевому слову")

'''Формируем JSON-ответ для страницы "Поиск"'''
json_trans = json.dumps(list_data, indent=4, ensure_ascii=False)
logger.info('Сформирован JSON-ответ для страницы "Простой поиск"')
print(json_trans)

"""Запускаем формирование отчёта по расходам для выбранной категории"""

print("Введите название категории. Например, фастфуд")
categor = input()
print("Введите дату окончания выборки. Например, 01.05.2021. Выборка выводится за 3 мес. до выбранной даты!")
end_date = input()

'''Формируем датафрейм для страницы "Отчеты"'''
df_filter = filter_period(df, end_date)
pay_list = spending_by_category(df_filter, categor)
while len(pay_list) == 0:
     print("Таких категорий не найдено. Введите другое слово!")
     category = input()
     logger.info('Категория не найдена')
     pay_list = spending_by_category(df_filter, categor)
logger.info("Сформирован отчёт по расходам в выбранной категории")

'''Формируем JSON-ответ для страницы "Отчёты"'''
json_reports = json.dumps(pay_list, indent=4, ensure_ascii=False)
logger.info('Сформирован JSON-ответ для страницы "Траты по категории"')
print("Траты по выбранной категории")
print(json_reports)
