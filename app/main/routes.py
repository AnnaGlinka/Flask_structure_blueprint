from flask import render_template
from app.main import bp
from app.products.forms import SearchProductForm


@bp.route('/')
def index():
    return render_template('base.html')

@bp.context_processor
def base():
    form = SearchProductForm()
    return dict(form=form)



