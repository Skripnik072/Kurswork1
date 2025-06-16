import datetime
import logging
import os


path1 = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs', 'views.log')

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(path1, encoding='utf-8')
file_formatter = logging.Formatter('%(asctime)s %(filename)s %(levelname)s: %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def hi_time() -> str:
    '''Определяем вид приветствия по времени'''
    current_date = datetime.datetime.now()
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


def set_interval(current_date: str) -> str:
    '''Определяем диапазон дат для анализа'''
    logger.info(f'Определяем диапазон дат для анализа')
    current_date = datetime.datetime.now()
    date_out = current_date.strftime("%d.%m.2021")
    date_begin = current_date.strftime("01.%m.2021")
    logger.info(f'Диапазон дат определен {date_begin} - {date_out}')
    return date_begin, date_out

# if __name__ == "__main__":
#    privet = hi_time()
#    print(privet)
#    print(path1)
#    print(path2)
#    print(joined_path)