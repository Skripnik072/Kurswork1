import datetime
import json
from dotenv import load_dotenv
from views import hi_time
from utils import get_external_xls, filter_for_date, grupp_in_cards, sorted_by_amount
from utils import get_user_latest, get_user_stocks
from services import get_searh_to_string


'''Формируем код для страницы "Главная"'''

'''Загрузка переменных'''
load_dotenv()

'''Формируем приветственную фразу'''
current_date = datetime.datetime.now()
greeting = hi_time(current_date)
print(greeting)

'''Создаем датафрейм, отфильтровываем нужные и переименовываем столбцы'''
df = get_external_xls("date\\operations.xlsx")

'''Определяем диапазон дат для анализа'''
current_date = datetime.datetime.now()
date_out = current_date.strftime("2021-%m-%d")
date_begin = current_date.strftime("2021-%m-01")

'''Отфильтровываем датафрейм по диапазону дат'''
df_filter = filter_for_date(df, date_begin, date_out)

'''Сортируем датафрейм по сумме и преобразуем в список словарей'''
list_trans = sorted_by_amount(df_filter)
# print(list_trans)

'''Получаем параметры из JSON, курс валют из API и преобразуем в список словарей'''
with open('user_settings.json', 'r') as file:
    data = json.load(file)
    currency = data["user_currencies"]
    symbols = ",".join(currency)
#    list_currency =  get_user_latest(symbols)

'''Получаем параметры из JSON, котировки акций из API и преобразуем в список словарей'''
with open('user_settings.json', 'r') as file:
    data = json.load(file)
    user_stocks = data["user_stocks"]
#    list_stocks = get_user_stocks(user_stocks)

'''Группируем по номерам карт и формируем словарь для JSON'''
#dict_data = grupp_in_cards(df_filter, list_trans, list_currency, list_stocks)
# print(dict_data)

'''Формируем JSON-ответ для страницы "Главная"'''
#json_data = json.dumps(dict_data, indent=4, ensure_ascii=False)
# print(json_data)

'''Формируем список для JSON'''
list_data = get_searh_to_string("date\\operations.xlsx", "супермаркеты")

'''Формируем код для страницы "Поиск"'''
json_trans = json.dumps(list_data, indent=4, ensure_ascii=False)
print(json_trans)

