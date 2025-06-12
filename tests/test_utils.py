import pytest
import pandas as pd
import pandas.testing as pdt
from src.main import date_begin
from src.utils import get_external_xls, get_user_latest, get_user_stocks
from src.utils import filter_for_date, grupp_in_cards, get_mask_card_numb
from src.utils import format_date, sorted_by_amount
from tests.conftest import pd_Data_Frame


def test_error_cod():
    with pytest.raises(FileNotFoundError, match="Файл не найден"):
        get_external_xls("operations.xlsx")


def test_filter_for_date(pd_Data_Frame):
    expected_df = pd.DataFrame(
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
    )
    expected_df["date"] = pd.to_datetime(expected_df["date"])
    pd_Data_Frame.date = pd.to_datetime(pd_Data_Frame.date)
    result_df = filter_for_date(pd_Data_Frame, "01.05.2021", "05.05.2021")
    pdt.assert_frame_equal(result_df, expected_df)


def test_grupp_in_cards(pd_Data_Frame):
    expected_dict = {
        "greeting": ["Добрый день!"],
        "cards": [{"7197": [{"total_spent": [920], "cashback": [0]}]}],
        "top_transactions": [],
        "currency_rates": [],
        "stock_prices": [],
    }
    assert grupp_in_cards(pd_Data_Frame, [], [], []) == expected_dict


def test_get_mask_card_numb():
    assert get_mask_card_numb("*7197") == "7197"


def test_format_date(data2):
    assert format_date("2023-02-06 00:00:00") == "06.02.2023"


def test_sorted_by_amount(pd_Data_Frame2):
    expected_list = [
        {"date": ["05.05.2021"], "amount": [760.89], "category": ["Супермаркеты"], "description": ["Переводы"]},
        {"date": ["02.05.2021"], "amount": [560.89], "category": ["Супермаркеты"], "description": ["Город"]},
        {"date": ["01.05.2021"], "amount": [460.89], "category": ["Супермаркеты"], "description": ["Колхоз"]},
    ]
    assert sorted_by_amount(pd_Data_Frame2) == expected_list
