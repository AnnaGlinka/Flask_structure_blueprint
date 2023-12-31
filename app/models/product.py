from app.extensions import db

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Numeric, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id',  ondelete='RESTRICT'), nullable=False)
    #
    # # one-to-many, optional
    order_item = db.relationship('OrderItem', backref='product')
    cart = db.relationship('Cart', backref='product')

    def __repr__(self):
        return f'{self.description}'
