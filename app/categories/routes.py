
from flask import render_template, flash, redirect, url_for
from app.categories import bp
from app.extensions import db
from app.models.category import Category
from app.categories.forms import CategoryForm
from flask_login import login_required


@bp.route('/')
def index():
    categories = Category.query.all()
    return render_template('categories/index.html', categories=categories)


@bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_category():
    form = CategoryForm()
    if form.validate_on_submit():
        category = Category.query.filter_by(name=form.name.data).first()
        if category is None:
            category = Category(name=form.name.data)
            db.session.add(category)
            db.session.commit()
            flash("Category added successfully")
            return redirect(url_for('categories.index'))
        else:
            flash("This category already exists!")
        form.name.data = ''
    else:
        if form.errors:
            flash("Validation error: " + str(form.errors))

    return render_template('categories/add_category.html', form=form)


