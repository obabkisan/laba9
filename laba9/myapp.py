"""
Основной модуль приложения для отображения курсов валют.
Реализует MVC архитектуру с полным разделением ответственности.
"""

from jinja2 import Environment, PackageLoader, select_autoescape
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from utils.currencies_api import get_currencies
from controllers.databasecontroller import CurrencyRatesCRUD
from controllers.currencycontroller import CurrencyController
from controllers.pages import PagesController
from models import Author, App

# Инициализация Jinja2 Environment
env = Environment(loader=PackageLoader("laba9"), autoescape=select_autoescape())

# Создание контроллеров
db_controller = CurrencyRatesCRUD()
currency_controller = CurrencyController(db_controller)
pages_controller = PagesController(env)  # Без currency_controller!

# Данные приложения
author = Author('Прозорова Полина', 'P3120')
app = App("CurrenciesListApp", "1.0", author)

# Начальное обновление курсов из API
currency_list = ['USD', 'EUR', 'GBP']
data = get_currencies(currency_list)
for code, value in data.items():
    try:
        new_value = float(value.replace(',', '.'))
        currency_controller.update_currency_value(code, new_value)
    except ValueError as e:
        print(f"Ошибка обновления {code}: {e}")


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    """Обработчик HTTP запросов с MVC маршрутизацией"""

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        params = parse_qs(parsed.query)

        try:
            if path == '/':
                currencies = currency_controller.get_all_currencies()
                html = pages_controller.render_index(author.name, author.group, currencies)

            elif path == '/author':
                html = pages_controller.render_author(author.name, author.group)

            elif path == '/currencies':
                currencies = currency_controller.get_all_currencies()
                html = pages_controller.render_currencies(author.name, author.group, currencies)

            elif path == '/users':
                html = self.handle_users_page()

            elif path == '/user':
                user_id = int(params.get('id', [1])[0])
                html = self.handle_user_page(user_id)

            elif 'currency/delete' in path:
                if 'id' in params:
                    currency_id = int(params['id'][0])
                    currency_controller.delete_currency(currency_id)
                self.send_redirect('/currencies')
                return

            elif 'currency/update' in path:
                self.handle_currency_update(params)
                self.send_redirect('/currencies')
                return

            elif 'currency/create' in path:
                self.handle_currency_create(params)
                self.send_redirect('/currencies')
                return

            elif 'currency/show' in path:
                self.show_currencies_in_console()
                html = "<h1>Данные выведены в консоль</h1>"

            elif path == '/currencies/update':
                self.update_from_api()
                self.send_redirect('/currencies')
                return

            else:
                html = pages_controller.render_error("Страница не найдена")

            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(html.encode('utf-8'))

        except Exception as e:
            html = pages_controller.render_error(f"Ошибка: {str(e)}")
            self.send_response(500)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(html.encode('utf-8'))

    def handle_users_page(self):
        template = env.get_template("users.html")
        users = db_controller._read_users()
        return template.render(
            myapp="CurrenciesListApp",
            author_name=author.name,
            group=author.group,
            users=users,
            current_user=None,
            user_currencies=[]
        )

    def handle_user_page(self, user_id):
        template = env.get_template("users.html")
        users = db_controller._read_users()
        current_user = next((u for u in users if u['id'] == user_id), None)
        if not current_user and users:
            current_user = users[0]
        user_currencies = db_controller._read_user_currencies(user_id)
        return template.render(
            myapp="CurrenciesListApp",
            author_name=author.name,
            group=author.group,
            users=users,
            current_user=current_user,
            user_currencies=user_currencies
        )

    def handle_currency_update(self, params):
        for key, value in params.items():
            if key.upper() in ['USD', 'EUR', 'GBP', 'CNY', 'JPY', 'CHF', 'TRY', 'KZT']:
                try:
                    new_value = float(value[0])
                    currency_controller.update_currency_value(key.upper(), new_value)
                except (ValueError, KeyError) as e:
                    print(f"Ошибка обновления {key}: {e}")

    def handle_currency_create(self, params):
        """Обработка создания новой валюты через GET-параметры"""
        required = ['num_code', 'char_code', 'name', 'value', 'nominal']
        try:
            data = {key: params[key][0] for key in required}
            currency_controller.create_currency(
                num_code=data['num_code'],
                char_code=data['char_code'],
                name=data['name'],
                value=float(data['value']),
                nominal=int(data['nominal'])
            )
        except (KeyError, ValueError, TypeError) as e:
            print(f"Ошибка создания валюты: {e}")

    def show_currencies_in_console(self):
        currencies = currency_controller.get_all_currencies()
        print("Текущие курсы валют:")
        for currency in currencies:
            formatted = currency_controller.format_currency_for_display(currency)
            print(f"{formatted['code']}: {formatted['value']} руб.")

    def update_from_api(self):
        currency_list = ['USD', 'EUR', 'GBP']
        data = get_currencies(currency_list)
        for code, value in data.items():
            try:
                new_value = float(value.replace(',', '.'))
                currency_controller.update_currency_value(code, new_value)
            except ValueError as e:
                print(f"Ошибка обновления {code}: {e}")

    def send_redirect(self, location):
        self.send_response(302)
        self.send_header('Location', location)
        self.end_headers()


http = HTTPServer(('localhost', 8080), SimpleHTTPRequestHandler)
print('Сервер запущен на http://localhost:8080')
http.serve_forever()