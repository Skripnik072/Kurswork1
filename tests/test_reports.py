import pytest
import pandas as pd
import pandas.testing as pdt
import datetime
from src.reports import time_minus_3_month, filter_period, spending_by_category


def test_time_minus():
    stamp = pd.Timestamp("2023-02-06 00:00:00")
    assert time_minus_3_month("05.06.2023") == stamp


def test_filter_period(pd_Data_Frame):
    expected_df = pd.DataFrame(
        {
            "date": ["05.05.2021 16:44:00"],
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
    result_df = filter_period(pd_Data_Frame, "05.05.2021")
    pdt.assert_frame_equal(result_df, expected_df)


def test_spending_by_category(pd_Data_Frame):
    expected_df = pd.DataFrame([{"category": ["Супермаркеты"], "payments": [-38772.45]}])
    result_df = spending_by_category(pd_Data_Frame,"Супермаркеты")
    pdt.assert_frame_equal(result_df, expected_df)

