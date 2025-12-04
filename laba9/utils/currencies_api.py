def get_currencies(currency_list=None):
    """
    Получает курсы валют.

    args:
        currency_list: список кодов валют, например ['USD', 'EUR']
                      если None, возвращаем все доступные валюты

    returns:
        словарь {код_валюты: значение_курса}
        пример: {'USD': '92,50', 'EUR': '99,80'}
    """

    # тестовые данные
    currencies_data = {
        'USD': '92,50',  # доллар США
        'EUR': '99,80',  # евро
        'GBP': '115,20',  # фунт стерлингов
        'CNY': '12,80',  # китайский юань
        'JPY': '0,62',  # японская йена (за 100 йен)
        'CHF': '105,30',  # швейцарский франк
        'TRY': '2,85',  # турецкая лира
        'KZT': '0,20'  # казахстанский тенге (за 100 тенге)
    }

    # если передали список конкретных валют
    if currency_list:
        result = {}
        for code in currency_list:
            if code in currencies_data:
                result[code] = currencies_data[code]
        return result

    # если не передали список - возвращаем все
    return currencies_data