from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length

class UpandInForm(FlaskForm):
    username: StringField = StringField('Username', validators=[DataRequired(), Length(1, 20)])
    password: PasswordField = PasswordField('Password', validators=[DataRequired(), Length(8, 150)])
    submit: SubmitField = SubmitField()
