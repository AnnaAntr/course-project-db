from app import app
from flask import render_template, flash, redirect, url_for, abort
import psycopg
from app.forms import InsertTeacherForm
from app.tupleproc import tupleProc
from flask_login import login_required

@app.route('/edit/teacher/insert', methods=['GET', 'POST'])
@login_required
def insertTeacherForm():
    with psycopg.connect(host=app.config['DB_SERVER'], user=app.config['DB_USER'], password=app.config['DB_PASSWORD'],
                         dbname=app.config['DB_NAME']) as con:
        cur = con.cursor()
        deps = tupleProc(cur.execute('SELECT dep_number FROM department ORDER BY dep_number').fetchall())
        teachers = cur.execute('SELECT full_name, emp_record_num FROM teacher').fetchall()

    if deps is None:
        abort(404)

    form = InsertTeacherForm()
    form.dep.choices = deps

    if form.validate_on_submit():
        name = form.name.data
        rec = form.rec_num.data
        pos = form.position.data or None
        dep = dict(form.dep.choices).get(int(form.dep.data))
        t = (name, rec,)

        if teachers is not None and t in teachers:
            flash('Преподаватель с таким ФИО и номером трудовой книжки уже существует', 'danger')
            redirect(url_for('insertTeacherForm'))

        else:
            with psycopg.connect(host=app.config['DB_SERVER'], user=app.config['DB_USER'],
                                 password=app.config['DB_PASSWORD'], dbname=app.config['DB_NAME']) as con:
                cur = con.cursor()
                cur.execute('INSERT INTO teacher (emp_record_num, full_name) '
                            'VALUES (%s, %s)', (rec, name,))

                if pos is not None:
                    cur.execute('UPDATE teacher '
                                'SET position = %s '
                                'WHERE emp_record_num = %s', (pos, rec,))

                if dep != 'не выбрано':
                    cur.execute('INSERT INTO teacher_department '
                                'VALUES (%s, %s)', (dep, rec))

            flash('Данные успешно обновлены', 'success')
            redirect(url_for('insertTeacherForm'))

    return render_template('renderForm.html', title='Добавление нового преподавателя', form=form)