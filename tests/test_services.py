import pytest
import pandas as pd
from unittest.mock import patch
from src.services import get_searh_to_string


@pytest.fixture
def pd_Data_Frame():
    df = pd.DataFrame({'id': [650703.0], 'Категория': ['EXECUTED'], 'Описание': ['Перевод организации']})
    return df

@patch("pandas.read_excel")
def test_filter_to_string(mock_xls, pd_Data_Frame):
        mock_xls.return_value = pd_Data_Frame
        assert get_searh_to_string("test_path", "Перевод") == [{'id': 650703.0, 'Категория': 'EXECUTED',
                                                                             'Описание': 'Перевод организации'}]
        mock_xls.assert_called_once_with("test_path")

def test_filter_to_error():
    with pytest.raises(FileNotFoundError, match="Файл не найден"):
        get_searh_to_string('operation.xlsx', "Перевод")