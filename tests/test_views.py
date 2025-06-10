import pytest
import datetime
import unittest
from src.views import hi_time, set_interval
from unittest.mock import Mock, patch


class TestViews(unittest.TestCase):
    @patch('datetime.datetime', wraps=datetime.datetime)
    def test_views_privet(self, mock_datetime):
        mock_datetime.now.return_value = datetime.datetime(2023, 1, 1, 12, 0, 0)
        self.assertEqual(hi_time(), "Добрый день!")

    @patch('datetime.datetime', wraps=datetime.datetime)
    def test_views_interval(self, mock_datetime):
        mock_datetime.now.return_value = datetime.datetime(2023, 1, 15, 12, 0, 0)
        self.assertEqual(set_interval(mock_datetime), ("01.01.2021", "15.01.2021"))


if __name__ == '__main__':
    unittest.main()