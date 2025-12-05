"""Модель Currency для представления валюты с курсом"""


class Currency:
    def __init__(self, id: int, num_code: str, char_code: str,
                 name: str, value: float, nominal: int):
        self.__id = id
        self.__num_code = num_code
        self.__char_code = char_code
        self.__name = name
        self.__value = value
        self.__nominal = nominal

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        if type(value) is int and value > 0:
            self.__id = value
        else:
            raise ValueError('Ошибка при задании ID валюты')

    @property
    def num_code(self):
        return self.__num_code

    @num_code.setter
    def num_code(self, value):
        if type(value) is str and len(value) == 3:
            self.__num_code = value
        else:
            raise ValueError('Ошибка при задании цифрового кода валюты')

    @property
    def char_code(self):
        return self.__char_code

    @char_code.setter
    def char_code(self, value):
        if type(value) is str and len(value) == 3:
            self.__char_code = value
        else:
            raise ValueError('Ошибка при задании символьного кода валюты')

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if type(value) is str and len(value) >= 2:
            self.__name = value
        else:
            raise ValueError('Ошибка при задании названия валюты')

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if type(value) in (int, float) and value > 0:
            self.__value = value
        else:
            raise ValueError('Ошибка при задании курса валюты')

    @property
    def nominal(self):
        return self.__nominal

    @nominal.setter
    def nominal(self, value):
        if type(value) is int and value > 0:
            self.__nominal = value
        else:
            raise ValueError('Ошибка при задании номинала валюты')