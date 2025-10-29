import requests
import logging
from functools import wraps
import sys


def setup_logging():
    """Настройка логирования"""
    logger = logging.getLogger('currency_api')
    logger.setLevel(logging.ERROR)
    
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    return logger


def log_errors(logger):
    """Декоратор для логирования ошибок"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except (requests.RequestException, KeyError, ValueError) as e:
                logger.error(f"Ошибка в функции {func.__name__}: {str(e)}")
                return None
        return wrapper
    return decorator


# Создаем логгер
currency_logger = setup_logging()


@log_errors(currency_logger)
def get_currencies(currency_codes, url="https://www.cbr-xml-daily.ru/daily_json.js"):
    """
    Получает курсы валют из API ЦБ РФ
    
    Args:
        currency_codes (list): Список кодов валют (например, ['USD', 'EUR'])
        url (str): URL API ЦБ РФ
    
    Returns:
        dict: Словарь с курсами валют или None в случае ошибки
    """
    if not currency_codes:
        raise ValueError("Список кодов валют не может быть пустым")
    
    response = requests.get(url)
    response.raise_for_status()
    
    data = response.json()
    
    if 'Valute' not in data:
        raise KeyError("В ответе API отсутствуют курсы валют")
    
    currencies = {}
    for code in currency_codes:
        code_upper = code.upper()
        if code_upper not in data['Valute']:
            raise KeyError(f"Валюта {code} не найдена в ответе API")
        
        currency_data = data['Valute'][code_upper]
        currencies[code] = currency_data['Value']
    
    return currencies


# Пример использования
if __name__ == "__main__":
    # Тестирование функции
    codes = ['USD', 'EUR', 'GBP']
    result = get_currencies(codes)
    print(f"Курсы валют: {result}")
        
    
