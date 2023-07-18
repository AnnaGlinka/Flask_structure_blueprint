from app.extensions import db
from datetime import datetime


class Shipment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    shipment_date = db.Column(db.DateTime, default=datetime.utcnow(), nullable=False)
    country = db.Column(db.String(120), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    postal_code = db.Column(db.String(20), nullable=False)
    street = db.Column(db.String(120), nullable=False)
    house_number = db.Column(db.String(20), nullable=False)
    apartment_number = db.Column(db.String(20))
    shipment_cost = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(120), nullable=False)

    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))


    #
    # # one-to-many, mandatory
    orders = db.relationship('Order', backref='shipment')

    def __repr__(self):
        return f'<Shipment "{self.id}">'
