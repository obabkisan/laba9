"""Модель UserCurrency для связи пользователей с валютами"""


class UserCurrency:
    def __init__(self, id: int, user_id: int, currency_id: int):
        self.__id: int = id
        self.__user_id: int = user_id
        self.__currency_id: int = currency_id

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, id: int):
        if type(id) is int and id > 0:
            self.__id = id
        else:
            raise ValueError('Ошибка при задании ID связи')

    @property
    def user_id(self):
        return self.__user_id

    @user_id.setter
    def user_id(self, user_id: int):
        if type(user_id) is int and user_id > 0:
            self.__user_id = user_id
        else:
            raise ValueError('Ошибка при задании ID пользователя')

    @property
    def currency_id(self):
        return self.__currency_id

    @currency_id.setter
    def currency_id(self, currency_id: int):
        if type(currency_id) is int and currency_id > 0:
            self.__currency_id = currency_id
        else:
            raise ValueError('Ошибка при задании ID валюты')
