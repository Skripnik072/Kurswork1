import datetime


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
    return text


def set_interval(current_date: str) -> str:
    '''Определяем диапазон дат для анализа'''
    current_date = datetime.datetime.now()
    date_out = current_date.strftime("%d.%m.2021")
    date_begin = current_date.strftime("01.%m.2021")
    return date_begin, date_out

if __name__ == "__main__":
    privet = hi_time()
    print(privet)