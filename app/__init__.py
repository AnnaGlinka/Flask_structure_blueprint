from flask import Flask

from config import Config
from app.extensions import db

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions here
    db.init_app(app)

    # Register blueprints here
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.posts import bp as posts_bp
    app.register_blueprint(posts_bp, url_prefix='/posts')

    from app.questions import bp as questions_bp
    app.register_blueprint(questions_bp, url_prefix='/questions')

    from app.products import bp as products_bp
    app.register_blueprint(products_bp, url_prefix='/products')

    from app.customers import bp as customers_bp
    app.register_blueprint(customers_bp, url_prefix='/customers')

    from app.orders import bp as orders_bp
    app.register_blueprint(orders_bp, url_prefix='/orders')

    from app.categories import bp as categories_bp
    app.register_blueprint(categories_bp, url_prefix='/categories')

    from app.order_items import bp as order_items_bp
    app.register_blueprint(order_items_bp, url_prefix='/order_items')

    from app.payments import bp as payments_bp
    app.register_blueprint(payments_bp, url_prefix='/payments')

    from app.shipments import bp as shipments_bp
    app.register_blueprint(shipments_bp, url_prefix='/shipments')

    from app.carts import bp as carts_bp
    app.register_blueprint(carts_bp, url_prefix='/carts')

    @app.route('/test/')
    def test_page():
        return '<h1>Testing the Flask Application Factory Pattern</h1>'

    return app