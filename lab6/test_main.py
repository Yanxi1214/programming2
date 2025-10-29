import unittest
from unittest.mock import patch, MagicMock
import sys
import logging
from io import StringIO
from main import get_currencies, setup_logging


class TestCurrencyAPI(unittest.TestCase):
    
    def setUp(self):
        """Настройка перед каждым тестом"""
        self.currency_codes = ['USD', 'EUR']
        self.test_url = "https://www.cbr-xml-daily.ru/daily_json.js"
        self.log_output = StringIO()
    
    def test_successful_response(self):
        """Тест успешного получения курсов валют"""
        mock_response = {
            'Valute': {
                'USD': {'Value': 75.5},
                'EUR': {'Value': 85.2},
                'GBP': {'Value': 95.1}
            }
        }
        
        with patch('main.requests.get') as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = mock_response
            
            result = get_currencies(self.currency_codes)
            
            expected = {'USD': 75.5, 'EUR': 85.2}
            self.assertEqual(result, expected)
    
    def test_currency_not_found(self):
        """Тест обработки отсутствующей валюты"""
        mock_response = {
            'Valute': {
                'USD': {'Value': 75.5}
                # EUR отсутствует
            }
        }
        
        with patch('main.requests.get') as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = mock_response
            
            result = get_currencies(self.currency_codes)
            self.assertIsNone(result)
    
    def test_no_valute_in_response(self):
        """Тест ответа без курсов валют"""
        mock_response = {}  # Нет ключа 'Valute'
        
        with patch('main.requests.get') as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = mock_response
            
            result = get_currencies(self.currency_codes)
            self.assertIsNone(result)
    
    def test_network_error(self):
        """Тест обработки сетевой ошибки"""
        with patch('main.requests.get') as mock_get:
            mock_get.side_effect = Exception("Network error")
            
            result = get_currencies(self.currency_codes)
            self.assertIsNone(result)
    
    def test_empty_currency_codes(self):
        """Тест пустого списка валют"""
        result = get_currencies([])
        self.assertIsNone(result)
    
    def test_case_insensitive_currency_codes(self):
        """Тест нечувствительности к регистру кодов валют"""
        mock_response = {
            'Valute': {
                'USD': {'Value': 75.5},
                'EUR': {'Value': 85.2}
            }
        }
        
        with patch('main.requests.get') as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = mock_response
            
            # Используем коды в нижнем регистре
            result = get_currencies(['usd', 'eur'])
            expected = {'usd': 75.5, 'eur': 85.2}
            self.assertEqual(result, expected)
    
    def test_logging_on_error(self):
        """Тест записи логов при ошибках"""
        logger = setup_logging()
        
        # Перехватываем вывод логов
        with patch('sys.stdout') as mock_stdout:
            with patch('main.requests.get') as mock_get:
                mock_get.side_effect = Exception("Test error")
                
                result = get_currencies(self.currency_codes)
                
                self.assertIsNone(result)
                # Проверяем, что была попытка записи в stdout
                self.assertTrue(mock_stdout.write.called)


if __name__ == '__main__':
    # Запуск тестов с более подробным выводом
    runner = unittest.TextTestRunner(verbosity=2)
    unittest.main(testRunner=runner)
