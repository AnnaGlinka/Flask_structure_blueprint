from flask import render_template
from app.shipments import bp
from app.extensions import db
from app.models.shipment import Shipment

@bp.route('/')
def index():
    shipments = Shipment.query.all()
    return render_template('shipments/index.html', shipments=shipments)


@bp.route('/categories/')
def categories():
    return render_template('shipments/categories.html')
