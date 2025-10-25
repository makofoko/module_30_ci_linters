from wtforms.validators import ValidationError

def number_length(min: int, max: int, message: Optional[str] = None):
    """
    Валидатор для проверки длины числа (как строки).
    """
    if message is None:
        message = f"Длина числа должна быть от {min} до {max} символов"

    def _number_length(form, field: Field):
        data = str(field.data) if field.data is not None else ""
        if not data.isdigit():
            raise ValidationError("Значение должно содержать только цифры")
        if not (min <= len(data) <= max):
            raise ValidationError(message)

    return _number_length

phone = StringField("Телефон", validators=[number_length(10, 10)])
