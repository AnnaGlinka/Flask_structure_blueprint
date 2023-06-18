from app.extensions import db


class Cart(db.Model):
    __tablename__ = 'Cart'
    cart_id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.customer_id'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'))

    def __repr__(self):
        return f'<Cart "{self.cart_id}">'
