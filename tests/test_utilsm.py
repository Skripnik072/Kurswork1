from unittest.mock import patch, Mock, MagicMock
from src.utils import get_external_xls, get_user_latest, get_user_stocks


@patch("pandas.read_excel")
def test_get_external_xls(mock_xls, pd_Data_Frame):
    mock_xls = Mock()
    mock_xls.return_value = pd_Data_Frame
    assert get_external_xls("test_path") == [
        {
            "date": ["01.05.2021 16:44:00"],
            "cards": ["*7197"],
            "currency": ["RUB"],
            "payments": [-460.89],
            "cashback": ["NaN"],
            "category": ["Супермаркеты"],
            "description": ["Колхоз"],
            "amount": [460.89],
        }
    ]
    mock_xls.assert_called_once_with("test_path")


@patch("requests.get")
def test_get_user_latest(mock_request_get):
    # Создаем mock-ответ
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [{"currency": "USD", "rate": 89.0}]
    # Пример корректного ответа API
    mock_request_get.return_value = mock_response
    # Проверяем, что функция возвращает то, что вернул бы response.json()
    assert get_user_latest("USD") == [{"currency": "USD", "rate": 89.0}]
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
    mock_response.json.return_value = [{"stock": "AAPL", "price": 152.12}]
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