"""
Контроллер для рендеринга страниц через Jinja2.
Отделяет логику рендеринга от бизнес-логики и маршрутизации.
"""

from jinja2 import Environment


class PagesController:
    """Контроллер для рендеринга HTML страниц"""

    def __init__(self, env: Environment):
        self.env = env

    def render_index(self, author_name: str, group: str, currencies):
        """Рендеринг главной страницы"""
        template = self.env.get_template("index.html")
        return template.render(
            myapp="CurrenciesListApp",
            author_name=author_name,
            group=group,
            currencies=currencies
        )

    def render_currencies(self, author_name: str, group: str, currencies):
        """Рендеринг страницы валют"""
        template = self.env.get_template("currencies.html")
        return template.render(
            myapp="CurrenciesListApp",
            author_name=author_name,
            group=group,
            currencies=currencies
        )

    def render_author(self, author_name: str, group: str):
        """Рендеринг страницы об авторе"""
        template = self.env.get_template("author.html")
        return template.render(
            myapp="CurrenciesListApp",
            author_name=author_name,
            group=group
        )

    def render_error(self, message: str):
        """Рендеринг страницы ошибки"""
        error_html = f"""
        <!DOCTYPE html>
        <html>
        <head><title>Ошибка</title></head>
        <body>
            <h1>Ошибка</h1>
            <p>{message}</p>
            <a href="/">На главную</a>
        </body>
        </html>
        """
        return error_html