from flask import render_template, flash, redirect, url_for
from sqlalchemy.exc import IntegrityError
from app.shipments import bp
from app.extensions import db
from app.models.shipment import Shipment
from flask_login import login_required, current_user
from app.shipments.forms import ShipmentForm

shipping_cost = 10

@bp.route('/')
def index():
    shipments = Shipment.query.all()
    return render_template('shipments/index.html', shipments=shipments)



@bp.route('/add_shipment', methods=['GET', 'POST'])
@login_required
def add_shipment():
    form = ShipmentForm()
    if form.validate_on_submit():
        shipment_created = Shipment.query.filter_by(customer_id=current_user.id).first()
        if shipment_created is None:
            shipment = Shipment(
                country=form.country.data,
                city=form.city.data,
                postal_code=form.postal_code.data,
                street=form.street.data,
                house_number=form.house_number.data,
                apartment_number=form.apartment_number.data,
                shipment_cost=shipping_cost,
                status="Created",
                customer_id=current_user.id
            )
            db.session.add(shipment)
            db.session.commit()
            flash("Shipment added successfully")
            return redirect(url_for('orders.review_order'))
        else:
            flash("This shipment already exists!")
            return redirect(url_for('shipments.edit_shipment'))
        form.country.data = ''
        form.city.data = ''
        form.postal_code.data = ''
        form.street.data = ''
        form.house_number.data = ''
        form.apartment_number.data = ''
    else:
        if form.errors:
            flash("Validation error: " + str(form.errors))

    return render_template('shipments/add_shipment.html', form=form)


@bp.route('/edit_shipment', methods=['GET', 'POST'])
@login_required
def edit_shipment():
    shipment_to_update = Shipment.query.filter_by(
        customer_id=current_user.id,
        status='Created').first()

    if shipment_to_update:
        form = ShipmentForm()
        if form.validate_on_submit():
            shipment_to_update.country = form.country.data
            shipment_to_update.city = form.city.data
            shipment_to_update.postal_code = form.postal_code.data
            shipment_to_update.street = form.street.data
            shipment_to_update.house_number = form.house_number.data
            shipment_to_update.apartment_number = form.apartment_number.data

            db.session.add(shipment_to_update)
            db.session.commit()
            flash("Shipment has been updated")
            return redirect(url_for('orders.review_order'))
        # else:
        #     flash("Fill the form")
        #     return render_template('shipments/edit_shipment.html', form=form)

        form.country.data = shipment_to_update.country
        form.city.data = shipment_to_update.city
        form.postal_code.data = shipment_to_update.postal_code
        form.street.data = shipment_to_update.street
        form.house_number.data = shipment_to_update.house_number
        form.apartment_number.data = shipment_to_update.apartment_number

        return render_template('shipments/edit_shipment.html', form=form)

    else:
        flash("Shipment cannot been updated")
        return render_template('shipments/index.html')


@bp.route('/delete_shipment/<int:id>')
@login_required
def delete_shipment(id):
    shipment_to_delete = Shipment.query.get_or_404(id)
    admin_email = current_user.email
    if admin_email == 'aglinka8@gmail.com':
        try:
            db.session.delete( shipment_to_delete)
            db.session.commit()
            flash("Shipment was deleted")
            # Grab all categories
            shipments = Shipment.query.order_by(Shipment.id)
            return render_template("shipments/index.html", shipments=shipments)

        except IntegrityError:
            db.session.rollback()
            flash("Shipment cannot be deleted!")
            shipments = Shipment.query.order_by(Shipment.id)
            return render_template("shipments/index.html", shipments=shipments)

    else:
        flash("You are not authorized to delete shipments!")
        shipments = Shipment.query.order_by(Shipment.id)
        return render_template("shipments/index.html", shipments=shipments)
