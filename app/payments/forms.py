from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, SelectField, IntegerField
from wtforms.validators import DataRequired, InputRequired, NumberRange, Regexp


class PaymentForm(FlaskForm):
    payment_method = SelectField('Select payment method',
                                 choices=['American Express',
                                          'Mastercard',
                                          'VISA',
                                          'Wire transfer'],
                                 validators=[InputRequired()])

    submit = SubmitField("Submit", validators=[DataRequired()])


class CreditCartForm(FlaskForm):
    # https://www.makeuseof.com/regex-validate-credit-card-numbers/
    # Visa - valid 4539890694174109
    number_reg = "4[0-9]{12}(?:[0-9]{3})?$"
    card_number = StringField('Number', validators=[DataRequired(), Regexp(number_reg,
                                                                           message="wrong credit card number")])
    card_Cvv = StringField("CVV", validators=[DataRequired(), Regexp('^[0-9]{3,4}$', message="wrong CVV card number")])
    card_exp_month = SelectField('Exp Month',
                                 choices=['01', '02', '03', '04', '05', '06',
                                          '07', '08', '09', '10', '11', '12'],
                                 validators=[InputRequired()])

    year_to_select = [x for x in range(2023, 2050)]
    card_exp_year = SelectField('Exp Year', choices=year_to_select, validators=[InputRequired()])

    submit = SubmitField("Submit", validators=[DataRequired()])
