from flask import Flask, render_template
from typing import List

from models import init_db, get_all_books, DATA
import sqlite3

app: Flask = Flask(__name__)


def _get_html_table_for_books(books: List[dict]) -> str:
    table = """
<table>
    <thead>
    <tr>
        <th>ID</th>
        <th>Title</th>
        <th>Author</th>
    </tr>
    </thead>
    <tbody>
        {books_rows}
    </tbody>
</table>
"""
    rows: str = ''
    for book in books:
        rows += '<tr><td>{id}</td><td>{title}</td><td>{author}</td></tr>'.format(
            id=book['id'], title=book['title'], author=book['author'],
        )
    return table.format(books_rows=rows)


def get_books_count() -> int:
    """Возвращает общее количество книг в базе данных."""
    with sqlite3.connect("../homework.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM table_books;")
        return cursor.fetchone()[0]


@app.route('/books')
def all_books() -> str:
    books = get_all_books()
    total = get_books_count()
    return render_template(
        'index.html',
        books=books,
        total_books=total
    )


@app.route('/books/form')
def get_books_form() -> str:
    return render_template('add_book.html')


if __name__ == '__main__':
    init_db(DATA)
    app.run(debug=True)