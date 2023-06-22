from flask import render_template, flash
from app.customers import bp
from app.extensions import db
from app.models.customer import Customer
from app.customers.forms import CustomerForm



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

        form.first_name.data = ''
        form.last_name.data = ''
        form.email.data = ''
        form.address.data = ''
        form.phone_number.data = ''
        flash("Account Added Successfully!")

    return render_template('customers/add_customer.html', form=form)


@bp.route('/customer/<int:id>')
def show_customer(id):
    customer = Customer.query.get_or_404(id)
    return render_template('customers/customer.html', customer=customer)


@bp.route('/categories/')
def categories():
    return render_template('customers/categories.html')
