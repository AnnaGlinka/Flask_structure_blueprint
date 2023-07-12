from flask import render_template, flash, request, redirect, url_for
from app.customers import bp
from app.extensions import db
from app.models.customer import Customer
from app.models.cart import Cart
from app.customers.forms import CustomerForm
from app.customers.forms import PasswordForm
from app.customers.forms import LoginForm
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user


@bp.route('/')
@login_required
def index():
    customers = Customer.query.all()
    return render_template('customers/index.html', customers=customers)


@bp.route('/add', methods=['GET', 'POST'])
def customer_create():
    form = CustomerForm()
    if form.validate_on_submit():
        customer = Customer.query.filter_by(email=form.email.data).first()
        if customer is None:
            # hash the pw
            hashed_pw = generate_password_hash(form.password_hash.data, "sha256")
            customer = Customer(first_name=form.first_name.data,
                                last_name=form.last_name.data,
                                email=form.email.data,
                                address=form.address.data,
                                phone_number=form.phone_number.data,
                                password_hash=hashed_pw
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
        form.password_hash.data = ''

    else:
        if form.errors:
            flash("Validation error: " + str(form.errors))
    return render_template('customers/customer_create.html', form=form)


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


@bp.route('/customer/delete/<int:id>')
def delete_customer(id):
    customer_to_delete = Customer.query.get_or_404(id)

    try:
        db.session.delete(customer_to_delete)
        db.session.commit()
        # Return a message
        flash("Customer was deleted")
        # Grab all the posts from the database
        customers = Customer.query.order_by(Customer.id)
        return render_template("customers/index.html", customers=customers)

    except:

        # Return an error message
        flash("There was a problem deleting this customer, try again")

        # Grab all customers from the database
        customers = Customer.query.order_by(Customer.id)
        return render_template("customers/index.html", customers=customers)


@bp.route('/test_pw', methods=['GET', 'POST'])
def test_pw():
    email = None
    password = None
    pw_to_check = None
    passed = None
    form = PasswordForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password_hash.data
        # Clear the form
        form.email.data = ''
        form.password_hash.data = ''

        # find customer by email address
        pw_to_check = Customer.query.filter_by(email=email).first()

        # Check Hashed Passwrod
        passed = check_password_hash(pw_to_check.password_hash, password)

    return render_template('customers/test_pw.html',
                           email=email,
                           password=password,
                           pw_to_check=pw_to_check,
                           passed=passed,
                           form=form)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        customer = Customer.query.filter_by(email=form.email.data).first()
        if customer:
            if check_password_hash(customer.password_hash, form.password.data):
                login_user(customer)
                flash("Login successful")
                return redirect(url_for('customers.user_profile'))
            else:
                flash("Wrong password!")
        else:
            flash("That email doesn't exist in the database")
    return render_template('customers/login.html', form=form)


@bp.route('/user_profile', methods=['GET', 'POST'])
@login_required
def user_profile():
    return render_template("customers/user_profile.html")


@bp.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash("You have been logged out!")
    return redirect(url_for('customers.login'))


@bp.route('/categories/')
def categories():
    return render_template('customers/categories.html')
