from flask import render_template, flash, request
from app.customers import bp
from app.extensions import db
from app.models.customer import Customer
from app.customers.forms import CustomerForm
from sqlalchemy.exc import IntegrityError


@bp.route('/')
def index():
    customers = Customer.query.all()
    return render_template('customers/index.html', customers=customers)


@bp.route('/add', methods=['GET', 'POST'])
def add_customer():
    form = CustomerForm()
    if form.validate_on_submit():
        customer = Customer.query.filter_by(email=form.email.data).first()
        if customer is None:
            customer = Customer(first_name=form.first_name.data,
                                last_name=form.last_name.data,
                                email=form.email.data,
                                address=form.address.data,
                                phone_number=form.phone_number.data
                                )
            db.session.add(customer)
            db.session.commit()
            flash("Account Added Successfully!")

        else:
            flash("The user with this email already has an account!")

        # Clear the form
        form.first_name.data = ''
        form.last_name.data = ''
        form.email.data = ''
        form.address.data = ''
        form.phone_number.data = ''

    return render_template('customers/add_customer.html', form=form)


@bp.route('/customer/update/<int:id>', methods=['POST', 'GET'])
def update_user(id):
    form = CustomerForm()
    customer_to_update = Customer.query.get_or_404(id)
    if request.method == 'POST':
        try:
            customer_to_update.first_name = request.form['first_name']
            customer_to_update.last_name = request.form['last_name']
            customer_to_update.email = request.form['email']
            customer_to_update.address = request.form['address']
            customer_to_update.phone_number = request.form['phone_number']

            db.session.commit()
            flash("Account updated successfully!")
            return render_template("customers/update.html", form=form, customer_to_update=customer_to_update, id=id)

        except IntegrityError:
            db.session.rollback()
            flash("Error! This email already exists in the database!")
            return render_template("customers/update.html", form=form, customer_to_update=customer_to_update)

    else:
        return render_template("customers/update.html", form=form, customer_to_update=customer_to_update, id=id)


@bp.route('/customer/<int:id>')
def show_customer(id):
    customer = Customer.query.get_or_404(id)
    return render_template('customers/customer.html', customer=customer)


@bp.route('/categories/')
def categories():
    return render_template('customers/categories.html')
