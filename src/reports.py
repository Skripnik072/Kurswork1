import datetime
import pandas as pd
from utils import get_external_xls, filter_for_date


current_date = datetime.datetime.now()
data_end = "06.05.2021"

def time_minus_3_month(data_end: str) -> str:
    '''Функция сдвигает заданное время на 3 месяца назад'''
    stamp = pd.Timestamp(data_end)
    if stamp.month in [1, 2, 3]:
        date_offset = pd.DateOffset(months=+9)
    else:
        date_offset = pd.DateOffset(months=-3)
    new_stamp = stamp + date_offset
    return new_stamp


def filter_period(df: pd.DataFrame, data_end: str) -> pd.DataFrame:
    '''Функция из датафрейма формирует список расходов за период 3 месяца до выбранной даты'''
    '''Определяем диапазон дат для анализа'''

    if data_end:
        data_out = data_end
    else:
        data_out = current_date

    data_begin = time_minus_3_month(data_end)
    df.date = pd.to_datetime(df.date)
    df_filtr = df.loc[(df.date >= data_begin) & (df.date <= data_out)]
    return df_filtr


def spending_by_category(df_filter: pd.DataFrame, category: str ) -> pd.DataFrame:
    '''Считаем расходы за период по выбранной категории'''
    df_filtr = df_filter.loc[df_filter.payments < 0]
    df_filter_cat = df_filtr[df_filtr['category'].str.contains(category, case=False, na=False)]
    df_filt = df_filter_cat.groupby('category').agg({'payments': 'sum'})
    return df_filt


if __name__ == "__main__":
    df = get_external_xls("date\\operations.xlsx")
    df_filter = filter_period(df, "05.05.2021")
    df_filtr = spending_by_category(df_filter, "транспорт")
    print(df_filtr)


