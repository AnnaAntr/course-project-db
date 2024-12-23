from app import app
from flask import render_template, flash, redirect, url_for, abort
import psycopg
from app.forms import InsertScheduleForm
from app.tupleproc import tupleProc
from flask_login import login_required

@app.route('/edit/schedule/insert', methods=['GET', 'POST'])
@login_required
def insertScheduleForm():
    with psycopg.connect(host=app.config['DB_SERVER'], user=app.config['DB_USER'], password=app.config['DB_PASSWORD'],
                         dbname=app.config['DB_NAME']) as con:
        cur = con.cursor()
        groups = tupleProc(cur.execute('SELECT group_number FROM group_tb ORDER BY group_number').fetchall())
        auds = cur.execute('SELECT building_address, room_number FROM classroom').fetchall()
        courses = tupleProc(cur.execute('SELECT name FROM course ORDER BY name').fetchall())
        teachers = tupleProc(cur.execute('SELECT full_name FROM teacher ORDER BY full_name').fetchall())
        schedule = cur.execute('SELECT group_number, week_type, week_day, class_number, '
                               'building_address, room_number, class_course_name, full_name '
                               'FROM group_class JOIN class '
                               'USING (week_day, class_number, week_type, room_number, building_address) '
                               'JOIN teacher ON emp_record_num = teacher_emp_record_num'). fetchall()

    if groups is None or auds is None or courses is None or teachers is None:
        abort(404)

    rooms = [(0, 'не выбрано')]
    rooms += [(i + 1, f"{item[0]}, ауд. {item[1]}") for i, item in enumerate(auds)]

    form = InsertScheduleForm()
    form.group.choices = groups
    form.aud.choices = rooms
    form.course.choices = courses
    form.teacher.choices = teachers

    if form.validate_on_submit():
        if form.group.data == 0 or form.wtype.data == 0 or form.wday.data == 0 or form.aud.data == 0 or form.course.data == 0 or form.teacher.data == 0:
            flash('Все поля должны быть заполнены', 'danger')
            return redirect(url_for('insertScheduleForm'))

        else:
            gr = dict(form.group.choices).get(int(form.group.data))
            wtype = dict(form.wtype.choices).get(int(form.wtype.data))
            wday = dict(form.wday.choices).get(int(form.wday.data))
            num = form.num.data
            course = dict(form.course.choices).get(int(form.course.data))
            teacher = dict(form.teacher.choices).get(int(form.teacher.data))
            if form.aud.data != 0:
                room = dict(form.aud.choices).get(int(form.aud.data))
                r = room.split(", ауд. ")
                corp = r[0]
                aud = r[1]

            sch = (gr, wtype, wday, num, corp, aud, course, teacher,)

            if schedule is not None and sch in schedule:
                flash('Пара с такими параметрами уже существует', 'danger')
                return redirect(url_for('insertScheduleForm'))

            else:
                with psycopg.connect(host=app.config['DB_SERVER'], user=app.config['DB_USER'],
                                     password=app.config['DB_PASSWORD'], dbname=app.config['DB_NAME']) as con:
                    cur = con.cursor()
                    emp_rec = cur.execute('SELECT emp_record_num FROM teacher WHERE full_name = %s', (teacher,)).fetchone()
                    cur.execute('INSERT INTO class VALUES (%s, %s, %s, %s, %s, %s, %s)', (wday, num, wtype, aud, corp, course, emp_rec[0]))
                    cur.execute('INSERT INTO group_class VALUES (%s, %s, %s, %s, %s, %s)', (gr, wday, num, wtype, aud, corp))

                flash('Данные успешно обновлены', 'success')
                redirect(url_for('insertScheduleForm'))

    return render_template('renderForm.html', title='Добавление нового расписания', form=form)