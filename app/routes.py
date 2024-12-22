from app import app
from flask import render_template
from flask_login import current_user

@app.route('/')
def index():
    if current_user.is_authenticated:
        return render_template('index_admin.html', title='Добро пожаловать!')
    else:
        return render_template('index.html', title='Добро пожаловать!')