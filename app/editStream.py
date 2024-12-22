from app import app
from flask import render_template
from flask_login import login_required

@app.get('/edit/stream')
@login_required
def editStream():
    return render_template('editStream.html', title='Управление потоками')