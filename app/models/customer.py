from flask import Flask
from datetime import datetime
from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class Customer(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(200), nullable=False)
    last_name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    address = db.Column(db.Text(), nullable=False)
    phone_number = db.Column(db.String(200), nullable=False)

    # one-to-many, optional
    shipments = db.relationship('Shipment', backref='customer')
    orders = db.relationship('Order', backref='customer')
    payments = db.relationship('Payment', backref='customer')
    carts = db.relationship('Cart', backref='customer')

    data_added = db.Column(db.DateTime, default=datetime.utcnow())
    password_hash = db.Column(db.String(128))


    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<Customer "{self.email}">'
