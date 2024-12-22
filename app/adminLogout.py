from app import app
from flask_login import logout_user
from flask import redirect, url_for

@app.route('/logout')
def adminLogout():
    logout_user()
    return redirect(url_for('index'))