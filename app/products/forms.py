from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, SelectField
from wtforms.validators import DataRequired, InputRequired
from app.models.category import Category


class ProductForm(FlaskForm):
    name = StringField("Product name", validators=[DataRequired()])
    description = StringField('Product description', validators=[DataRequired()])
    price = StringField("Price", validators=[DataRequired()])
    stock = StringField("Number of product in stock", validators=[DataRequired()])
    category_id = SelectField('Category', validators=[InputRequired()])

    def __init__(self):
        super(ProductForm, self).__init__()
        self.category_id.choices = [(c.id, c.name) for c in Category.query.all()]
    submit = SubmitField("Submit", validators=[DataRequired()])


class SearchProductForm(FlaskForm):
    searched = StringField("Searched", validators=[DataRequired()])
    submit = SubmitField("Submit")
