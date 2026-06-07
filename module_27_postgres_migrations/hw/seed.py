import requests
import requests
import random
from extensions import db
from models import Coffee, User

def seed_data():
    # Кофе
    coffee_data = requests.get("https://dummyjson.com/products/search?q=coffee").json()["products"]
    c = coffee_data[0]
    coffee = Coffee(
        title=c["title"],
        category=c.get("category"),
        description=c.get("description"),
        reviews=[r["comment"] for r in c.get("reviews", [])]
    )
    db.session.add(coffee)
    db.session.commit()

    # Пользователи
    users_data = requests.get("https://dummyjson.com/users").json()["users"]
    for i in range(10):
        user_data = users_data[i]
        user = User(
            name=user_data["firstName"],
            has_sale=bool(random.getrandbits(1)),
            address=user_data["address"],
            coffee_id=coffee.id
        )
        db.session.add(user)
    db.session.commit()
