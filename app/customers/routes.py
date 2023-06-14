from flask import render_template
from app.customers import bp
from app.extensions import db
from app.models.customer import Customer

@bp.route('/')
def index():
    customers = Customer.query.all()
    return render_template('customers/index.html', customers=customers)


@bp.route('/categories/')
def categories():
    return render_template('customers/categories.html')
