from flask_login import login_user
from werkzeug.wrappers import Response
from app import app
from flask import redirect, render_template, request 
from app.forms import UpandInForm
from app.models import User
from app import bc
from app import lm

@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Index
@app.route('/')
def index() -> str:
    return render_template('index.html')

# SignUp
@app.route('/signup', methods=['GET', 'POST'])
def signup() -> str:
    signup_form: UpandInForm = UpandInForm(request.form)

    msg: None | str = None

    if request.method == "GET":
        return render_template('signup.html', form=signup_form, msg=msg)

    if signup_form.validate():
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user:
            msg = 'User Exists!'
        else:   
            password_hash = bc.generate_password_hash(password).decode('utf-8')

            user = User(username, password_hash)

            user.save()

            msg = 'User created!'
    else:
        msg = 'Input error'

    return render_template('signup.html', form=signup_form, msg=msg)

@app.route('/signin', methods=['GET', 'POST'])
def signin() -> str | Response:
    signin_form = UpandInForm(request.form)

    msg: str | None = None

    if signin_form.validate_on_submit():

        username = request.form.get('username', '', type=str)
        password = request.form.get('password', '', type=str)

        user = User.query.filter_by(username=username).first()

        if user:
            if bc.check_password_hash(user.password, password):
                login_user(user)
                return redirect('/')
            else:
                msg = "Wrong password. Please try again"
        else:
            msg = "Unknown User!"

    return render_template('signin.html', form=signin_form, msg=msg)
