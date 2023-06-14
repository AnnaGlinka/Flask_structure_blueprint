from flask import Flask
from datetime import datetime
from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class Customer(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    surname = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    country = db.Column(db.String(120), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    postal_code = db.Column(db.String(20), nullable=False)
    street = db.Column(db.String(120), nullable=False)
    house_number = db.Column(db.String(20), nullable=False)
    apartment_number = db.Column(db.String(20))
    data_added = db.Column(db.DateTime, default=datetime.utcnow())
    password_hash = db.Column(db.String(128))
    # completed_orders = db.relationship('Order', backref='customer')
    # shopping_cart = db.Column(db.Integer, db.ForeignKey('order.id'))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<Customer "{self.name}">'
