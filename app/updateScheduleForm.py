from app import app
from flask import render_template, flash, redirect, url_for, abort
import psycopg
from app.forms import UpdateScheduleForm
from app.tupleproc import tupleProc
from flask_login import login_required

@app.route('/edit/schedule/update/<group>', methods=['GET', 'POST'])
@login_required
def updateScheduleForm(group):
    with psycopg.connect(host=app.config['DB_SERVER'], user=app.config['DB_USER'], password=app.config['DB_PASSWORD'],
                         dbname=app.config['DB_NAME']) as con:
        cur = con.cursor()
        pare = cur.execute('SELECT week_type, week_day, class_number, class_course_name, '
                           'building_address, room_number, full_name '
                           'FROM group_class JOIN class '
                           'USING (week_day, class_number, week_type, room_number, building_address) '
                           'JOIN teacher ON teacher_emp_record_num = emp_record_num '
                           'JOIN day_of_week ON day = week_day '
                           'WHERE group_number = %s '
                           'ORDER BY week_type, day_number', (group,)).fetchall()
        courses = tupleProc(cur.execute('SELECT * FROM course ORDER BY name').fetchall())
        teachers = tupleProc(cur.execute('SELECT full_name FROM teacher ORDER BY full_name').fetchall())
        auds = cur.execute('SELECT building_address, room_number FROM classroom').fetchall()

    if pare is None or auds is None or courses is None or teachers is None:
        abort(404)

    rooms = [(0, 'не выбрано')]
    rooms += [(i + 1, f"{item[0]}, ауд. {item[1]}") for i, item in enumerate(auds)]

    pares = [(0, 'не выбрано')]
    pares += [(i + 1, f"{item[0]} неделя, {item[1]}, {item[2]} пара, {item[3]}, {item[4]}, {item[5]}, {item[6]}") for i, item in enumerate(pare)]

    form = UpdateScheduleForm()
    form.pare.choices = pares
    form.aud.choices = rooms
    form.course.choices = courses
    form.teacher.choices = teachers

    if form.validate_on_submit():
        if form.pare.data == 0:
            flash('Выберите пару', 'danger')
            redirect(url_for('updateScheduleForm', group=group))

        elif form.wtype.data == 0 and form.wday.data == 0 and form.num.data is None and form.aud.data == 0 and form.course.data == 0 and form.teacher.data == 0:
            flash('Заполните хотя бы одно поле', 'danger')

        else:
            wtype = dict(form.wtype.choices).get(int(form.wtype.data))
            wday = dict(form.wday.choices).get(int(form.wday.data))
            num = form.num.data or None
            course = dict(form.course.choices).get(int(form.course.data))
            teacher = dict(form.teacher.choices).get(int(form.teacher.data))
            if form.aud.data != 0:
                room = dict(form.aud.choices).get(int(form.aud.data))
                r = room.split(", ауд. ")
                corp = r[0]
                aud = r[1]

            ktype = pare[0][0]
            kday = pare[0][1]
            knum = pare[0][2]
            kaddr = pare[0][4]
            kroom = pare[0][5]

            with psycopg.connect(host=app.config['DB_SERVER'], user=app.config['DB_USER'],
                                 password=app.config['DB_PASSWORD'], dbname=app.config['DB_NAME']) as con:
                cur = con.cursor()

                if course != 'не выбрано':
                    cur.execute('UPDATE class '
                                'SET class_course_name = %s '
                                'WHERE week_type = %s AND week_day = %s AND class_number = %s '
                                'AND building_address = %s AND room_number = %s', (course, ktype, kday, knum, kaddr, kroom))

                if teacher != 'не выбрано':
                    cur.execute('UPDATE class '
                                'SET teacher_emp_record_num = '
                                '('
                                    'SELECT emp_record_num '
                                    'FROM teacher '
                                    'WHERE full_name = %s'
                                ')'
                                'WHERE week_type = %s AND week_day = %s AND class_number = %s '
                                'AND building_address = %s AND room_number = %s', (teacher, ktype, kday, knum, kaddr, kroom))

                if wtype != 'не выбрано':
                    cur.execute('UPDATE class '
                                'SET week_type = %s '
                                'WHERE week_type = %s AND week_day = %s AND class_number = %s '
                                'AND building_address = %s AND room_number = %s',
                                (wtype, ktype, kday, knum, kaddr, kroom))
                    ktype = wtype

                if wday != 'не выбрано':
                    cur.execute('UPDATE class '
                                'SET week_day = %s '
                                'WHERE week_type = %s AND week_day = %s AND class_number = %s '
                                'AND building_address = %s AND room_number = %s',
                                (wday, ktype, kday, knum, kaddr, kroom))
                    kday = wday

                if num is not None:
                    cur.execute('UPDATE class '
                                'SET class_number = %s '
                                'WHERE week_type = %s AND week_day = %s AND class_number = %s '
                                'AND building_address = %s AND room_number = %s',
                                (num, ktype, kday, knum, kaddr, kroom))
                    knum = num

                if form.aud.data != 0:
                    cur.execute('UPDATE class '
                                'SET building_address = %s, room_number = %s '
                                'WHERE week_type = %s AND week_day = %s AND class_number = %s '
                                'AND building_address = %s AND room_number = %s',
                                (corp, aud, ktype, kday, knum, kaddr, kroom))
                    kaddr = corp
                    kroom = aud

            flash('Данные успешно обновлены', 'success')
            redirect(url_for('updateScheduleForm', group=group))

    return render_template('renderForm.html', title='Редактирование существующего расписания', form=form)