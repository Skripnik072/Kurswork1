import datetime
import json
from views import hi_time
from utils import get_external_xls, filter_for_date, grupp_in_cards


'''Формируем приветственную фразу'''
current_date = datetime.datetime.now()
greeting = hi_time(current_date)
print(greeting)

'''Создаем датафреймб отфильтровываем нужные и переименовываем столбцы'''
df = get_external_xls("date\\operations.xlsx")

'''Определяем диапазон дат для анализа'''
current_date = datetime.datetime.now()
date_out = current_date.strftime("2021-%m-%d")
date_begin = current_date.strftime("2021-%m-01")

'''Отфильтровываем датафрейм по диапазону дат'''
df_filter = filter_for_date(df, date_begin, date_out)

'''Создаем словарь и группируем по номерам карт'''
dict_data = grupp_in_cards(df_filter)
# print(dict_data)

'''Формируем JSON-ответ'''
json_data = json.dumps(dict_data, indent=4)
print(json_data)
