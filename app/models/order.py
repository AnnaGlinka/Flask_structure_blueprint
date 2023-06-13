from app.extensions import db


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer = db.relationship("Customers", uselist=False, backref='order')
    purchase_list = db.relationship("Products", backref='order')
    status = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f'<Post "{self.title}">'
