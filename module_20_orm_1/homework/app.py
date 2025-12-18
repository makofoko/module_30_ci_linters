from flask import Flask, request, jsonify
from datetime import date
from sqlalchemy.orm import sessionmaker
from orm import engine, Book, ReceivingBooks

app = Flask(__name__)
Session = sessionmaker(bind=engine)

@app.route("/books", methods=["GET"])
def get_books():
    session = Session()
    books = session.query(Book).all()
    return jsonify([{"id": b.id, "title": b.title, "author_id": b.author_id} for b in books])

@app.route("/debtors", methods=["GET"])
def get_debtors():
    session = Session()
    debtors = session.query(ReceivingBooks).filter(
        ReceivingBooks.date_return == None,
        ReceivingBooks.count_date_with_book > 14
    ).all()
    return jsonify([{"student_id": d.student_id, "book_id": d.book_id, "days": d.count_date_with_book} for d in debtors])

@app.route("/give_book", methods=["POST"])
def give_book():
    session = Session()
    data = request.json
    rb = ReceivingBooks(student_id=data["student_id"], book_id=data["book_id"], date_receiving=date.today())
    session.add(rb)
    session.commit()
    return jsonify({"status": "book given"})

@app.route("/return_book", methods=["POST"])
def return_book():
    session = Session()
    data = request.json
    rb = session.query(ReceivingBooks).filter_by(
        student_id=data["student_id"],
        book_id=data["book_id"],
        date_return=None
    ).first()
    if not rb:
        return jsonify({"error": "no such record"}), 400
    rb.date_return = date.today()
    session.commit()
    return jsonify({"status": "book returned"})

if __name__ == "__main__":
    app.run(debug=True)