from app import app
from flask import render_template, flash, redirect, url_for, abort
import psycopg
from app.forms import DeleteCourseForm
from app.tupleproc import tupleProc
from flask_login import login_required

@app.route('/edit/course/delete', methods=['GET', 'POST'])
@login_required
def deleteCourseForm():
    with psycopg.connect(host=app.config['DB_SERVER'], user=app.config['DB_USER'],
                         password=app.config['DB_PASSWORD'], dbname=app.config['DB_NAME']) as con:
        cur = con.cursor()
        courses = tupleProc(cur.execute('SELECT * FROM course ORDER BY name').fetchall())

    if courses is None:
        abort(404)

    form = DeleteCourseForm()
    form.course.choices = courses

    if form.validate_on_submit():
        course = dict(form.course.choices).get(int(form.course.data))

        if form.course.data == 0:
            flash('Выберите предмет', 'danger')
            redirect(url_for('deleteCourseForm'))

        else:
            with psycopg.connect(host=app.config['DB_SERVER'], user=app.config['DB_USER'],
                                 password=app.config['DB_PASSWORD'], dbname=app.config['DB_NAME']) as con:
                cur = con.cursor()
                cur.execute('DELETE FROM course '
                            'WHERE name = %s', (course,))

            flash('Данные успешно обновлены', 'success')
            redirect(url_for('deleteCourseForm'))

    flash('При удалении предмета будут удалены связанные с ним пары и учебные планы!', 'warning')
    return render_template('renderForm.html', title='Удаление существующего предмета', form=form)