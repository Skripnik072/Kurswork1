import pandas as pd
import pytest
from datetime import datetime


@pytest.fixture()
def pd_Data_Frame():
    df = pd.DataFrame(
        {
            "date": ["05.05.2021 00:00:00"],
            "cards": ["*7197"],
            "currency": ["RUB"],
            "payments": [-460.89],
            "cashback": ["NaN"],
            "category": ["Супермаркеты"],
            "description": ["Колхоз"],
            "amount": [460.89]
        }
    )
    return df


@pytest.fixture()
def pd_Data_Frame2():
    data1 = datetime.strptime("2021-05-05 00:00:00", '%Y-%m-%d %H:%M:%S')
    data2 = datetime.strptime("2021-05-02 00:00:00", '%Y-%m-%d %H:%M:%S')
    data3 = datetime.strptime("2021-05-01 00:00:00", '%Y-%m-%d %H:%M:%S')
    df = pd.DataFrame(
        [
            {
                "date": data1,
                "cards": ["*7197"],
                "currency": ["RUB"],
                "payments": [-760.89],
                "cashback": ["NaN"],
                "category": ["Супермаркеты"],
                "description": ["Переводы"],
                "amount": [760.89],
            },
            {
                "date": data2,
                "cards": ["*7195"],
                "currency": ["RUB"],
                "payments": [-560.89],
                "cashback": ["NaN"],
                "category": ["Супермаркеты"],
                "description": ["Город"],
                "amount": [560.89],
            },
            {
                "date": data3,
                "cards": ["*6195"],
                "currency": ["RUB"],
                "payments": [-460.89],
                "cashback": ["NaN"],
                "category": ["Супермаркеты"],
                "description": ["Колхоз"],
                "amount": [460.89],
            },
        ]
    )
    return df


@pytest.fixture()
def data2():
    return "2021-02-06 00:00:00"
