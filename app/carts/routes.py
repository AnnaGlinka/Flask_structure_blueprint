from flask import render_template, flash
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import functions
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


def update_total(carts, products):
    total = 0
    for cart in carts:
        total += products[cart.product_id - 1].price
    return total


@bp.route('/cart')
@login_required
def show_user_carts():
    carts = Cart.query.filter(Cart.customer_id == current_user.id).all()
    products = Product.query.all()
    total = update_total(carts, products)

    return render_template('carts/customers_cart.html', carts=carts, products=products, total=total)


@bp.route('/cart/<int:id>')
@login_required
def remove_from_cart(id):
    cart_to_delete = Cart.query.get_or_404(id)
    try:
        db.session.delete(cart_to_delete)
        carts = Cart.query.filter(Cart.customer_id == current_user.id).all()
        products = Product.query.all()
        total = update_total(carts, products)
        product_back_in_stock = Product.query.filter(Product.id == cart_to_delete.product_id).first()
        product_back_in_stock.stock = product_back_in_stock.stock + cart_to_delete.quantity
        db.session.commit()
        flash("Product was removed from your cart")
        return render_template('carts/customers_cart.html', carts=carts, products=products, total=total)
    except IntegrityError:
        db.session.rollback()
        flash("Can't remove this product!")
        carts = Cart.query.all()
        return render_template('carts/customers_cart.html', carts=carts)



@bp.route('/cart/add/<int:id>')
@login_required
def add_the_same(id):
    cart_to_update = Cart.query.get_or_404(id)
    product = Product.query.filter_by(id=cart_to_update.product_id).first()


    if product.stock > 0:
        product.stock -= 1
        cart_to_update.quantity += 1
        db.session.commit()
        flash(f"Another item of {product} added to your cat")
        carts = Cart.query.filter(Cart.customer_id == current_user.id).all()
        products = Product.query.all()
        total = update_total(carts, products)
        return render_template('carts/customers_cart.html', carts=carts, products=products, total=total)
    else:
        flash(f"Product {product} currently unavailable !!!")
        products = Product.query.order_by(Product.id)
        carts = Cart.query.filter(Cart.customer_id == current_user.id).all()
        total = update_total(carts, products)
        return render_template('carts/customers_cart.html', carts=carts, products=products, total=total)







