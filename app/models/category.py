from app.extensions import db


class Category(db.Model):
    category_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False, unique=True)

    # one-to-many, optional
    products = db.relationship('Product', backref='Category')

    def __repr__(self):
        return f'<Product "{self.name}">'
