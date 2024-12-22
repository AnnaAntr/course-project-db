from app import app
from flask import render_template
from flask_login import login_required

@app.get('/edit/edplan')
@login_required
def editEdPlan():
    return render_template('editEdplan.html', title='Управление учебным планом')