from flask import Blueprint

bp = Blueprint('order_items', __name__)


from app.order_items import routes