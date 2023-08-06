from flask import render_template
from app.contacts import bp


@bp.route('/')
def contact_us():
    return render_template('contact/contact_us.html')


@bp.route('/delivery_and_return_info')
def delivery_and_return():
    return render_template('contact/delivery_and_return_info.html')
