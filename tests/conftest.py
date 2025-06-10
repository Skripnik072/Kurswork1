import pandas as pd
import pytest
import datetime


@pytest.fixture()
def pd_Data_Frame():
    df= pd.DataFrame({'date': ['01.05.2021 16:44:00'], 'cards': [*7197], 'currency': ['RUB'],  'payments': [-460.89 ],
                      'cashback': ['NaN'], 'category': ['Супермаркеты'], 'description': ['Колхоз'],
                      'amount': [460.89]})
    return df
