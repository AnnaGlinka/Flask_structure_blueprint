from datetime import datetime
from app.extensions import db


class Order_Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    # primarykey do order id usuniete

    def __repr__(self):
        return f'<Order_Item "{self.id}">'
