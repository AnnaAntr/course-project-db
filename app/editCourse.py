from app import app
from flask import render_template
from flask_login import login_required

@app.get('/edit/course')
@login_required
def editCourse():
    return render_template('editCourse.html', title='Управление предметами')