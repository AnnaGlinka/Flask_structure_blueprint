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
    shipment_created = Shipment.query.filter_by(customer_id=current_user.id, status='Created').first()
    if not shipment_created:
        if form.validate_on_submit():
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
            flash("New shipment added successfully")

        else:
            flash("Please fill the form")

        # Clear the form
        form.country.data = ''
        form.city.data = ''
        form.postal_code.data = ''
        form.street.data = ''
        form.house_number.data = ''
        form.apartment_number.data = ''
        #return render_template('shipments/add_shipment.html', form=form)
        return redirect(url_for('orders.create_order'))

    else:
        flash("The shipment is already created")
        return redirect(url_for('shipments.edit_shipment'))


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
            shipment_to_update.house_number = form.house_number.data
            shipment_to_update.apartment_number = form.apartment_number.data

            db.session.add(shipment_to_update)
            db.session.commit()
            flash("Shipment has been updated")
            return render_template('shipments/edit_shipment.html', form=form)
        else:
            flash("Fill the form")
            return render_template('shipments/edit_shipment.html', form=form)

        shipment_to_update.country = form.country.data
        shipment_to_update.city = form.city.data
        shipment_to_update.postal_code = form.postal_code.data
        shipment_to_update.house_number = form.house_number.data
        shipment_to_update.apartment_number = form.apartment_number.data
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
