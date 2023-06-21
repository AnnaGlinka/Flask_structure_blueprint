from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class CustomerForm(FlaskForm):
    first_name = StringField("First name", validators=[DataRequired()])
    last_name = StringField('Last name', validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    address = StringField("Address", validators=[DataRequired()])
    phone_number = StringField("Phone", validators=[DataRequired()])
    submit = SubmitField("Submit", validators=[DataRequired()])
