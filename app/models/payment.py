from app.extensions import db
from datetime import datetime


class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    payment_date = db.Column(db.DateTime, default=datetime.utcnow())
    payment_method = db.Column(db.String(150), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(150), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    #
    # # one-to-many, mandatory
    orders = db.relationship('Order', backref='payment')

    def __repr__(self):
        return f'<Payment "{self.id}">'



