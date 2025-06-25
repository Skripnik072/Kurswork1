from datetime import datetime
import logging
import os
import pandas as pd


path1 = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs', 'views.log')

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(path1, encoding='utf-8')
file_formatter = logging.Formatter('%(asctime)s %(filename)s %(levelname)s: %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def hi_time(current_date = None) -> str:
    '''Определяем вид приветствия по времени'''
    if current_date is None:
        current_date = datetime.now()
    hour = current_date.hour
    if 6 < hour < 10:
        text = "Доброе утро!"
    elif 10 < hour < 16:
        text = "Добрый день!"
    elif 16 < hour < 22:
        text = "Добрый вечер!"
    else:
        text = "Доброй ночи!"
    logger.info(f'Определен тип приветствия -  {text}')
    return text


# print("Нужно ввести дату окончания выборки транзакций в формате YYYY-MM-DD HH:MM:SS")
# print("Выборка будет сделана от начала текущего месяца до указанной даты")
# print("Если дата не введена - диапазон будет определяться от текущей даты")
# print("Будете вводить дату? Да/Нет")
# choice = input()
# while choice not in ["Да", "да", "Нет", "нет"]:
#     print("Некорректный термин. Введите заново")
#     choice = input()
# if choice in ["Нет", "нет"]:
#     data_time = datetime.now()
#     data_out = data_time.strftime("%Y-%m-%d %H:%M:%S")
#
# else:
#     print("Введите дату в формате YYYY-MM-DD HH:MM:SS")
#     data_out = input()


def find_begin_month(data_out: str) -> str:
    '''Функция задает диапазон от начала месяца до выбранной даты'''
    dt = pd.Timestamp(data_out)
    date_begin = dt.replace(day=1)
    date_begin = date_begin.strftime("%Y-%m-%d %H:%M:%S")
    logger.info('Диапазон дат для выборки определен')
    return date_begin, data_out


# def set_interval(current_date: str) -> str:
#     '''Определяем диапазон дат для анализа'''
#     logger.info('Определяем диапазон дат для анализа')
#     current_date = datetime.datetime.now()
#     date_out = current_date.strftime("%d.%m.2021 00:00:00")
#     date_begin = current_date.strftime("01.%m.2021 00:00:00")
#     logger.info(f'Диапазон дат определен {date_begin} - {date_out}')
#     return date_begin, date_out

if __name__ == "__main__":
    privet = hi_time()
    print(privet)
    result = find_begin_month()

    print(result)
#    print(path2)
#    print(joined_path)
