from flask import Flask, url_for, render_template_string

app = Flask(__name__)


@app.route('/dogs')
def dogs():
    return 'Страница с пёсиками'


@app.route('/cats')
def cats():
    return 'Страница с котиками'


@app.route('/cats/<int:cat_id>')
def cat_page(cat_id: int):
    return f'Страница с котиком {cat_id}'


@app.route('/index')
def index():
    return 'Главная страница'

@app.errorhandler(404)
def page_not_found(error):
    """
    Обработчик ошибки 404.
    Собирает список всех URL и выводит их как HTML.
    """
    links_html = ""

    for rule in app.url_map.iter_rules():
        if rule.endpoint != 'static' and not rule.arguments:

            url = url_for(rule.endpoint)

            links_html += f'<li><a href="{url}">{rule.rule}</a></li>'

    output = f"""
    <h1>404 - Страница не найдена</h1>
    <p>Запрошенный URL не существует. Доступные страницы:</p>
    <ul>
        {links_html}
    </ul>
    """
    return output, 404

if __name__ == '__main__':
    app.run(debug=True)