from flask import render_template, flash
from sqlalchemy.exc import IntegrityError
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


@bp.route('/cart')
@login_required
def show_user_carts():
    carts = Cart.query.filter(Cart.customer_id == current_user.id).all()
    products = Product.query.all()
    return render_template('carts/customers_cart.html', carts=carts, products=products)


@bp.route('/cart/<int:id>')
@login_required
def remove_from_cart(id):
    cart_to_delete = Cart.query.get_or_404(id)
    try:
        db.session.delete(cart_to_delete)
        carts = Cart.query.all()
        products = Product.query.all()
        product_back_in_stock = Product.query.filter(Product.id == cart_to_delete.product_id).first()
        product_back_in_stock.stock = product_back_in_stock.stock + 1
        db.session.commit()
        flash("Product was removed from your cart")
        return render_template('carts/customers_cart.html', carts=carts, products=products)
    except IntegrityError:
        db.session.rollback()
        flash("Can't remove this product!")
        carts = Cart.query.all()
        return render_template('carts/customers_cart.html', carts=carts)










