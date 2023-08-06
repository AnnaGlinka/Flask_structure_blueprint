import requests
from flask import render_template, flash, redirect, url_for
from app.payments import bp
from app.extensions import db
from app.models.payment import Payment
from app.models.cart import Cart
from app.models.product import Product
from app.models.shipment import Shipment
from app.models.order import Order
from app.products.forms import SearchProductForm
from flask_login import login_required, current_user
from app.payments.forms import PaymentForm, CreditCartForm
from sqlalchemy.exc import IntegrityError

@bp.route('/')
@login_required
def index():
    payments = Payment.query.all()
    return render_template('payments/index.html', payments=payments)


@bp.context_processor
def base():
    form = SearchProductForm()
    return dict(form=form)


def update_total(carts, products):
    total = 0
    for cart in carts:
        total += (products[cart.product_id - 1].price * cart.quantity)
    return total


def update_payment_sum(payment):
    carts = Cart.query.filter(Cart.customer_id == current_user.id).all()
    products = Product.query.all()
    total = update_total(carts, products)
    payment.amount = total
    db.session.add(payment)
    db.session.commit()


@bp.route('/create_payment/<int:sum>', methods=['GET', 'POST'])
@login_required
def create_payment(sum):

    payment_created = Payment.query.filter_by(customer_id=current_user.id, status='Created').first()
    shipment_created = Shipment.query.filter_by(customer_id=current_user.id, status='Created').first()

    if payment_created and shipment_created:
        update_payment_sum(payment_created)
        return redirect(url_for('orders.review_order'))

    if payment_created and not shipment_created:
        update_payment_sum(payment_created)
        return redirect(url_for('shipments.add_shipment'))

    else:
        form = PaymentForm()
        if form.validate_on_submit():
            payment = Payment(payment_method=form.payment_method.data,
                              amount=sum,
                              status='Created',
                              customer_id=current_user.id)
            db.session.add(payment)
            db.session.commit()
            flash("New payment created")
            return redirect(url_for('shipments.add_shipment'))

        else:
            flash("Please select payment method")
            return render_template('payments/add_payment.html', form=form)

        # Clear the form
        form.payment_method.data = ''
        return render_template('shipments/add_shipment.html', form=form)


@bp.route('/payment')
@login_required
def review_payment():
    payment = Payment.query.filter_by(customer_id=current_user.id).order_by(Payment.id.desc()).first()
    return render_template('payments/customers_payment.html', payment=payment)


@bp.route('/payment_update', methods=['GET', 'POST'])
@login_required
def update_payment():
    payment_to_update = Payment.query.filter_by(customer_id=current_user.id, status="Created").first()
    form = PaymentForm()
    if form.validate_on_submit():
        payment_to_update.payment_method = form.payment_method.data
        db.session.add(payment_to_update)
        db.session.commit()
        # flash("Payment has been updated")
        return redirect(url_for('orders.review_order'))

    return render_template('payments/add_payment.html', form=form)


@bp.route('/payment/<int:id>')
@login_required
def delete_payment(id):
    payment_to_delete = Payment.query.get_or_404(id)
    admin_email = current_user.email
    if admin_email == 'aglinka8@gmail.com':

        try:
            db.session.delete(payment_to_delete)
            db.session.commit()
            flash("Payment was successfully deleted")
            # Grab all categories
            payments = Payment.query.order_by(Payment.id)
            return render_template("payments/index.html", payments=payments)

        except IntegrityError:
            db.session.rollback()
            flash("Payment cannot be deleted!")
            payments = Payment.query.order_by(Payment.id)
            return render_template("payments/index.html", payments=payments)

    else:
        flash("You are not authorized to delete categories!")
        payments = Payment.query.order_by(Payment.id)
        return render_template("payments/index.html", payments=payments)


@bp.route('/credit_card_details', methods=['GET', 'POST'])
@login_required
def add_credit_card_details():
    payment = Payment.query.filter_by(customer_id=current_user.id, status='Created').first()
    form = CreditCartForm()
    if form.validate_on_submit():

        headers = {
            'Content-Type': 'application/json',
        }

        json_data = {
            'type': 'card',
            'cardNumber': form.card_number.data,
            'cardCvv': form.card_Cvv.data,
            'cardExpMonth': form.card_exp_month.data,
            'cardExpYear': form.card_exp_year.data,
            'amount': str(payment.amount),
        }

        response = requests.post('https://dummypay.io/pay', headers=headers, json=json_data)

        endpoint = 'https://dummypay.io/card/' + str(form.card_number.data)
        response = requests.get(endpoint)

        flash("Successful Credit Card Validation!" + " Response " + response.reason)

        response = requests.get('https://dummypay.io/card/' + form.card_number.data).json()
        flash(response['balance'])

        flash('Correct payment: ' + str(response['balance'] == payment.amount))

        form.card_number.data = ''
        form.card_Cvv.data = ''
        form.card_exp_month.data = ''
        form.card_exp_year.data = ''

        order = Order.query.filter_by(customer_id=current_user.id, status='Created').first()
        if order and (response['balance'] == payment.amount):
            order.status = 'Order paid'
            db.session.commit()
            return render_template('orders/finalized_order_message.html', order=order)

        else:
            flash("Something wrong with your payment!")
    else:
        if form.errors:
            for e in form.errors:
                flash("Validation error: " + str(e))

    return render_template('payments/credit_card_details.html', form=form)







