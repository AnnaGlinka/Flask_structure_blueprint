from datetime import datetime
from app.extensions import db
from app.models.product import Product
from app.extensions import db


class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))


    def __repr__(self):
        return f'<OrderItem "{self.id}">'

    def get_product_name(self, prod_id: int) -> str:
        product = Product.query.filter_by(id=prod_id).first()
        return product.name
