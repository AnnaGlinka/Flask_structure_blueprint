from flask import render_template
from app.carts import bp
from app.extensions import db
from app.models.cart import Cart

@bp.route('/')
def index():
    carts = Cart.query.all()
    return render_template('carts/index.html', carts=carts)


@bp.route('/categories/')
def categories():
    return render_template('carts/categories.html')
