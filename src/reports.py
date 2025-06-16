import datetime
from datetime import datetime
import pandas as pd
import logging
import os
from src.utils import get_external_xls


path1 = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs', 'reports.log')
path2 =  os.path.join(os.path.dirname(os.path.dirname(__file__)), 'date', 'operations.xlsx')

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(path1, encoding='utf-8')
file_formatter = logging.Formatter('%(asctime)s %(filename)s %(levelname)s: %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

current_date = datetime.now()
data_end = "06.05.2021"
logger.info(f'Выбрана дата окончания трехмесячного диапазона')

def time_minus_3_month(data_end: str) -> str:
    '''Функция сдвигает заданное время на 3 месяца назад'''
    stamp = pd.Timestamp(data_end)
    if stamp.month in [1, 2, 3]:
        date_offset = pd.DateOffset(months=+9)
    else:
        date_offset = pd.DateOffset(months=-3)
    new_stamp = stamp + date_offset
    logger.info(f'Диапазон дат для выборки определен')
    return new_stamp


def filter_period(df: pd.DataFrame, data_end: str=current_date) -> pd.DataFrame:
    '''Функция из датафрейма формирует список расходов за период 3 месяца до выбранной даты'''
    '''Определяем диапазон дат для анализа'''

    if data_end:
        data_out = datetime.strptime(data_end, "%d.%m.%Y")
    else:
        data_out = current_date
    data_begin = time_minus_3_month(data_end)
    logger.info(f'Даты для выборки {data_begin} - {data_out}')

    '''Отфильтровываем датафрейм по диапазону дат'''
    df.date = pd.to_datetime(df.date)
    df_filtr = df.loc[(df.date >= data_begin) & (df.date <= data_out)]
    logger.info(f'Датафрейм по диапазону дат отфильтрован')
    return df_filtr


def spending_by_category(df_filter: pd.DataFrame, category: str ) -> pd.DataFrame:
    '''Считаем расходы за период по выбранной категории'''
    df_filtr = df_filter.loc[df_filter.payments < 0]
    df_filter_cat = df_filtr[df_filtr['category'].str.contains(category, case=False, na=False)]
    df_filt = df_filter_cat.groupby('category').agg({'payments': 'sum'})
    logger.info(f'Расходы по выбранной категории подсчитаны')
    pay_list = df_filt.to_dict(orient='records')
    pay_dict = {}
    my_list = []
    for i in pay_list:
        pay_dict = {"Категория": [category], "Расходы": [i['payments']]}
        my_list.append(pay_dict)
    return my_list


if __name__ == "__main__":
    df = get_external_xls(path2)
    df_filter = filter_period(df, "05.05.2021")
    pay_list = spending_by_category(df_filter, "супермаркеты")
    print(pay_list)

#     print(df_filtr)


#    date = time_minus_3_month("05.06.2023")


