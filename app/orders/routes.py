from flask import render_template, flash
from app.extensions import db
from app.orders import bp
from app.models.order import Order
from flask_login import login_required, current_user

@bp.route('/')
@login_required
def index():
    orders = Order.query.all()
    return render_template('orders/index.html', orders=orders)


@bp.route('/create_order')
@login_required
def create_order():
    order = Order(total_price=100,
                  status="Created",
                  customer_id=current_user.id,
                  payment_id=3,
                  shipment_id=4
                  )
    db.session.add(order)
    db.session.commit()
    flash("New order created")
    return render_template('orders/show_order.html', order=order)
