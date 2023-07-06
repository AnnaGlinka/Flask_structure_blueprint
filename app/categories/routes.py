
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


@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_category(id):
    category = Category.query.get_or_404(id)
    form = CategoryForm()
    if form.validate_on_submit():
        category.name = form.name.data
        # Update Database
        db.session.add(category)
        db.session.commit()
        flash("Category has been updated")
        return redirect(url_for('categories.index', id=category.id))

    form.name.data = category.name
    return render_template('categories/edit_category.html', form=form)

@bp.route('/delete/<int:id>')
@login_required
def delete_category(id):
    category_to_delete = Category.query.get_or_404(id)

    try:
        db.session.delete(category_to_delete)
        db.session.commit()
        flash("Category was deleted")
        # Grab all categories
        categories = Category.query.order_by(Category.id)
        return render_template("categories/index.html", categories=categories)

    except:
        flash("There was a problem deleting posts, try again")
        categories = Category.query.order_by(Category.id)
        return render_template("categories/index.html", categories=categories)




