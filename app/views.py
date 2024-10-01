from datetime import datetime
from typing import List
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.wrappers import Response
from app import app
from flask import jsonify, redirect, render_template, request, url_for 
from app.forms import UpandInForm
from app.models import Task, User, Notice
from app import bc, lm, bgs
from typing import cast
from app.util import send_message
from apscheduler.schedulers import SchedulerAlreadyRunningError


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

@lm.unauthorized_handler     
def unauthorized_callback():            
       return redirect(url_for('signin'))

@app.route("/mytodo")
@login_required
def mytodo() -> str:
    return render_template('mytodo.html')

# MyTodo-ADD(POST)
@app.route("/mytodo/add", methods=['POST'])
@login_required
def mytodo_add():
    data = request.get_json()
    
    user = cast(User, current_user)

    if data['dat_success'] is not None:
        try:
            dt: datetime = datetime.strptime(data['dat_success'], '%Y-%m-%dT%H:%M')
            task_new: Task = Task(data['name_task'], data['desc_task'], dt, user.get_id())
            task_new.save()
        except ValueError:
            return jsonify({"message": "Enter the time according to the format!"})

    return jsonify({"message": "Task added successfully!"})

# Mytodo-GET(GET)
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

#Mytodo-Del(DELETE)
@app.route('/mytodo/del/<int:task_id>', methods=['DELETE'])
@login_required
def mytodo_del(task_id):
    user_id = cast(User, current_user).get_id()
    task = Task.query.filter_by(id=task_id).first()
    if task is not None:
        if int(task.user_id) == int(user_id):
            task.delete()
        else:
            return jsonify({"message": "Don't have access!"}), 406
    
    return jsonify({"message": "Success!"}), 200

#Mytodo-Edit(PUT)
@app.route('/mytodo/edit/<int:task_id>', methods=['PUT'])
@login_required
def mytodo_edit(task_id):
    user_id = cast(User, current_user).get_id()
    data = request.get_json()
    task = Task.query.filter_by(id=task_id).first()
    if task is not None:
        if int(task.user_id) == int(user_id):
            task.update(
                data['name_task'], 
                data['description_task'], 
                datetime.strptime(data['dat_task'], "%Y-%m-%dT%H:%M"),
                user_id,
            )
        else:
            return jsonify({"message": "Don't have access!"}), 406

    return jsonify({'message': "Success"}), 200

#Mytodo-Notice-Start(POST)
@app.route('/mytodo/notice/start', methods=["POST"])
@login_required
def mytodo_notice_start():
    user = cast(User, current_user)
    tasks: List = Task.query.filter_by(user_id=user.get_id()).all()

    if len(tasks) == 0:
        return jsonify({"message": "No tasks!"})

    data = request.get_json()
    user_id = int(user.get_id())

    notice_config = Notice.query.filter_by(user_id=user_id).first()

    if notice_config is None:
        notice_config = Notice(data['chat_id'], data['interval'], user_id)
        notice_config.save()
    else:
        notice_config.update(data['chat_id'], data['interval'], user_id)
        
    jobs = bgs.get_jobs()
    for job in jobs:
        if int(job.name) == int(user_id):
            job.pause()
            job.remove()    

    for task in tasks:
        message = (
            f"*📝 Task Name:* {task.name}\n"
            f"*📝 Task Description:* \n{task.description}\n\n"
            f"*⏰ Execution Time:* {task.dat_success}"
        )      

        bgs.add_job(
            send_message, 
            'interval', 
            minutes=int(notice_config.interval), 
            args=[message, notice_config.chat_id], 
            name=str(user_id),
        )

    return jsonify({"message": "Notice started!"})

#Mytodo-Notice-Stop(DELETE)
@app.route('/mytodo/notice/stop', methods=["DELETE"])
@login_required
def mytodo_notice_stop():
    user = cast(User, current_user)
    user_id = user.get_id()
    jobs = bgs.get_jobs()
    for job in jobs:
        if int(job.name) == int(user_id):
            job.pause()
            job.remove()

    return jsonify({"message": "Notice stopped!"})

#Mytodo-Notice-Get(GET)
@app.route('/mytodo/notice/get', methods=['GET'])
@login_required
def mytodo_notice_get():
    user = cast(User, current_user)

    notice_config = Notice.query.filter_by(user_id=user.get_id()).first()
    if notice_config is None:
        return jsonify({
            "chat_id": "",
            "interval": "",
        })
    else:
        return jsonify({
            "chat_id": notice_config.chat_id,
            "interval": notice_config.interval,
        })

@app.route('/mytodo/notice/get_jobs', methods=['GET'])
@login_required
def mytodo_notice_get_jobs():
    user = cast(User, current_user)
    jobs = bgs.get_jobs()

    jobs_user = []
    for job in jobs:
        if int(job.name) == int(user.get_id()):
            jobs_user.append({
                "id": job.id,
                "name": job.name, 
            })

    return jsonify(jobs_user)

@app.route("/logout")
@login_required
def logout() -> Response:
    logout_user()
    return redirect(url_for('index'))
