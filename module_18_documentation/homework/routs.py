from flask import Flask, request
from flasgger import Swagger, swag_from

app = Flask(__name__)
swagger = Swagger(app, template_file='post_endpoint.json')


@app.route('/hello')
@swag_from('hello_endpoint.yaml')
def hello():
    """
    Это пример GET-эндпоинта для Flasgger.
    """
    return 'Привет, {}'.format(request.args.get('name', 'Мир'))


@app.route('/post_hello', methods=['POST'])
def post_hello():
    """
    Это пример POST-эндпоинта для Flasgger.
    """
    name = request.form.get('name', 'Мир')
    return 'Привет, {}'.format(name)


if __name__ == '__main__':
    app.run(debug=True)
