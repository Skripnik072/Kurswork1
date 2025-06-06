import datetime
import pandas as pd
from views import set_interval


def get_external_xls(path: str) -> list[dict]:
    '''Функция принимает файл Excel и возвращает датафрейм с переименованными столбцами'''
    my_dict = {}
    my_list = []
    try:
        excel_data = pd.read_excel(path)
#        print(excel_data.head(3)
        df = excel_data.iloc[:, [0,2,5,8,9,11,14]]
        newcols = {'Дата операции': 'date',
                   'Номер карты': 'cards',
                   'Сумма операции с округлением': 'amount',
                   'Валюта операции': 'currency',
                   'Кэшбэк': 'cashback',
                   'Категория': 'category',
                   'Описание': 'description'
                   }
        df.rename(columns=newcols, inplace=True)
    except FileNotFoundError:
        raise FileNotFoundError("Файл не найден")
    return df


def filter_for_date(df: pd.DataFrame, date_begin, date_out) -> pd.DataFrame:
    '''Отфильтровываем датафрейм по диапазону дат и убираем значение NaN'''
    df.date = pd.to_datetime(df.date)
    df_filt_data = df.loc[(df.date >= date_begin) & (df.date <= date_out)]
    df_filter = df_filt_data.loc[df_filt_data.cards.notnull()]
    df_filter['cashback'].fillna(0, inplace=True)
    return df_filter


def grupp_in_cards(df: pd.DataFrame) -> dict:
    '''Группируем транзакции по номерам карт'''
    df_grupp = df.groupby('cards').agg({
        "amount": 'sum',
        "cashback": 'sum'
    })
    dict_cards = df_grupp.reset_index().to_dict(orient='records')

    result = dict()
    for index, item in enumerate(dict_cards):
        mask = get_mask_card_number(item["cards"])
        result[f'cards{index+1}'] = {
            "last_digits": mask, "total_spent": item["amount"], "cashback": item["cashback"]}
    return result

if __name__ == '__main__':
    df = get_external_xls("date\\operations.xlsx")
#    print(df.head(5))
    current_date = datetime.datetime.now()
    date_out = current_date.strftime("2021-%m-%d")
    date_begin = current_date.strftime("2021-%m-01")
    df.date = pd.to_datetime(df.date)
    df_filter = df.loc[(df.date >= date_begin) & (df.date <= date_out)]
    print(date_begin, date_out)
    print(df_filter)


def get_mask_card_number(number_card: str) -> str:
    """Функция возвращает маску номера банковской карты"""
    return str(number_card)[1:]


# print(get_mask_card_number("*3611"))
