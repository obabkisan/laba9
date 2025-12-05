"""Пакет моделей данных для приложения курсов валют.

Содержит классы для представления сущностей предметной области:
    - Author: информация об авторе приложения
    - User: пользователь системы
    - Currency: валюта с курсом и метаданными
    - UserCurrency: подписка пользователя на валюту
    - App: метаинформация о приложении

Все модели реализуют:
    - инкапсуляцию через приватные атрибуты
    - валидацию данных в сеттерах
    - аннотации типов Python
    - свойства (property) для контролируемого доступа
"""

from .author import Author
from .app import App
from .user import User
from .currency import Currency
from .user_currency import UserCurrency

__all__ = ['Author', 'App', 'User', 'Currency', 'UserCurrency']
