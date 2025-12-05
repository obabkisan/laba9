"""Модель User для представления пользователя системы"""


class User:
    def __init__(self, id: int, name: str):
        self.__id: int = id
        self.__name: str = name

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, id: int):
        if type(id) is int and id > 0:
            self.__id = id
        else:
            raise ValueError('Ошибка при задании ID пользователя')

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name: str):
        if type(name) is str and len(name) >= 2:
            self.__name = name
        else:
            raise ValueError('Ошибка при задании имени пользователя')
