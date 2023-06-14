from flask import render_template
from app.products import bp
from app.extensions import db
from app.models.product import Product

@bp.route('/')
def index():
    products = Product.query.all()
    return render_template('products/index.html', products=products)


@bp.route('/categories/')
def categories():
    return render_template('products/categories.html')
