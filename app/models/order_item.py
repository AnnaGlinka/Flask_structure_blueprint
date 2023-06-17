from datetime import datetime
from app.extensions import db


class Order_Item(db.Model):
    order_item_id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Real, nullable=False)
    total_price = db.Column(db.Real, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'))
    order_id = db.Column(db.Integer, db.ForeignKey('order.order_id'), primary_key=True)


    def __repr__(self):
        return f'<Order_Item "{self.order_item_id}">'
