"""
Контроллер для бизнес-логики валют.
Отделяет бизнес-логику от работы с БД.
"""

from .databasecontroller import CurrencyRatesCRUD


class CurrencyController:
    """Контроллер бизнес-логики для работы с валютами"""

    def __init__(self, db_controller: CurrencyRatesCRUD):
        self.db = db_controller

    def get_all_currencies(self):
        """Получение всех валют"""
        return self.db._read()

    def get_currency_by_id(self, currency_id: int):
        """Получение валюты по ID"""
        result = self.db._read(currency_id=currency_id)
        return result[0] if result else None

    def get_currency_by_code(self, char_code: str):
        """Получение валюты по символьному коду"""
        result = self.db._read(char_code=char_code.upper())
        return result[0] if result else None

    def update_currency_value(self, char_code: str, value: float):
        """Обновление курса валюты с проверкой бизнес-правил"""
        if value <= 0:
            raise ValueError("Курс валюты должен быть положительным числом")

        # Можно добавить другие бизнес-правила
        if len(char_code) != 3:
            raise ValueError("Код валюты должен состоять из 3 символов")

        return self.db._update({char_code.upper(): value})

    def delete_currency(self, currency_id: int):
        """Удаление валюты"""
        return self.db._delete(currency_id)

    def create_currency(self, num_code: str, char_code: str,
                        name: str, value: float, nominal: int):
        """Создание новой валюты с валидацией"""
        # Бизнес-правила валидации
        if len(num_code) != 3:
            raise ValueError("Цифровой код должен состоять из 3 символов")

        if len(char_code) != 3:
            raise ValueError("Символьный код должен состоять из 3 символов")

        if value <= 0:
            raise ValueError("Курс валюты должен быть положительным")

        if nominal <= 0:
            raise ValueError("Номинал должен быть положительным числом")

        # Создаем данные для БД
        data = [{
            'num_code': num_code,
            'char_code': char_code.upper(),
            'name': name,
            'value': value,
            'nominal': nominal
        }]

        return self.db._create(data)

    def format_currency_for_display(self, currency):
        """Форматирование валюты для отображения (бизнес-логика)"""
        if currency:
            return {
                'id': currency.get('id'),
                'code': currency.get('char_code'),
                'name': currency.get('name'),
                'value': f"{currency.get('value', 0):.2f}",
                'nominal': currency.get('nominal', 1)
            }
        return None