from flask import Flask, request, jsonify
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from init_db import engine, Author, Book, Student, ReceivingBooks
from datetime import date
import csv
from io import StringIO

app = Flask(__name__)
Session = sessionmaker(bind=engine)

@app.route("/books_by_author/<int:author_id>", methods=["GET"])
def books_by_author(author_id):
    session = Session()
    count = session.query(func.count(Book.id)).filter(Book.author_id == author_id).scalar()
    return jsonify({"author_id": author_id, "books_count": count})

@app.route("/unread_books/<int:student_id>", methods=["GET"])
def unread_books(student_id):
    session = Session()
    read_books = session.query(Book.id).join(ReceivingBooks).filter(ReceivingBooks.student_id == student_id).subquery()
    author_ids = session.query(Book.author_id).filter(Book.id.in_(read_books)).distinct().subquery()
    unread = session.query(Book).filter(Book.author_id.in_(author_ids)).filter(~Book.id.in_(read_books)).all()
    return jsonify([{"id": b.id, "title": b.title} for b in unread])

@app.route("/avg_books_month", methods=["GET"])
def avg_books_month():
    session = Session()
    month = date.today().month
    avg = session.query(func.avg(func.count(ReceivingBooks.id))).join(Student).filter(func.strftime("%m", ReceivingBooks.date_receiving) == str(month)).group_by(Student.id).scalar()
    return jsonify({"avg_books_per_student": avg})

@app.route("/popular_book", methods=["GET"])
def popular_book():
    session = Session()
    book = session.query(Book.title, func.count(ReceivingBooks.id).label("cnt")).join(ReceivingBooks).join(Student).filter(Student.avg_grade > 4.0).group_by(Book.id).order_by(func.count(ReceivingBooks.id).desc()).first()
    return jsonify({"title": book.title, "count": book.cnt})

@app.route("/top_students", methods=["GET"])
def top_students():
    session = Session()
    year = date.today().year
    students = session.query(Student.name, func.count(ReceivingBooks.id).label("cnt")).join(ReceivingBooks).filter(func.strftime("%Y", ReceivingBooks.date_receiving) == str(year)).group_by(Student.id).order_by(func.count(ReceivingBooks.id).desc()).limit(10).all()
    return jsonify([{"name": s.name, "count": s.cnt} for s in students])

# 🔹 Новый роут: загрузка CSV
@app.route("/upload_students", methods=["POST"])
def upload_students():
    session = Session()
    file = request.files["file"]
    stream = StringIO(file.stream.read().decode("utf-8"))
    reader = csv.DictReader(stream, delimiter=";")
    students = [dict(row) for row in reader]
    session.bulk_insert_mappings(Student, students)
    session.commit()
    return jsonify({"status": "students uploaded", "count": len(students)})

if __name__ == "__main__":
    app.run(debug=True)