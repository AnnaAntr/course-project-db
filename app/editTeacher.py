from app import app
from flask import render_template
from flask_login import login_required

@app.get('/edit/teacher')
@login_required
def editTeacher():
    return render_template('editTeacher.html', title='Управление преподавателями')