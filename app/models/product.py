from app.extensions import db


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Numeric, nullable=False)
    number_in_stock = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(150), nullable=False)

    def __repr__(self):
        return f'<Product "{self.name}">'
