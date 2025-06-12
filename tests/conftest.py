import pandas as pd
import pytest


@pytest.fixture()
def pd_Data_Frame():
    df = pd.DataFrame(
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
    return df

@pytest.fixture()
def pd_Data_Frame2():
    df = pd.DataFrame(
        [
            {
                "date": ["01.05.2021 16:44:00"],
                "cards": ["*7197"],
                "currency": ["RUB"],
                "payments": [-460.89],
                "cashback": ["NaN"],
                "category": ["Супермаркеты"],
                "description": ["Колхоз"],
                "amount": [460.89],
            },
            {
                "date": ["02.05.2021 16:44:00"],
                "cards": ["*7195"],
                "currency": ["RUB"],
                "payments": [-560.89],
                "cashback": ["NaN"],
                "category": ["Супермаркеты"],
                "description": ["Город"],
                "amount": [560.89],
            },
            {
                "date": ["05.05.2021 16:44:00"],
                "cards": ["*6195"],
                "currency": ["RUB"],
                "payments": [-760.89],
                "cashback": ["NaN"],
                "category": ["Супермаркеты"],
                "description": ["Переводы"],
                "amount": [760.89],
            },
        ]
    )
    return df

@pytest.fixture()
def data2():
    return "2023-02-06 00:00:00"