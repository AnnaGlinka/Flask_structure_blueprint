from flask import render_template
from app.contacts import bp


@bp.route('/')
def contact_us():

    return render_template('contact/contact_us.html')
