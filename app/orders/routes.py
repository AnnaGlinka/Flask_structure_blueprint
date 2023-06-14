from flask import render_template
from app.orders import bp
from app.extensions import db
from app.models.order import Order

@bp.route('/')
def index():
    orders = Order.query.all()
    return render_template('orders/index.html', orders=orders)


@bp.route('/categories/')
def categories():
    return render_template('orders/categories.html')
