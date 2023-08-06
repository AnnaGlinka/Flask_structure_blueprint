from flask import Flask
from flask_login import LoginManager

from config import Config
from app.extensions import db
from app.models.customer import Customer


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions here
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'customers.login'

    @login_manager.user_loader
    def load_user(customer_id):
        return Customer.query.get(int(customer_id))

    # Register blueprints here
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.posts import bp as posts_bp
    app.register_blueprint(posts_bp, url_prefix='/posts')

    from app.contacts import bp as contacts_bp
    app.register_blueprint(contacts_bp, url_prefix='/contacts')

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