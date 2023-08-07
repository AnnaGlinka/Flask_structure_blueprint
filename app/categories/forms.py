from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField


class CategoryForm(FlaskForm):
    name = StringField("Category name", validators=[DataRequired()])
    picture = FileField("Picture")
    submit = SubmitField("Submit")
