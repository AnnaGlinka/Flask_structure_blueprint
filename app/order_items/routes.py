from flask import render_template, flash
from app.order_items import bp
from app.extensions import db
from app.models.order_item import OrderItem
from flask_login import login_required, current_user
from sqlalchemy.exc import IntegrityError

@bp.route('/')
@login_required
def index():
    order_items = OrderItem.query.all()
    return render_template('order_items/index.html', order_items=order_items)


@bp.route('/delete_order_item/<int:id>')
@login_required
def delete_order_item(id):
    order_item_to_delete = OrderItem.query.get_or_404(id)
    admin_email = current_user.email
    if admin_email == 'aglinka8@gmail.com':
        try:
            db.session.delete(order_item_to_delete)
            db.session.commit()
            flash("Order item was deleted")
            order_items = OrderItem.query.order_by(OrderItem.id)
            return render_template("order_items/index.html", order_items=order_items)

        except IntegrityError:
            db.session.rollback()
            flash("Order item cannot be deleted!")
            order_items = OrderItem.query.order_by(OrderItem.id)
            return render_template("order_items/index.html", order_items=order_items)

    else:
        flash("You are not authorized to delete order items!")
        order_items = OrderItem.query.order_by(OrderItem.id)
        return render_template("order_items/index.html", order_items=order_items)




