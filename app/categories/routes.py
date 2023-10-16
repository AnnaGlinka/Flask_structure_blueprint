
from flask import render_template, flash, redirect, url_for, request
from sqlalchemy.exc import IntegrityError

import app
from app.categories import bp
from app.extensions import db
from app.models.category import Category
from app.categories.forms import CategoryForm
from app.products.forms import SearchProductForm
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import uuid as uuid
import os


@bp.route('/')
def index():
    categories = Category.query.all()
    return render_template('categories/index.html', categories=categories)

@bp.context_processor
def base():
    form = SearchProductForm()
    return dict(form=form)


@bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_category():
    form = CategoryForm()
    if form.validate_on_submit():
        category = Category.query.filter_by(name=form.name.data).first()
        if category is None:
            category = Category(name=form.name.data, description=form.description.data)

            category.picture = request.files['picture']
            # get image name
            pic_filename = secure_filename(category.picture.filename)
            pic_name = str(uuid.uuid1()) + "_" + pic_filename
            saver = request.files['picture']
            # save the image

            category.picture = pic_name
            db.session.add(category)
            db.session.commit()
            saver.save(os.path.join("app/static/images/", pic_name))
            flash("Category added successfully")
            return redirect(url_for('categories.index'))
        else:
            flash("This category already exists!")
        form.name.data = ''
        form.description.data = ''

    else:
        if form.errors:
            flash("Validation error: " + str(form.errors))

    return render_template('categories/add_category.html', form=form)


@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_category(id):
    admin_email = current_user.email
    if admin_email == 'aglinka8@gmail.com':
        category = Category.query.get_or_404(id)
        form = CategoryForm()
        if form.validate_on_submit():
            category.name = form.name.data
            category.description = form.description.data

            db.session.commit()

            flash("Category has been updated")
            return redirect(url_for('categories.index', id=category.id))

        form.name.data = category.name
        form.description.data = category.description

        return render_template('categories/edit_category.html', form=form)
    else:
        flash("You are not authorized to edit categories!")
        categories = Category.query.order_by(Category.id)
        return render_template("categories/index.html", categories=categories)

@bp.route('/edit_picture/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_category_picture(id):
    admin_email = current_user.email
    if admin_email == 'aglinka8@gmail.com':
        category = Category.query.get_or_404(id)
        form = CategoryForm()
        if form.validate_on_submit():
            category.name = form.name.data
            category.picture = request.files['picture']
            # get image name
            pic_filename = secure_filename(category.picture.filename)
            pic_name = str(uuid.uuid1()) + "_" + pic_filename
            saver = request.files['picture']
            # save the image

            category.picture = pic_name
            db.session.commit()

            saver.save(os.path.join("app/static/images/", pic_name))
            flash("Category has been updated")
            return redirect(url_for('categories.index', id=category.id))

        form.name.data = category.name
        return render_template('categories/edit_category_picture.html', form=form)
    else:
        flash("You are not authorized to edit categories!")
        categories = Category.query.order_by(Category.id)
        return render_template("categories/index.html", categories=categories)



@bp.route('/delete/<int:id>')
@login_required
def delete_category(id):
    category_to_delete = Category.query.get_or_404(id)
    admin_email = current_user.email
    if admin_email == 'aglinka8@gmail.com':

        try:
            db.session.delete(category_to_delete)
            db.session.commit()
            flash("Category was deleted")
            # Grab all categories
            categories = Category.query.order_by(Category.id)
            return render_template("categories/index.html", categories=categories)

        except IntegrityError:
            db.session.rollback()
            flash("The category that is uses in Products cannot be deleted!")
            categories = Category.query.order_by(Category.id)
            return render_template("categories/index.html", categories=categories)

    else:
        flash("You are not authorized to delete categories!")
        categories = Category.query.order_by(Category.id)
        return render_template("categories/index.html", categories=categories)





