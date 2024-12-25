from app import app
from app.forms import UpdateTeacherForm
from flask import render_template, flash, redirect, url_for, abort
import psycopg
from app.tupleproc import tupleProc
from flask_login import login_required

@app.route('/edit/teacher/update', methods=['GET', 'POST'])
@login_required
def updateTeacherForm():
    with psycopg.connect(host=app.config['DB_SERVER'], user=app.config['DB_USER'], password=app.config['DB_PASSWORD'],
                         dbname=app.config['DB_NAME']) as con:
        cur = con.cursor()
        teachers = tupleProc(cur.execute('SELECT full_name FROM teacher ORDER BY full_name').fetchall())
        deps = tupleProc(cur.execute('SELECT dep_number FROM department ORDER BY dep_number').fetchall())

    if teachers is None or deps is None:
        abort(404)

    form = UpdateTeacherForm()
    form.name.choices = teachers
    form.dep.choices = deps

    if form.validate_on_submit():
        if form.name.data == 0:
            flash('Выберите преподавателя', 'danger')
            redirect(url_for('updateTeacherForm'))

        else:
            name = dict(form.name.choices).get(int(form.name.data))
            new_name = form.new_name.data or None
            pos = form.position.data or None
            ch = int(form.dep_ch.data)
            dep = dict(form.dep.choices).get(int(form.dep.data)) or None

            with psycopg.connect(host=app.config['DB_SERVER'], user=app.config['DB_USER'],
                                 password=app.config['DB_PASSWORD'], dbname=app.config['DB_NAME']) as con:
                cur = con.cursor()

                if new_name is not None:
                    cur.execute('UPDATE teacher '
                                'SET full_name = %s '
                                'WHERE full_name = %s', (new_name, name,))
                    name = new_name

                if pos is not None:
                    cur.execute('UPDATE teacher '
                                'SET position = %s '
                                'WHERE full_name = %s', (pos, name,))

                if dep is not None:
                    if ch == 1:
                        cur.execute('UPDATE teacher_department '
                                    'SET teacher_dep_number = %s '
                                    'WHERE teacher_emp_record_num = '
                                    '('
                                        'SELECT emp_record_num '
                                        'FROM teacher '
                                        'WHERE full_name = %s'
                                    ')', (dep, name,))

                    elif ch == 2:
                        rec = cur.execute('SELECT emp_record_num '
                                          'FROM teacher '
                                          'WHERE full_name = %s', (name,)).fetchone()
                        cur.execute('INSERT INTO teacher_department '
                                    'VALUES (%s, %s) ', (dep, rec[0],))

                    elif ch == 3:
                        cur.execute('DELETE FROM teacher_department '
                                    'WHERE teacher_dep_number = %s AND teacher_emp_record_num = '
                                    '('
                                        'SELECT emp_record_num '
                                        'FROM teacher '
                                        'WHERE full_name = %s'
                                    ')', (dep, name,))

                    else:
                        flash('Выберите действие для изменения кафедры', 'danger')
                        redirect(url_for('updateTeacherForm'))

            flash('Данные успешно обновлены', 'success')
            redirect(url_for('updateTeacherForm'))

    return render_template('renderForm.html', title='Редактирование существующего преподавателя', form=form)