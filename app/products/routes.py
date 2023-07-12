from flask import render_template, flash, redirect, url_for
from app.products import bp
from app.extensions import db
from app.models.product import Product
from app.models.cart import Cart
from app.products.forms import ProductForm
from flask_login import login_required, current_user


@bp.route('/')
def index():
    products = Product.query.all()
    return render_template('products/index.html', products=products)


@bp.route('/add-product', methods=['GET', 'POST'])
@login_required
def add_product():
    form = ProductForm()
    if form.validate_on_submit():
        # seller = current_user.id()
        product = Product.query.filter_by(name=form.name.data).first()
        if product is None:
            product = Product(name=form.name.data,
                              description=form.description.data,
                              price=form.price.data,
                              stock=form.stock.data,
                              category_id=form.category_id.data
                              )

            db.session.add(product)
            db.session.commit()
            flash("Product Added Successfully!")

        else:
            flash("The product with the same name already exists in the database!")

        # Clear the form
        form.name.data = ''
        form.description.data = ''
        form.price.data = ''
        form.stock.data = ''
        form.category_id.data = ''

    return render_template('products/add_product.html', form=form)


@bp.route('/product/<int:id>')
def show_product(id):
    product = Product.query.get_or_404(id)
    return render_template('products/show_product.html', product=product)


@bp.route('/edit_product/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_product(id):
    product = Product.query.get_or_404(id)
    product_to_delete = Product.query.get_or_404(id)
    admin_email = current_user.email
    if admin_email == 'aglinka8@gmail.com':
        form = ProductForm()
        if form.validate_on_submit():
            product.name = form.name.data
            product.description = form.description.data
            product.price = form.price.data
            product.stock = form.stock.data
            product.category_id = form.category_id.data
            # Update Database
            db.session.add(product)
            db.session.commit()
            flash("Product has been updated")
            return redirect(url_for('products.index', id=product.id))

        form.name.data = product.name
        form.description.data = product.description
        form.price.data = product.price
        form.stock.data = product.stock
        form.category_id.data = product.category_id

        return render_template('products/edit_product.html', form=form)
    else:
        flash("You are not authorized to edit products!")
        products = Product.query.order_by(Product.id)
        return render_template("products/index.html", products=products)


@bp.route('/delete_product/<int:id>')
@login_required
def delete_product(id):
    product_to_delete = Product.query.get_or_404(id)
    admin_email = current_user.email
    if admin_email == 'aglinka8@gmail.com':
        try:
            db.session.delete(product_to_delete)
            db.session.commit()
            # Return a message
            flash("Product was deleted")
            # Grab all the products from the database
            products = Product.query.order_by(Product.id)
            return render_template("products/index.html", products=products)

        except InterruptedError:
            db.session.rollback()
            flash("There was a problem deleting this product")
            products = Product.query.order_by(Product.id)
            return render_template("products/index.html", products=products)

    else:
        flash("You are not authorized to delete products!")
        products = Product.query.order_by(Product.id)
        return render_template("products/index.html", products=products)


@bp.route('/product/add_to_cart/<int:id>', methods=['GET', 'POST'])
@login_required
def add_to_carts(id):
    product = Product.query.get_or_404(id)
    cart = Cart(quantity=1, customer_id=current_user.id, product_id=product.id)
    if product.stock > 0:
        product.stock = product.stock - 1
        db.session.add(cart)
        db.session.commit()
        flash(f"Product added to your cart: {product}")
        carts = Cart.query.filter(Cart.customer_id == current_user.id).all()
        products = Product.query.all()
        return render_template('carts/customers_cart.html', carts=carts, products=products)
    else:
        flash(f"Product {product} currently unavailable !!!")
        products = Product.query.order_by(Product.id)
        return render_template('products/index.html', products=products)



