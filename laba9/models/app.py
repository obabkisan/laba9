"""Модель App для метаинформации о приложении"""


from .author import Author


class App:
    def __init__(self, name: str, version: str, author: Author):
        self.__name: str = name
        self.__version: str = version
        self.__author: Author = author

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, name: str):
        if type(name) is str and len(name.strip()) >= 2:
            self.__name = name.strip()
        else:
            raise ValueError('Ошибка прр задании названия приложения')  # название должно быть строкой от 2 символов

    @property
    def version(self) -> str:
        return self.__version

    @version.setter
    def version(self, version: str):
        if type(version) is str and len(version.strip()) >= 1:
            self.__version = version.strip()
        else:
            raise ValueError('Ошибка при задании версии приложения')  # версия не должна быть пустой строкой

    @property
    def author(self) -> Author:
        return self.__author

    @author.setter
    def author(self, author: Author):
        self.__author = author  # без сложной проверки
