from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField
from flask_ckeditor import CKEditorField


class CategoryForm(FlaskForm):
    name = StringField("Category name", validators=[DataRequired()])
    description = CKEditorField('Description')
    picture = FileField("Picture")
    submit = SubmitField("Submit", validators=[DataRequired()])
