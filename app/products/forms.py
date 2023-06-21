from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_ckeditor import CKEditorField


class AddNewProductForm(FlaskForm):
    name = StringField("Product name", validators=[DataRequired()])
    description = StringField('Product description', validators=[DataRequired()])
    price = StringField("Price", validators=[DataRequired()])
    stock = StringField("Number of product in stock", validators=[DataRequired()])
    category_id = StringField("Select Category", validators=[DataRequired()])
    submit = SubmitField("Submit", validators=[DataRequired()])
