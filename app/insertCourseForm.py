from app import app
from flask import render_template, flash, redirect, url_for
import psycopg
from app.forms import InsertCourseForm
from flask_login import login_required

@app.route('/edit/course/insert', methods=['GET', 'POST'])
@login_required
def insertCourseForm():
    with psycopg.connect(host=app.config['DB_SERVER'], user=app.config['DB_USER'],
                         password=app.config['DB_PASSWORD'], dbname=app.config['DB_NAME']) as con:
        cur = con.cursor()
        courses = cur.execute('SELECT * FROM course').fetchall()

    form = InsertCourseForm()

    if form.validate_on_submit():
        course = form.course.data
        c = (course,)

        if courses is not None and c in courses:
            flash('Такой предмет уже существует', 'danger')
            redirect(url_for('insertCourseForm'))

        else:
            with psycopg.connect(host=app.config['DB_SERVER'], user=app.config['DB_USER'],
                                 password=app.config['DB_PASSWORD'], dbname=app.config['DB_NAME']) as con:
                cur = con.cursor()
                cur.execute('INSERT INTO course VALUES (%s)', (course,))

            flash('Данные успешно обновлены', 'success')
            redirect(url_for('insertCourseForm'))

    return render_template('renderForm.html', title='Добавление нового предмета', form=form)