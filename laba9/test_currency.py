import unittest
from unittest.mock import MagicMock
from controllers.currencycontroller import CurrencyController


class TestCurrencyController(unittest.TestCase):
    """Тесты для CurrencyController с использованием mock"""

    def test_list_currencies(self):
        mock_db = MagicMock()
        mock_db._read.return_value = [{"id": 1, "char_code": "USD", "value": 90.0}]
        controller = CurrencyController(mock_db)
        result = controller.get_all_currencies()
        self.assertEqual(result[0]["char_code"], "USD")
        mock_db._read.assert_called_once()

    def test_update_currency_value(self):
        mock_db = MagicMock()
        controller = CurrencyController(mock_db)
        controller.update_currency_value("USD", 95.5)
        mock_db._update.assert_called_once_with({"USD": 95.5})

    def test_delete_currency(self):
        mock_db = MagicMock()
        controller = CurrencyController(mock_db)
        controller.delete_currency(1)
        mock_db._delete.assert_called_once_with(1)

    def test_create_currency(self):
        mock_db = MagicMock()
        controller = CurrencyController(mock_db)
        controller.create_currency("123", "ABC", "Test Currency", 100.0, 1)
        expected_data = [{
            'num_code': '123',
            'char_code': 'ABC',
            'name': 'Test Currency',
            'value': 100.0,
            'nominal': 1
        }]
        mock_db._create.assert_called_once_with(expected_data)


if __name__ == '__main__':
    unittest.main()