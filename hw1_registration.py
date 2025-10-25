from flask import Flask
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, NumberRange, Optional, Regexp

app = Flask(__name__)


class RegistrationForm(FlaskForm):
    email = StringField(
        "Email",
        validators=[
            DataRequired(message="Email обязателен"),
            Email(message="Некорректный формат email")
        ]
    )

    phone = StringField(
        "Телефон",
        validators=[
            DataRequired(message="Телефон обязателен"),
            Regexp(r'^[0-9]{10}$', message="Телефон должен состоять из 10 цифр")
        ]
    )

    name = StringField(
        "Имя",
        validators=[DataRequired(message="Имя обязательно")]
    )

    address = StringField(
        "Адрес",
        validators=[DataRequired(message="Адрес обязателен")]
    )

    index = IntegerField(
        "Индекс",
        validators=[
            DataRequired(message="Индекс обязателен"),
            NumberRange(min=0, message="Индекс должен быть положительным числом")
        ]
    )

    comment = TextAreaField(
        "Комментарий",
        validators=[Optional()]
    )


@app.route("/registration", methods=["POST"])
def registration():
    form = RegistrationForm()

    if form.validate_on_submit():
        email, phone = form.email.data, form.phone.data
        return f"Successfully registered user {email} with phone +7{phone}"

    return f"Invalid input, {form.errors}", 400

if __name__ == "__main__":
    app.config["WTF_CSRF_ENABLED"] = False
    app.run(debug=True)