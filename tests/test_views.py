import datetime
import unittest
from unittest.mock import patch

from src.views import hi_time, find_begin_month


class TestViews(unittest.TestCase):
    def test_views_privet(self):
        privet  = datetime.datetime(2023, 1, 1, 12, 0, 0)
        self.assertEqual(hi_time(privet), "Добрый день!")

    def test_views_interval(self):
        result = "15-01-2021 00:00:00"
        self.assertEqual(find_begin_month(result), ("2021-01-01 00:00:00", "15-01-2021 00:00:00"))


if __name__ == '__main__':
    unittest.main()
