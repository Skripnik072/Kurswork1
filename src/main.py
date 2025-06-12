import datetime
import json
import logging
from dotenv import load_dotenv
from src.views import hi_time
from src.utils import get_external_xls, filter_for_date, grupp_in_cards, sorted_by_amount
from src.utils import get_user_latest, get_user_stocks
from src.services import get_searh_to_string
from src.reports import filter_period, spending_by_category

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('C:/Users/it-pc.ru/PycharmProjects/PythonProject2/logs/main.log',
                                   encoding='utf-8')
file_formatter = logging.Formatter('%(asctime)s %(filename)s %(levelname)s: %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

'''Формируем код для страницы "Главная"'''
logger.info(f'Формируем код для страницы "Главная"')

'''Загрузка переменных'''
load_dotenv()

'''Формируем приветственную фразу'''
current_date = datetime.datetime.now()
greeting = hi_time()
logger.info(f'Определено привествие"')

'''Создаем датафрейм, отфильтровываем нужные и переименовываем столбцы'''
df = get_external_xls("date\\operations.xlsx")
logger.info(f'Датафрейм создан. Столбцы переименованы')

'''Определяем диапазон дат для анализа'''
current_date = datetime.datetime.now()
date_out = current_date.strftime("2021-%m-%d")
date_begin = current_date.strftime("2021-%m-01")
logger.info(f'Определен диапазон дат для анализа от начала месяца')

'''Отфильтровываем датафрейм по диапазону дат'''
df_filter = filter_for_date(df, date_begin, date_out)
logger.info(f'Датафрейм отфильтрован по выбранному диапазону дат')

'''Сортируем датафрейм по сумме и преобразуем в список словарей'''
list_trans = sorted_by_amount(df_filter)
logger.info(f'Датафрей отсортирован по сумме')
# print(list_trans)

'''Получаем параметры из JSON, курс валют из API и преобразуем в список словарей'''
with open('user_settings.json', 'r') as file:
    data = json.load(file)
    currency = data["user_currencies"]
    symbols = ",".join(currency)
    list_currency =  get_user_latest(symbols)
    logger.info(f'Получены курсы валют из API')

'''Получаем параметры из JSON, котировки акций из API и преобразуем в список словарей'''
with open('user_settings.json', 'r') as file:
    data = json.load(file)
    user_stocks = data["user_stocks"]
    list_stocks = get_user_stocks(user_stocks)
    logger.info(f'Получены курсы акций из API')

'''Группируем по номерам карт и формируем словарь для JSON'''
dict_data = grupp_in_cards(df_filter, list_trans, list_currency, list_stocks)
logger.info(f'Сформирован словарь для JSON-ответа')
# print(dict_data)

'''Формируем JSON-ответ для страницы "Главная"'''
json_data = json.dumps(dict_data, indent=4, ensure_ascii=False)
logger.info(f'Сформирован JSON-ответ для страницы "Главная"')
print(json_data)

'''Формируем список для JSON'''
list_data = get_searh_to_string("date\\operations.xlsx", "супермаркеты")
logger.info(f'Сформирован список отфильтрованный по ключевому слову')

'''Формируем код для страницы "Поиск"'''
json_trans = json.dumps(list_data, indent=4, ensure_ascii=False)
logger.info(f'Сформирован JSON-ответ для страницы "Простой поиск"')
print(json_trans)

'''Формируем датафрейм для страницы "Отчеты"'''
df_filter = filter_period(df, "05.05.2021")
pay_list = spending_by_category(df_filter, "Фастфуд")
logger.info(f'Сформирован отчёт по расходам в выбранной категории')

'''Формируем код для страницы "Отчёты"'''
json_reports = json.dumps(pay_list, indent=4, ensure_ascii=False)
logger.info(f'Сформирован JSON-ответ для страницы "Траты по категории"')
print("Траты по выбранной категории")
print(json_reports)