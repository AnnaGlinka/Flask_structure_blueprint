from flask import render_template
from app.products import bp
from app.extensions import db
from app.models.product import Product
from app.products.forms import AddNewProductForm

@bp.route('/')
def index():
    products = Product.query.all()
    return render_template('products/index.html', products=products)


@bp.route('/add-product', methods=['GET', 'POST'])
def add_product():
    form = AddNewProductForm()
    if form.validate_on_submit():
        # seller = current_user.id()
        product = Product(name=form.name.data,
                          description=form.description.data,
                          price=form.price.data,
                          stock=form.stock.data,
                          category_id=form.category_id.data
                          )
        # Clear the form
        form.name.data = ''
        form.description.data = ''
        form.price.data = ''
        form.stock.data = ''
        form.category_id.data = ''

        db.session.add(product)
        db.session.commit()

    return render_template('products/add_product.html', form=form)


@bp.route('/product/<int:id>')
def show_product(id):
    product = Product.query.get_or_404(id)
    return render_template('products/product.html', product=product)



@bp.route('/categories/')
def categories():
    return render_template('products/categories.html')
