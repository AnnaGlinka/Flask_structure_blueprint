from flask import render_template
from app.order_items import bp
from app.extensions import db
from app.models.order_item import OrderItem

@bp.route('/')
def index():
    order_items = OrderItem.query.all()
    return render_template('order_items/index.html', order_items=order_items)


@bp.route('/categories/')
def categories():
    return render_template('order_items/categories.html')
