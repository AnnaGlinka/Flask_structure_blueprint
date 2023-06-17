from flask import render_template
from app.payments import bp
from app.extensions import db
from app.models.payment import Payment

@bp.route('/')
def index():
    payments = Payment.query.all()
    return render_template('payments/index.html', payments=payments)


@bp.route('/categories/')
def categories():
    return render_template('payments/categories.html')
