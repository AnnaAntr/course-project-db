from app import app
from flask import render_template
from flask_login import login_required

@app.get('/edit/schedule')
@login_required
def editSchedule():
    return render_template('editSchedule.html', title='Управление расписанием')