from wtforms.validators import ValidationError

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

    def __call__(self, form, field):
        data = str(field.data) if field.data is not None else ""
        if not data.isdigit():
            raise ValidationError("Значение должно содержать только цифры")
        if not (self.min <= len(data) <= self.max):
            raise ValidationError(self.message)


from wtforms import StringField, Form


class MyForm(Form):
    # функциональный валидатор
    phone1 = StringField("Телефон (функция)", validators=[number_length(10, 10)])

    # класс-валидатор
    phone2 = StringField("Телефон (класс)", validators=[NumberLength(10, 10)])