from app import app
from flask import render_template

# Index
@app.route('/')
def index() -> str:
    return render_template('index.html')

# SignIn
@app.route('/signin')
def signin() -> str:
    return render_template('signin.html')

# SignUp
@app.route('/signup')
def signup() -> str:
    return render_template('signup.html')
