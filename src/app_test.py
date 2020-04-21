import logging
import unittest
import sys

import pandas as pd

from unittest.mock import patch, Mock

from app import app, forecast

app.logger = logging.getLogger()
app.logger.level = logging.DEBUG
app.logger.addHandler(logging.StreamHandler(sys.stdout))


@patch('pandas.read_csv')
class TestApp(unittest.TestCase):

    def test_forecast_US(self, read_csv_mock: Mock):
        read_csv_mock.return_value = pd.DataFrame(
            columns=["A", "B", "C", "D", "E", "F", "Province_State", "Country_Region", "I", "J", "Combined_Key", "L",
                     "4/9/20", "4/10/20", "4/11/20", "4/12/20", "4/13/20", "4/14/20", "4/15/20", "4/16/20", "4/17/20",
                     "4/18/20", "4/19/20", "4/20/20"],
            data=[['a', 'b', 'c', 'd', 'e', 'f', 'Test Key', 'US', 'i', 'j', 'Test Key, US', 'l',
                   0, 1, 2, 3, 4, 4, 4, 5, 6,
                   6, 6, 6]],
            index=['Test Key, US'])

        ret = forecast('test_US', 'Test Key, US', 10, 0, 1, 1)
        assert read_csv_mock.called
        self.assertIsNotNone(ret)

        ret2 = forecast('test_US', '', 10, 0, 1, 1)
        self.assertIsNotNone(ret2)

        ret3 = forecast('test_US', 'Nowhere, US', 10, 0, 1, 1)
        self.assertIsNone(ret3)

    def test_forecast_global(self, read_csv_mock: Mock):
        read_csv_mock.return_value = pd.DataFrame(
            columns=["Province_State", "Country_Region", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L",
                     "4/9/20", "4/10/20", "4/11/20", "4/12/20", "4/13/20", "4/14/20", "4/15/20", "4/16/20", "4/17/20",
                     "4/18/20", "4/19/20", "4/20/20"],
            data=[['Test Key', 'US', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
                   0, 1, 2, 3, 4, 4, 4, 5, 6,
                   6, 6, 6]],
            index=[('Test Key', 'US')])

        ret = forecast('test_global', 'Test Key, US', 10, 0, 1, 1)
        assert read_csv_mock.called
        self.assertIsNotNone(ret)


if __name__ == '__main__':
    unittest.main()
