import pandas as pd
import pandas.testing as pdt
import pytest

from src.utils import filter_for_date, get_external_xls, get_mask_card_numb, grupp_in_cards, sorted_by_amount


def test_error_cod():
    with pytest.raises(FileNotFoundError, match="Файл не найден"):
        get_external_xls("operation.xlsx")


def test_filter_for_date(pd_Data_Frame):
    expected_df = pd.DataFrame(
        {
            "date": ["05.05.2021 00:00:00"],
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
    result_df = filter_for_date(pd_Data_Frame, "2021-05-01 00:00:00", "2021-05-05 00:00:00")
    pdt.assert_frame_equal(result_df, expected_df)


def test_grupp_in_cards(pd_Data_Frame):
    expected_list = [{"last_digits": "7197", "total_spent": 460.89, "cashback": "NaN"}]
    assert grupp_in_cards(pd_Data_Frame) == expected_list


def test_get_mask_card_numb():
    assert get_mask_card_numb("*7197") == "7197"


# def test_format_date(data2):
#     assert format_date("2023-02-06 00:00:00") == "06.02.2023"


def test_sorted_by_amount(pd_Data_Frame2):
    expected_list = [
        {"date": "2021-05-05 00:00:00", "amount": [760.89], "category": ["Супермаркеты"], "description": ["Переводы"]},
        {"date": "2021-05-02 00:00:00", "amount": [560.89], "category": ["Супермаркеты"], "description": ["Город"]},
        {"date": "2021-05-01 00:00:00", "amount": [460.89], "category": ["Супермаркеты"], "description": ["Колхоз"]},
    ]
    assert sorted_by_amount(pd_Data_Frame2) == expected_list
