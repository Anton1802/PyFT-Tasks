from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length

class UpandInForm(FlaskForm):
    username: StringField = StringField('Username', validators=[DataRequired(), Length(4, 25)])
    password: PasswordField = PasswordField('Password', validators=[DataRequired()])
    submit: SubmitField = SubmitField()
