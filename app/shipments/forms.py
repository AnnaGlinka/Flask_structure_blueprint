from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, SelectField
from wtforms.validators import DataRequired, InputRequired


class ShipmentForm(FlaskForm):
    country = StringField("Country", validators=[DataRequired()])
    city = StringField("City", validators=[DataRequired()])
    postal_code = StringField("Postal code", validators=[DataRequired()])
    street = StringField("Street", validators=[DataRequired()])
    house_number = StringField("House number", validators=[DataRequired()])
    apartment_number = StringField("Apartment number", validators=[DataRequired()])

    submit = SubmitField("Submit", validators=[DataRequired()])
