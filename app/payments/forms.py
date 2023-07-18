from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, SelectField
from wtforms.validators import DataRequired, InputRequired


class PaymentForm(FlaskForm):
    payment_method = SelectField('Select payment method',
                                 choices=['American Express',
                                          'Apple Pay',
                                          'Mastercard',
                                          'PyuPal',
                                          'VISA',
                                          'Wire transfer'],
                                 validators=[InputRequired()])

    submit = SubmitField("Submit", validators=[DataRequired()])

