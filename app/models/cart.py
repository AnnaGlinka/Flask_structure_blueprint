from app.extensions import db


class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))

    # customer_id -> primary key

    def __repr__(self):
        return f'<Cart "{self.cart_id}">'
