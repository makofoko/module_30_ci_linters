

class Coffee(db.Model):
    __tablename__ = "coffee"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(200))
    description = db.Column(db.String(200))
    reviews = db.Column(db.ARRAY(db.String))

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    has_sale = db.Column(db.Boolean)
    address = db.Column(db.JSON)
    coffee_id = db.Column(db.Integer, db.ForeignKey("coffee.id"))
    coffee = db.relationship("Coffee")
