from app import app
from flask import render_template
from flask_login import login_required

@app.get('/edit/group')
@login_required
def editGroup():
    return render_template('editGroup.html', title='Управление группами')