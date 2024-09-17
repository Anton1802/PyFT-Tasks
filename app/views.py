from datetime import datetime
from typing import List
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.wrappers import Response
from app import app
from flask import jsonify, redirect, render_template, request, url_for 
from app.forms import UpandInForm
from app.models import Task, User
from app import bc, lm
from typing import cast


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

            msg = f"User created! <a href={url_for('signin')}>Click</a>"
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
    
    msg: str = ""
    
    user = cast(User, current_user)

    if dat_success is not None:
        dt: datetime = datetime.strptime(dat_success, '%Y-%m-%dT%H:%M')
        task_new: Task = Task(name_task, desc_task, dt, user.get_id())

        task_new.save()

        msg: str = "Task added successfully!"

    return msg 

@app.route("/mytodo/get", methods=['GET'])
@login_required
def mytodo_get():
    user = cast(User, current_user)
    tasks: List = Task.query.filter_by(user_id=user.get_id()).all()

    tasks_data = []
    for task in tasks:
        task_data = {
            "id": task.id,
            "name": task.name,
            "description": task.description,
            "dat_success": task.dat_success.isoformat(),
        }
        tasks_data.append(task_data)

    return jsonify(tasks_data)

@app.route("/logout")
@login_required
def logout() -> Response:
    logout_user()
    return redirect(url_for('index'))
