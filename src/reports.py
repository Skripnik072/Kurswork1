import datetime
import pandas as pd
import logging
from src.utils import get_external_xls


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('C:/Users/it-pc.ru/PycharmProjects/PythonProject2/logs/reports.log',
                                   encoding='utf-8')
file_formatter = logging.Formatter('%(asctime)s %(filename)s %(levelname)s: %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

current_date = datetime.datetime.now()
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


def filter_period(df: pd.DataFrame, data_end: str) -> pd.DataFrame:
    '''Функция из датафрейма формирует список расходов за период 3 месяца до выбранной даты'''
    '''Определяем диапазон дат для анализа'''

    if data_end:
        data_out = data_end
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
    for i in pay_list:
        pay_dict = {"Категория": category, "Расходы": i['payments']}
    return pay_dict


# if __name__ == "__main__":
#    date = time_minus_3_month("05.06.2023")
#    print(date)

#    df = get_external_xls("C:/Users/it-pc.ru/PycharmProjects/PythonProject2/date/operations.xlsx")
#    df_filter = filter_period(df, "05.05.2021")
#    pay_list = spending_by_category(df_filter, "супермаркеты")
#    print(pay_list)


