from flask import render_template, flash
from sqlalchemy.exc import IntegrityError
from app.extensions import db
from app.orders import bp
from app.models.order import Order
from app.models.shipment import Shipment
from app.models.payment import Payment
from app.models.cart import Cart
from app.models.product import Product
from app.products.forms import SearchProductForm
from app.models.order_item import OrderItem
from flask_login import login_required, current_user

@bp.route('/')
@login_required
def index():
    orders = Order.query.all()
    order_items = OrderItem.query.all()
    return render_template('orders/index.html', orders=orders, order_items=order_items)

@bp.context_processor
def base():
    form = SearchProductForm()
    return dict(form=form)


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


def update_total(carts, products):
    total = 0
    for cart in carts:
        total += (products[cart.product_id - 1].price * cart.quantity)
    return total

@bp.route('/review_order')
@login_required
def review_order():

    order_created = Order.query.filter_by(customer_id=current_user.id, status='Created').first()
    payment = Payment.query.filter_by(customer_id=current_user.id, status='Created').first()
    shipment = Shipment.query.filter_by(customer_id=current_user.id, status='Created').first()

    if order_created is None:
        order = Order(total_price=payment.amount,
                      status="Created",
                      customer_id=current_user.id,
                      payment_id=payment.id,
                      shipment_id=shipment.id
                      )
        db.session.add(order)
        db.session.commit()

    order = Order.query.filter_by(customer_id=current_user.id, status='Created').first()

    carts = Cart.query.filter(Cart.customer_id == current_user.id).all()
    products = Product.query.all()
    total = update_total(carts, products)

    return render_template('orders/review_order.html',
                           order=order,
                           shipment=shipment,
                           payment=payment,
                           carts=carts,
                           products=products,
                           total=total)


@bp.route('/order_and_pay')
@login_required
def order_with_obligation_to_pay():
    order = Order.query.filter_by(customer_id=current_user.id, status='Created').first()
    carts = Cart.query.filter(Cart.customer_id == current_user.id).all()
    order_items_created = OrderItem.query.filter(OrderItem.order_id == order.id).all()
    if not order_items_created:
        for cart in carts:
            product = Product.query.filter_by(id=cart.product_id).first()
            order_item = OrderItem(quantity=cart.quantity,
                                   price=product.price,
                                   product_id=cart.product_id,
                                   order_id=order.id
                                   )
            db.session.add(order_item)
            db.session.delete(cart)

        db.session.commit()

    order_items = OrderItem.query.filter(OrderItem.order_id == order.id).all()
    return render_template('orders/order.html', order=order, order_items=order_items)


@bp.route('/order/<int:id>')
def show_ordered(id):
    order = Order.query.get_or_404(id)
    order_items = OrderItem.query.filter(OrderItem.order_id == order.id).all()
    return render_template('orders/paid_order_details.html', order=order, order_items=order_items)





