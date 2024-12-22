from app import app
from flask import render_template, flash, redirect, url_for, abort
import psycopg
from app.forms import UpdateCourseForm
from app.tupleproc import tupleProc
from flask_login import login_required

@app.route('/edit/course/update', methods=['GET', 'POST'])
@login_required
def updateCourseForm():
    with psycopg.connect(host=app.config['DB_SERVER'], user=app.config['DB_USER'], password=app.config['DB_PASSWORD'],
                         dbname=app.config['DB_NAME']) as con:
        cur = con.cursor()
        courses = tupleProc(cur.execute('SELECT * FROM course ORDER BY name').fetchall())

    if courses is None:
        abort(404)

    form = UpdateCourseForm()
    form.course.choices = courses

    if form.validate_on_submit():
        new_name = form.new_name.data
        course = dict(form.course.choices).get(int(form.course.data))

        if form.course.data == 0:
            flash('Выберите предмет', 'danger')
            redirect(url_for('updateCourseForm'))

        elif new_name in courses:
            flash('Предмет с таким названием уже существует', 'danger')
            redirect(url_for('updateCourseForm'))

        else:
            with psycopg.connect(host=app.config['DB_SERVER'], user=app.config['DB_USER'],
                                 password=app.config['DB_PASSWORD'], dbname=app.config['DB_NAME']) as con:
                cur = con.cursor()
                cur.execute('UPDATE course '
                            'SET name = %s '
                            'WHERE name = %s', (new_name, course,))

            flash('Данные успешно обновлены', 'success')
            redirect(url_for('updateCourseForm'))

    return render_template('renderForm.html', title='Редактирование существующего предмета', form=form)