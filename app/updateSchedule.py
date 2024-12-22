from app import app
from flask import render_template
import psycopg
from flask_login import login_required

@app.route('/edit/schedule/update', methods=['GET', 'POST'])
@login_required
def chooseGroupForm():
    with psycopg.connect(host=app.config['DB_SERVER'], user=app.config['DB_USER'],
                         password=app.config['DB_PASSWORD'], dbname=app.config['DB_NAME']) as con:
        cur = con.cursor()
        groups = cur.execute('SELECT group_number FROM group_tb ORDER BY group_number').fetchall()

    return render_template('updateSchedule.html', title='Редактирование расписания группы', groups=groups)