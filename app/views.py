from app import app
from flask               import render_template

# Index
@app.route('/', defaults={'path': 'index.html'})
@app.route('/path')
def index(path: str) -> str:
    return render_template(path)
