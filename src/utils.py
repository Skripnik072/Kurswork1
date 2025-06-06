import datetime
import pandas as pd
from views import hi_time

'''Формируем приветственную фразу'''
current_date = datetime.datetime.now()
greeting = hi_time(current_date)

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


def grupp_in_cards(df: pd.DataFrame, trans_list: list[dict]) -> dict:
    '''Группируем транзакции по номерам карт'''
    df_grupp = df.groupby('cards').agg({
        "amount": 'sum',
        "cashback": 'sum'
    })
    list_cards = df_grupp.reset_index().to_dict(orient='records')
    card_list = []
    resul = {}

    for i in list_cards:
        mask = get_mask_card_number(i["cards"])
        resul = {
                "last_digits": mask, "total_spent": i["amount"], "cashback": i["cashback"]}
        card_list.append(resul)
    result = {
        "greeting": greeting, "cards": card_list, "top_transactions": trans_list, "currency_rates": [], "stock_prices": []
    }
    return result


def get_mask_card_number(number_card: str) -> str:
    """Функция возвращает маску номера банковской карты"""
    return str(number_card)[1:]


def format_date(date: str) -> str:
    '''Изменяем формат даты'''
    date_now = date.strftime("%d.%m.%Y")
    return date_now



def sorted_by_amount(df: pd.DataFrame) -> list:
    '''Сортируем датафрейм по сумме'''
    df_amount = df.sort_values(by='amount', ascending=False)
    trans_list = []
    resul = {}
    list_tr = df_amount.head(5).to_dict(orient='records')
    for i in list_tr:
        resul = {
                "date": format_date(i["date"]), "amount": i["amount"], "category": i["category"],
                "description": i["description"]
        }
        trans_list.append(resul)
    return trans_list


#    "date": "21.12.2021",
#    "amount": 1198.23,
#    "category": "Переводы",
#    "description": "Перевод Кредитная карта. ТП 10.2 RUR"

    return list_tr

#if __name__ == '__main__':
#    df = get_external_xls("date\\operations.xlsx")
#    print(df.head(5))

# print(get_mask_card_number("*3611"))
