from flask import render_template, flash
from app.carts import bp
from app.extensions import db
from app.models.cart import Cart
from app.models.product import Product
from app.models.customer import Customer
from flask_login import login_required, current_user

@bp.route('/')
@login_required
def index():
    carts = Cart.query.all()
    products = Product.query.all()
    customers = Customer.query.all()
    return render_template('carts/index.html',
                           carts=carts,
                           products=products,
                           customers=customers)


@bp.route('/')
@login_required
def show_user_carts():
    carts = Cart.query.filter(customer_id=current_user.id)
    return render_template('carts/index.html', carts=carts)








