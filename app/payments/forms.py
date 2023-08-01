from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, SelectField, IntegerField
from wtforms.validators import DataRequired, InputRequired, NumberRange


class PaymentForm(FlaskForm):
    payment_method = SelectField('Select payment method',
                                 choices=['American Express',
                                          'Mastercard',
                                          'VISA',
                                          'Wire transfer'],
                                 validators=[InputRequired()])

    submit = SubmitField("Submit", validators=[DataRequired()])


class CreditCartForm(FlaskForm):
    card_number = IntegerField('Number', validators=[NumberRange(min=16, max=16, message="wrong number"),
                                                     DataRequired()])
    card_Cvv = IntegerField("CVV", validators=[NumberRange(min=4, max=4, message="wrong number"),
                                               DataRequired()])
    card_exp_month = SelectField('Exp Month',
                                 choices=['01', '02', '03', '04', '05', '06',
                                          '07', '08', '09', '10', '11', '12'],
                                 validators=[InputRequired()])

    year_to_select = [x for x in range(2023, 2050)]

    street = StringField("Street", validators=[DataRequired()])
    house_number = StringField("House number", validators=[DataRequired()])
    apartment_number = StringField("Apartment number", validators=[DataRequired()])

    submit = SubmitField("Submit", validators=[DataRequired()])