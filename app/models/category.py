from app.extensions import db


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False, unique=True)
    picture = db.Column(db.String(), nullable=True)

    # one-to-many, optional
    products = db.relationship('Product', backref='category')

    def __repr__(self):
        return f'<Product "{self.id}">'
