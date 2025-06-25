import tempfile
from unittest.mock import MagicMock, patch
import os
import pandas as pd
from src.utils import get_external_xls, get_user_latest, get_user_stocks

def test_get_external_xls():
    data = {
'Дата операции': ['2024-01-01'],
        '1': [1],
        'Номер карты': ['1234'],
        '3': [3],
        '4': [4],

        'Сумма операции с округлением': [100],
        'Валюта операции': ['RUB'],
'7':[7],
        'Сумма платежа': [90],
        'Кэшбэк': [10],
'10':[10],
        'Категория': ['Еда'],
'12':[12],
'13' :[13],
        'Описание': ['Покупка'],
    }
    df = pd.DataFrame(data)
    with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp:
        df.to_excel(tmp.name, index=False)
        tmp_path = tmp.name

    result = get_external_xls(tmp_path)
    assert list(result.columns) == ['date', 'cards', 'amount', 'currency', 'payments', 'cashback', 'category', 'description']
    assert result.shape[0] == 1
    assert result['date'][0] == '2024-01-01'

    os.remove(tmp_path)


# @patch("pandas.read_excel")
# def test_get_external_xls(mock_xls, pd_Data_Frame):
#      mock_xls.return_value = pd_Data_Frame
#
#      assert get_external_xls("test_path") == [
#          {
#              "date": ["01.05.2021 16:44:00"],
#              "cards": ["*7197"],
#              "currency": ["RUB"],
#              "payments": [-460.89],
#              "cashback": ["NaN"],
#              "category": ["Супермаркеты"],
#              "description": ["Колхоз"],
#              "amount": [460.89],
#          }
#      ]
#      mock_xls.assert_called()


@patch("requests.get")
def test_get_user_latest(mock_request_get):
    # Создаем mock-ответ
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {'rates': {'USD': 0.012743}}
    # Пример корректного ответа API
    mock_request_get.return_value = mock_response
    # Проверяем, что функция возвращает то, что вернул бы response.json()
    assert get_user_latest("USD") == [{"currency": "USD", "rate": 0.012743}]
    # Проверяем, что requests.get был вызван с правильными параметрами
    mock_request_get.assert_called_once()


@patch("requests.get")
def test_get_user_latest_cod400(mock_request_get):
    status_code = 400
    text = "error"
    mock_request_get.return_value.status_code = status_code
    mock_request_get.return_value.text = text
    assert get_user_latest("USD") == \
        f"Ошибка при обращении к API {status_code} - {text}"


@patch("requests.get")
def test_get_user_stocks(mock_request_get):
    # Создаем mock-ответ
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {'Global Quote': {"01. symbol": "AAPL", "05. price": 152.12}}
    # Пример корректного ответа API
    mock_request_get.return_value = mock_response
    # Проверяем, что функция возвращает то, что вернул бы response.json()
    assert get_user_stocks(["AAPL"]) == [{"stock": "AAPL", "price": 152.12}]
    # Проверяем, что requests.get был вызван с правильными параметрами
    mock_request_get.assert_called_once()


@patch("requests.get")
def test_get_user_stocks_cod400(mock_request_get):
    status_code = 400
    text = "error"
    mock_request_get.return_value.status_code = status_code
    mock_request_get.return_value.text = text
    assert get_user_stocks(["AAPL"]) == \
        f"Ошибка при обращении к API {status_code} - {text}"
