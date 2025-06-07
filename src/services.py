import json
import re
import pandas as pd


def get_searh_to_string(path: str, str_descr: str) -> list[dict]:
    '''Функция принимает файл Excel, возвращает датафрейм и'''
    '''выполняет поиск транзакций по категории или по описанию'''
    my_list = []
    try:
        excel_data = pd.read_excel(path)
        '''Выбираем транзакции по строке из Описания или Категории'''
        df = excel_data[excel_data['Описание'].str.contains(str_descr, case=False) |
                        excel_data['Категория'].str.contains(str_descr, case=False)]
#        df['Кэшбек'].fillna(0, inplace=True)
        my_list = df.to_dict(orient='records')
    except FileNotFoundError:
        raise FileNotFoundError("Файл не найден")
    return my_list


# if __name__ == "__main__":
#    my_list = get_searh_to_string("date\\operations.xlsx", 'Перевод')
#    print(my_list)
