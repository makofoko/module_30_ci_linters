from flask import Flask, request, jsonify
from extensions import db
from models import Coffee, User
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://magzhan:secret@localhost:5432/skillbox_db"
db.init_app(app)

with app.app_context():
    db.create_all()

# 1. Добавление пользователя
@app.route("/add_user", methods=["POST"])
def add_user():
    data = request.json
    coffee_id = random.choice([c.id for c in Coffee.query.all()])
    user = User(
        name=data.get("name", "NoName"),
        has_sale=bool(random.getrandbits(1)),
        address=data.get("address", {"country": "Kazakhstan"}),
        coffee_id=coffee_id
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({"id": user.id, "name": user.name, "coffee": user.coffee.title})

# 2. Поиск кофе по названию (LIKE вместо полнотекстового поиска для простоты)
@app.route("/search_coffee")
def search_coffee():
    title = request.args.get("title")
    coffee = Coffee.query.filter(Coffee.title.ilike(f"%{title}%")).all()
    return jsonify([{"id": c.id, "title": c.title, "description": c.description} for c in coffee])

# 3. Список уникальных заметок (reviews)
@app.route("/coffee_notes")
def coffee_notes():
    notes = set()
    for c in Coffee.query.all():
        if c.reviews:
            notes.update(c.reviews)
    return jsonify(list(notes))

# 4. Список пользователей по стране
@app.route("/users_by_country")
def users_by_country():
    country = request.args.get("country")
    users = User.query.filter(User.address["country"].astext == country).all()
    return jsonify([{"id": u.id, "name": u.name, "country": u.address.get("country")} for u in users])

if __name__ == "__main__":
    app.run(debug=True)

