from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired

class BookForm(FlaskForm):
    title = StringField("Book title", validators=[InputRequired()])
    author = StringField("Author full name", validators=[InputRequired()])
    submit = SubmitField("Add new book")
