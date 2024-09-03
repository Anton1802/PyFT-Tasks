from flask_wtf import Form
from app import app
from flask import render_template, request
from app.forms import UpandInForm
from app.models import User
from app import bc

# Index
@app.route('/')
def index() -> str:
    return render_template('index.html')

# SignUp
@app.route('/signup', methods=['GET', 'POST'])
def signup() -> str:
    signup_form: Form = UpandInForm(request.form)

    msg: None | str = None
    success: bool = False

    if request.method == "GET":
        return render_template('signup.html', form=signup_form, msg=msg)

    if signup_form.validate():
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user:
            msg = 'User Exists!'
        else:   
            password_hash = bc.generate_password_hash(password)

            user = User(username, password_hash)

            user.save()

            msg = 'User created!'
            success = True
    else:
        msg = 'Input error'

    return render_template('signup.html', form=signup_form, msg=msg)


