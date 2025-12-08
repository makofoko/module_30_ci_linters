from flask import Flask, render_template, request, redirect, url_for
from models import (
    init_db,
    get_all_books,
    add_book,
    get_books_by_author,
    get_book_by_id,
    increment_views,
    get_books_count,
    DATA
)
from forms import BookForm

app: Flask = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # нужен для WTForms


@app.route('/books')
def all_books() -> str:
    books = get_all_books()
    total = get_books_count()
    return render_template(
        'index.html',
        books=books,
        total_books=total
    )


@app.route('/books/form', methods=['GET', 'POST'])
def get_books_form():
    form = BookForm()
    if form.validate_on_submit():
        add_book(form.title.data, form.author.data)
        return redirect(url_for('all_books'))
    return render_template('add_book.html', form=form)


@app.route('/books/author/<author_name>')
def books_by_author(author_name: str):
    books = get_books_by_author(author_name)
    return render_template('author_books.html', books=books, author=author_name)


@app.route('/books/<int:book_id>')
def book_detail(book_id: int):
    book = get_book_by_id(book_id)
    if not book:
        return "Book not found", 404
    increment_views(book_id)
    return render_template('book_detail.html', book=book)


if __name__ == '__main__':
    init_db(DATA)
    app.run(debug=True)
