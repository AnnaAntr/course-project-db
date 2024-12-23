from app import app
import psycopg
from app.forms import ScheduleForm
from flask import render_template, flash, redirect, url_for, abort
from app.tupleproc import tupleProc

@app.route('/schedule', methods=['GET', 'POST'])
def scheduleForm():
    with psycopg.connect(host=app.config['DB_SERVER'], user=app.config['DB_USER'], password=app.config['DB_PASSWORD'],
                         dbname=app.config['DB_NAME']) as con:
        cur = con.cursor()
        groups = tupleProc(cur.execute('SELECT group_number, group_number FROM group_tb ORDER BY group_number').fetchall())
        teachers = tupleProc(cur.execute('SELECT full_name FROM teacher ORDER BY full_name').fetchall())
        # corps = tupleProc(cur.execute('SELECT address FROM building ORDER BY address').fetchall())
        # auds = tupleProc(cur.execute('SELECT room_number FROM classroom ORDER BY room_number').fetchall())
        auds = cur.execute('SELECT building_address, room_number FROM classroom').fetchall()


    if groups is None or teachers is None or auds is None:
        abort(404)

    rooms = [(0, 'не выбрано')]
    rooms += [(i + 1, f"{item[0]}, ауд. {item[1]}") for i, item in enumerate(auds)]

    form = ScheduleForm()
    form.group.choices = groups
    form.teacher.choices = teachers
    form.aud.choices = rooms

    if form.validate_on_submit():
        if (form.group.data == 0 and form.teacher.data == 0 and form.aud.data == 0):
            flash('Выберите хотя бы один параметр', 'warning')
            return redirect(url_for('scheduleForm'))

        else:
            group = dict(form.group.choices).get(int(form.group.data))
            teacher = dict(form.teacher.choices).get(int(form.teacher.data))
            if form.aud.data != 0:
                room = dict(form.aud.choices).get(int(form.aud.data))
                r = room.split(", ауд. ")
                corp = r[0]
                aud = r[1]
            else:
                corp = 'не выбрано'
                aud = 'не выбрано'

            return redirect(url_for('scheduleShow', group=group, teacher=teacher, corp=corp, aud=aud))

    return render_template('renderForm.html', title='Параметры расписания', form=form)