from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, TextAreaField, IntegerField, SelectField, DecimalField, SubmitField, PasswordField
from wtforms.validators import DataRequired, NumberRange, InputRequired, Email, EqualTo, Length

class PropertyForm(FlaskForm):
    title = StringField('Property Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    bedrooms = IntegerField('No. of Bedrooms', validators=[DataRequired(), NumberRange(min=1, max=10)])
    bathrooms = IntegerField('No. of Bathrooms', validators=[DataRequired(), NumberRange(min=1, max=10)])
    location = StringField('Location', validators=[DataRequired()])
    price = DecimalField('Price', validators=[DataRequired()], places=2)
    property_type = SelectField('Property Type',
                               choices=[('House', 'House'), ('Apartment', 'Apartment')],
                               validators=[InputRequired()])
    photo = FileField('Photo', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only!')
    ])
    submit = SubmitField('Add Property')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')