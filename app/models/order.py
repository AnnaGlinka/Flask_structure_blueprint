from datetime import datetime
from app.extensions import db


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    status = db.Column(db.String(20), default="Pending", nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow(), nullable=False)
    purchase_list = db.relationship(JsonEncodeDict)

    def __repr__(self):
        return f'<Order "{self.id}">'
