from flask import render_template, flash, redirect, url_for
from app.payments import bp
from app.extensions import db
from app.models.payment import Payment
from flask_login import login_required, current_user
from app.payments.forms import PaymentForm
from sqlalchemy.exc import IntegrityError

@bp.route('/')
@login_required
def index():
    payments = Payment.query.all()
    return render_template('payments/index.html', payments=payments)


@bp.route('/create_payment/<int:sum>', methods=['GET', 'POST'])
@login_required
def create_payment(sum):

    payment_created = Payment.query.filter_by(customer_id=current_user.id, status='Created').first()
    if not payment_created:
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
    else:
        flash("The payments is already created")
        return redirect(url_for('payments.review_payment'))



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
        return redirect(url_for('shipments.add_shipment'))

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







