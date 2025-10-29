import requests


def get_currencies(currency_codes, url="https://www.cbr-xml-daily.ru/daily_json.js"):
    """
    Получает курсы валют из API Центробанка России.
    
    Args:
        currency_codes (list): Список кодов валют (например, ['USD', 'EUR'])
        url (str): URL API (по умолчанию API ЦБ РФ)
    
    Returns:
        dict: Словарь с кодами валют и их курсами
        None: В случае ошибки запроса
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        data = response.json()
        currencies_data = data.get('Valute', {})
        
        result = {}
        for code in currency_codes:
            if code in currencies_data:
                currency_info = currencies_data[code]
                result[code] = currency_info.get('Value', 0)
        
        return result
        
    except (requests.RequestException, ValueError, KeyError):
        return None


if __name__ == "__main__":
    # Пример использования
    codes = ['USD', 'EUR', 'GBP', 'CNY']
    currencies = get_currencies(codes)
    
    if currencies:
        print("Курсы валют:")
        for code, rate in currencies.items():
            print(f"{code}: {rate:.2f} руб.")
    else:
        print("Ошибка при получении данных)
