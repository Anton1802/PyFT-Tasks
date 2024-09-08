from datetime import datetime
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.wrappers import Response
from app import app
from flask import redirect, render_template, request, url_for 
from app.forms import UpandInForm
from app.models import Task, User
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
def signup() -> str | Response:
    if getattr(current_user, 'is_authenticated', False):
        return redirect(url_for('index'))

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

# SignIn
@app.route('/signin', methods=['GET', 'POST'])
def signin() -> str | Response:
    if getattr(current_user, 'is_authenticated', False):
        return redirect(url_for('index'))

    signin_form = UpandInForm(request.form)

    msg: str | None = None

    if signin_form.validate_on_submit():

        username = request.form.get('username', '', type=str)
        password = request.form.get('password', '', type=str)

        user = User.query.filter_by(username=username).first()

        if user:
            if bc.check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('index'))
            else:
                msg = "Wrong password. Please try again"
        else:
            msg = "Unknown User!"

    return render_template('signin.html', form=signin_form, msg=msg)

@app.route("/mytodo")
@login_required
def mytodo() -> str:
    return render_template('mytodo.html')

@app.route("/mytodo/add", methods=['POST'])
@login_required
def mytodo_add():
    name_task: str | None = request.form.get('name-task')
    desc_task: str | None = request.form.get('desc-task')
    dat_success: str | None = request.form.get('dat-succes')
    
    msg = None

    if dat_success is not None:
        dt: datetime = datetime.strptime(dat_success, '%Y-%m-%dT%H:%M')
        task_new: Task = Task(name_task, desc_task, dt, current_user.get_id())

        task_new.save()

        msg = "Task added successfully!"

    return msg

@app.route("/logout")
@login_required
def logout() -> Response:
    logout_user()
    return redirect(url_for('index'))
