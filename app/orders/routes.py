from flask import render_template, flash
from sqlalchemy.exc import IntegrityError
from app.extensions import db
from app.orders import bp
from app.models.order import Order
from app.models.shipment import Shipment
from app.models.payment import Payment
from flask_login import login_required, current_user

@bp.route('/')
@login_required
def index():
    orders = Order.query.all()
    return render_template('orders/index.html', orders=orders)


# @bp.route('/create_order')
# @login_required
# def create_order():
#     order = Order(total_price=100,
#                   status="Created",
#                   customer_id=current_user.id,
#                   payment_id="dummy",
#                   shipment_id="dummy"
#                   )
#     db.session.add(order)
#     db.session.commit()
#     flash("New order created")



@bp.route('/delete_order/<int:id>')
@login_required
def delete_order(id):
    order_to_delete = Order.query.get_or_404(id)
    admin_email = current_user.email
    if admin_email == 'aglinka8@gmail.com':
        try:
            db.session.delete(order_to_delete)
            db.session.commit()
            flash("Order was deleted")
            orders = Order.query.order_by(Order.id)
            return render_template("orders/index.html", orders=orders)

        except IntegrityError:
            db.session.rollback()
            flash("Order cannot be deleted!")
            orders = Order.query.order_by(Order.id)
            return render_template("orders/index.html", orders=orders)

    else:
        flash("You are not authorized to delete orders!")
        orders = Order.query.order_by(Order.id)
        return render_template("orders/index.html", orders=orders)


@bp.route('/review_order')
@login_required
def review_order():

    order_created = Order.query.filter_by(customer_id=current_user.id, status='Created').first()
    if order_created is None:
        order = Order(total_price=100,
                      status="Created",
                      customer_id=current_user.id,
                      payment_id="dummy",
                      shipment_id="dummy"
                      )
        db.session.add(order)
        db.session.commit()

    order = Order.query.filter_by(customer_id=current_user.id, status='Created').first()
    shipment = Shipment.query.filter_by(customer_id=current_user.id).first()
    payment = Payment.query.filter_by(customer_id=current_user.id).first()

    return render_template('orders/review_order.html', order=order, shipment=shipment, payment=payment)

