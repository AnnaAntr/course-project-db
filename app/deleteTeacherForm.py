from app import app
from flask import render_template, flash, redirect, url_for, abort
import psycopg
from app.forms import DeleteTeacherForm
from app.tupleproc import tupleProc
from flask_login import login_required

@app.route('/edit/teacher/delete', methods=['GET', 'POST'])
@login_required
def deleteTeacherForm():
    with psycopg.connect(host=app.config['DB_SERVER'], user=app.config['DB_USER'],
                         password=app.config['DB_PASSWORD'], dbname=app.config['DB_NAME']) as con:
        cur = con.cursor()
        teachers = tupleProc(cur.execute('SELECT full_name FROM teacher ORDER BY full_name').fetchall())

    if teachers is None:
        abort(404)

    form = DeleteTeacherForm()
    form.name.choices = teachers

    if form.validate_on_submit():
        if form.name.data == 0:
            flash('Выберите преподавателя', 'danger')
            redirect(url_for('deleteTeacherForm'))
        else:
            tname = dict(form.name.choices).get(int(form.name.data))
            with psycopg.connect(host=app.config['DB_SERVER'], user=app.config['DB_USER'],
                                 password=app.config['DB_PASSWORD'], dbname=app.config['DB_NAME']) as con:
                cur = con.cursor()
                cur.execute('DELETE FROM teacher '
                            'WHERE full_name = %s', (tname,))

            flash('Данные успешно обновлены', 'success')
            redirect(url_for('deleteTeacherForm'))

    return render_template('renderForm.html', title='Удаление существующего преподавателя', form=form)