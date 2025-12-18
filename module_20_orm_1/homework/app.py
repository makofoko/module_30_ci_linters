from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

engine = create_engine("sqlite:///library.db")
Session = sessionmaker(bind=engine)

@app.route("/books", methods=["GET"])
def get_books():
    session = Session()
    books = session.query(Book).all()
    return jsonify([{"id": b.id, "title": b.title} for b in books])

@app.route("/debtors", methods=["GET"])
def get_debtors():
    session = Session()
    debtors = session.query(ReceivingBooks).filter(
        ReceivingBooks.date_return == None,
        ReceivingBooks.count_date_with_book > 14
    ).all()
    return jsonify([{"student_id": d.student_id, "book_id": d.book_id} for d in debtors])

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
    rb = session.query(ReceivingBooks).filter_by(student_id=data["student_id"], book_id=data["book_id"], date_return=None).first()
    if not rb:
        return jsonify({"error": "no such record"}), 400
    rb.date_return = date.today()
    session.commit()
    return jsonify({"status": "book returned"})

@app.route("/search_book", methods=["GET"])
def search_book():
    session = Session()
    query = request.args.get("q", "")
    books = session.query(Book).filter(Book.title.like(f"%{query}%")).all()
    return jsonify([{"id": b.id, "title": b.title} for b in books])
if __name__ == "__main__": app.run(debug=True)