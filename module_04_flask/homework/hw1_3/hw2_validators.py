from wtforms.validators import ValidationError
from wtforms import Field
from flask_wtf import FlaskForm

def number_length(min: int, max: int, message: str = None):
    """
    Функциональный валидатор для проверки длины числа (как строки).
    """
    if message is None:
        message = f"Длина числа должна быть от {min} до {max} символов"

    def _number_length(form: FlaskForm, field: Field):
        data = str(field.data) if field.data is not None else ""
        if not data.isdigit():
            raise ValidationError("Значение должно содержать только цифры")
        if not (min <= len(data) <= max):
            raise ValidationError(message)

    return _number_length

class NumberLength:
    """
    Класс-валидатор для проверки длины числа (как строки).
    """
    def __init__(self, min: int, max: int, message: str = None):
        self.min = min
        self.max = max
        if message is None:
            message = f"Длина числа должна быть от {min} до {max} символов"
        self.message = message

    def __call__(self, form: FlaskForm, field: Field):
        data = str(field.data) if field.data is not None else ""
        if not data.isdigit():
            raise ValidationError("Значение должно содержать только цифры")
        if not (self.min <= len(data) <= self.max):
            raise ValidationError(self.message)

from wtforms import StringField, Form

class MyForm(Form):
    phone1 = StringField("Телефон (функция)", validators=[number_length(10, 10)])

    phone2 = StringField("Телефон (класс)", validators=[NumberLength(10, 10)])