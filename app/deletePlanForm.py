from app import app
from flask import render_template, flash, redirect, url_for, abort
import psycopg
from app.forms import DeletePlanForm
from flask_login import login_required

@app.route('/edit/edplan/delete/<dir>/<year>', methods=['GET', 'POST'])
@login_required
def deletePlanForm(dir, year):
    with psycopg.connect(host=app.config['DB_SERVER'], user=app.config['DB_USER'],
                         password=app.config['DB_PASSWORD'], dbname=app.config['DB_NAME']) as con:
        cur = con.cursor()
        plans = cur.execute('SELECT course_name, term_number '
                            'FROM term_stream_by_course '
                            'WHERE stream_dir_code = %s AND stream_entry_year = %s '
                            'ORDER BY term_number, course_name', (dir, year,)).fetchall()

    if plans is None:
        abort(404)

    result = [(0, 'не выбрано')]
    result += [(i + 1, f"{item[0]}, {item[1]} семестр") for i, item in enumerate(plans)]

    form = DeletePlanForm()
    form.course.choices = result

    if form.validate_on_submit():
        if form.course.data == 0:
            flash('Выберите план', 'danger')
            redirect(url_for('deletePlanForm', dir=dir, year=year))

        else:
            pl = dict(form.course.choices).get(int(form.course.data))
            p = pl.split(", ")
            course = p[0]
            term = p[1][0]

            with psycopg.connect(host=app.config['DB_SERVER'], user=app.config['DB_USER'],
                                 password=app.config['DB_PASSWORD'], dbname=app.config['DB_NAME']) as con:
                cur = con.cursor()
                cur.execute('DELETE FROM term_stream_by_course '
                            'WHERE stream_dir_code = %s AND stream_entry_year = %s '
                            'AND course_name = %s AND term_number = %s', (dir, year, course, term,))

            flash('Данные успешно обновлены', 'success')
            redirect(url_for('deletePlanForm', dir=dir, year=year))

    return render_template('renderForm.html', title='Удаление существующего учебного плана', form=form)