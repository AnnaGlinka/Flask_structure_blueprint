from flask import render_template, flash, redirect, url_for
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
        total += (products[cart.product_id - 1].price * cart.quantity)
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


@bp.route('/cart/reduce_quantity/<int:id>')
@login_required
def reduce_quantity(id):
    cart_to_update = Cart.query.get_or_404(id)
    product = Product.query.filter_by(id=cart_to_update.product_id).first()

    if cart_to_update.quantity > 1:
        product.stock += 1
        cart_to_update.quantity -= 1
        db.session.commit()
        flash(f"An item of {product} was removed")
        carts = Cart.query.filter(Cart.customer_id == current_user.id).all()
        products = Product.query.all()
        total = update_total(carts, products)
        return render_template('carts/customers_cart.html', carts=carts, products=products, total=total)
    else:
        return redirect(url_for('carts.remove_from_cart', id=cart_to_update.id))



@bp.route('/delete_cart/<int:id>')
@login_required
def delete_cart(id):
    cart_to_delete = Cart.query.get_or_404(id)
    admin_email = current_user.email
    if admin_email == 'aglinka8@gmail.com':

        try:
            db.session.delete(cart_to_delete)
            db.session.commit()
            flash("Cart was deleted")
            carts = Cart.query.order_by(Cart.id)
            return render_template("carts/index.html", carts=carts)

        except IntegrityError:
            db.session.rollback()
            flash("The cart cannot be deleted!")
            carts = Cart.query.order_by(Cart.id)
            return render_template("carts/index.html", carts=carts)

    else:
        flash("You are not authorized to delete carts!")
        carts = Cart.query.order_by(Cart.id)
        return render_template("carts/index.html", carts=carts)






