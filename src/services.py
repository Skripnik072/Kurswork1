import pandas as pd
import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('C:/Users/it-pc.ru/PycharmProjects/PythonProject2/logs/services.log',
                                   encoding='utf-8')
file_formatter = logging.Formatter('%(asctime)s %(filename)s %(levelname)s: %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def get_searh_to_string(path: str, str_descr: str) -> list[dict]:
    '''Функция принимает файл Excel, возвращает датафрейм и'''
    '''выполняет поиск транзакций по категории или по описанию'''
    my_list = []
    try:
        excel_data = pd.read_excel(path)
        logger.info(f'Файо найден {path}')
        logger.info(f'Получаем датафрейм из файла Excel')
        '''Выбираем транзакции по строке из Описания или Категории'''
        df = excel_data[excel_data['Описание'].str.contains(str_descr, case=False) |
                        excel_data['Категория'].str.contains(str_descr, case=False)]
#        df['Кэшбек'].fillna(0, inplace=True)
        my_list = df.to_dict(orient='records')
        logger.info(f'Выбраны транзакции по ключевому слову')
    except FileNotFoundError:
        logger.error(f'Файл не найден')
        raise FileNotFoundError("Файл не найден")
    return my_list


# if __name__ == "__main__":
#    my_list = get_searh_to_string("date\\operations.xlsx", 'Перевод')
#    print(my_list)
