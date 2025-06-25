import logging
import os

import pandas as pd

path1 = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs', 'services.log')

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(path1, encoding='utf-8')
file_formatter = logging.Formatter('%(asctime)s %(filename)s %(levelname)s: %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def get_searh_to_string(path: str, str_descr: str) -> list[dict]:
    '''Функция принимает файл Excel, возвращает датафрейм и'''
    '''выполняет поиск транзакций по категории или по описанию'''
    my_list = []
    try:
        excel_data = pd.read_excel(path)
        logger.info(f'Файл найден {path}')
        logger.info('Получаем датафрейм из файла Excel')
        '''Выбираем транзакции по строке из Описания или Категории'''
        df = excel_data[excel_data['Описание'].str.contains(str_descr, case=False) |
                        excel_data['Категория'].str.contains(str_descr, case=False)]
#        df['Кэшбек'].fillna(0, inplace=True)
        my_list = df.to_dict(orient='records')
        # while len(my_list) == 0:
        #     print("Нет таких слов в категориях или описании транзакций. Введите другое слово!")
        #
        #     logger.info('Транзакции по ключевому слову не найдены')
        logger.info('Выбраны транзакции по ключевому слову')
    except FileNotFoundError:
        logger.error('Файл не найден')
        raise FileNotFoundError("Файл не найден")
    return my_list


# if __name__ == "__main__":
#    my_list = get_searh_to_string("date\\operations.xlsx", 'Перевод')
#    print(my_list)
