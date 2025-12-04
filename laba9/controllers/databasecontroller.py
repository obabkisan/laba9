import sqlite3


class CurrencyRatesCRUD:
    """Контроллер для CRUD операций с БД SQLite"""

    def __init__(self):
        self.__con = sqlite3.connect(':memory:')
        self.__createtable()
        self.__cursor = self.__con.cursor()
        self.__seed_data()

    def __createtable(self):
        """Создание таблиц с первичными и внешними ключами"""
        # PRIMARY KEY - уникальный идентификатор записи
        # FOREIGN KEY - ссылка на запись в другой таблице
        self.__con.execute(
            "CREATE TABLE IF NOT EXISTS currency("
            "id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "num_code TEXT NOT NULL, "
            "char_code TEXT NOT NULL UNIQUE, "
            "name TEXT NOT NULL, "
            "value FLOAT, "
            "nominal INTEGER);")

        self.__con.execute(
            "CREATE TABLE IF NOT EXISTS user("
            "id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "name TEXT NOT NULL);")

        self.__con.execute(
            "CREATE TABLE IF NOT EXISTS user_currency("
            "id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "user_id INTEGER NOT NULL, "
            "currency_id INTEGER NOT NULL, "
            "FOREIGN KEY(user_id) REFERENCES user(id), "
            "FOREIGN KEY(currency_id) REFERENCES currency(id));")

        self.__con.commit()

    def __seed_data(self):
        """Начальное заполнение БД тестовыми данными"""
        # Валюты
        data = [
            {"num_code": "840", "char_code": "USD", "name": "Доллар США", "value": 90.0, "nominal": 1},
            {"num_code": "978", "char_code": "EUR", "name": "Евро", "value": 91.0, "nominal": 1},
            {"num_code": "826", "char_code": "GBP", "name": "Фунт стерлингов", "value": 105.0, "nominal": 1}
        ]

        sql = """INSERT OR IGNORE INTO currency 
                 (num_code, char_code, name, value, nominal) 
                 VALUES(:num_code, :char_code, :name, :value, :nominal)"""
        self.__cursor.executemany(sql, data)

        # Пользователи
        users = [{"name": "Иван"}, {"name": "Мария"}, {"name": "Алексей"}]
        self.__cursor.executemany("INSERT OR IGNORE INTO user(name) VALUES(:name)", users)

        # Подписки
        subscriptions = [
            {"user_id": 1, "currency_id": 1},
            {"user_id": 1, "currency_id": 2},
            {"user_id": 2, "currency_id": 2},
            {"user_id": 3, "currency_id": 1}
        ]
        self.__cursor.executemany(
            "INSERT OR IGNORE INTO user_currency(user_id, currency_id) VALUES(:user_id, :currency_id)",
            subscriptions
        )

        self.__con.commit()

    # CRUD операции (только работа с БД, без бизнес-логики)
    def _create(self, data):
        """Create - добавление записей в БД"""
        sql = """INSERT INTO currency 
                 (num_code, char_code, name, value, nominal) 
                 VALUES(:num_code, :char_code, :name, :value, :nominal)"""
        self.__cursor.executemany(sql, data)
        self.__con.commit()

    def _read(self, currency_id=None, char_code=None):
        """Read - чтение записей из БД с параметризованными запросами"""
        if currency_id:
            sql = "SELECT * FROM currency WHERE id = ?"
            self.__cursor.execute(sql, (currency_id,))
        elif char_code:
            sql = "SELECT * FROM currency WHERE char_code = ?"
            self.__cursor.execute(sql, (char_code,))
        else:
            sql = "SELECT * FROM currency ORDER BY char_code"
            self.__cursor.execute(sql)

        result_data = []
        for _row in self.__cursor.fetchall():
            _d = {
                'id': int(_row[0]),
                'num_code': _row[1],
                'char_code': _row[2],
                'name': _row[3],
                'value': float(_row[4]),
                'nominal': int(_row[5])
            }
            result_data.append(_d)
        return result_data

    def _update(self, currency: dict):
        """Update - обновление записи в БД с параметризованным запросом"""
        currency_code = tuple(currency.keys())[0]
        currency_value = tuple(currency.values())[0]
        sql = "UPDATE currency SET value = ? WHERE char_code = ?"
        self.__cursor.execute(sql, (currency_value, currency_code))
        self.__con.commit()

    def _delete(self, currency_id: int):
        """Delete - удаление записи из БД с параметризованным запросом"""
        sql = "DELETE FROM currency WHERE id = ?"
        self.__cursor.execute(sql, (currency_id,))
        self.__con.commit()

    def _read_users(self, user_id=None):
        """Чтение пользователей из БД"""
        if user_id:
            sql = "SELECT * FROM user WHERE id = ?"
            self.__cursor.execute(sql, (user_id,))
        else:
            sql = "SELECT * FROM user ORDER BY id"
            self.__cursor.execute(sql)

        result_data = []
        for _row in self.__cursor.fetchall():
            _d = {'id': int(_row[0]), 'name': _row[1]}
            result_data.append(_d)
        return result_data

    def _read_user_currencies(self, user_id):
        """Чтение валют пользователя из БД (JOIN запрос)"""
        sql = '''
            SELECT c.* FROM currency c
            JOIN user_currency uc ON c.id = uc.currency_id
            WHERE uc.user_id = ?
        '''
        self.__cursor.execute(sql, (user_id,))

        result_data = []
        for _row in self.__cursor.fetchall():
            _d = {
                'id': int(_row[0]),
                'num_code': _row[1],
                'char_code': _row[2],
                'name': _row[3],
                'value': float(_row[4]),
                'nominal': int(_row[5])
            }
            result_data.append(_d)
        return result_data

    def __del__(self):
        """Деструктор - закрытие соединения с БД"""
        if hasattr(self, '__cursor'):
            self.__cursor = None
        if hasattr(self, '__con'):
            self.__con.close()