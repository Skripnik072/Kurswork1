import pytest
import pandas as pd
from unittest.mock import Mock, patch
from pandas import Timestamp
from src.reports import time_minus_3_month, filter_period, spending_by_category


@patch('src.reports.time_minus_3_month')
def test_time_minus(mock_timeminus):
    mock_timeminus.return_value = pd.Timestamp('2023-02-06 00:00:00')
    assert str(time_minus_3_month("05.06.2023")) == '2023-02-06 00:00:00'


def test_filter_period(pd_Data_Frame):
    mock_timeminus = Mock(return_value = pd.Timestamp('2023-02-06 00:00:00'))
    time_minus_3_month = mock_timeminus
    assert filter_period(pd_Data_Frame, "05.06.2021") == [{'date': ['01.05.2021 16:44:00'], 'cards': [*7197],
                                                                  'currency': ['RUB'],  'payments': [-460.89 ],
                                                                  'cashback': ['NaN'], 'category': ['Супермаркеты'],
                                                                'description': ['Колхоз'], 'amount': [460.89]}]
    mock_timeminus.assert_called_once_with(pd_Data_Frame, "05.06.2021")



