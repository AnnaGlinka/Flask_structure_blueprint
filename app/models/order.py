from datetime import datetime
from app.extensions import db


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow(), nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(200), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    payment_id = db.Column(db.Integer, db.ForeignKey('payment.id'))
    shipment_id = db.Column(db.Integer, db.ForeignKey('shipment.id'))


    # one-to-many, mandatory
    order_items = db.relationship('OrderItem', backref='order')

    def __repr__(self):
        return f'<Order "{self.id}">'
