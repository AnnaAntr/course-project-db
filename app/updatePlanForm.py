from app import app
from flask import render_template, flash, redirect, url_for, abort
import psycopg
from app.forms import UpdatePlanForm
from flask_login import login_required

@app.route('/edit/edplan/update/<dir>/<year>', methods=['GET', 'POST'])
@login_required
def updatePlanForm(dir, year):
    with psycopg.connect(host=app.config['DB_SERVER'], user=app.config['DB_USER'], password=app.config['DB_PASSWORD'],
                         dbname=app.config['DB_NAME']) as con:
        cur = con.cursor()
        plans = cur.execute('SELECT course_name, term_number '
                            'FROM term_stream_by_course '
                            'WHERE stream_dir_code = %s AND stream_entry_year = %s '
                            'ORDER BY term_number, course_name', (dir, year,)).fetchall()

    if plans is None:
        abort(404)

    result = [(0, 'не выбрано')]
    result += [(i + 1, f"{item[0]}, {item[1]} семестр") for i, item in enumerate(plans)]

    form = UpdatePlanForm()
    form.course.choices = result

    if form.validate_on_submit():
        if form.course.data == 0:
            flash('Выберите план', 'danger')
            redirect(url_for('updatePlanForm', dir=dir, year=year))

        elif form.lec.data is None and form.lab.data is None and form.term.data is None and form.att.data == 0:
            flash('Заполните хотя бы одно поле', 'danger')
            redirect(url_for('updatePlanForm', dir=dir, year=year))

        else:
            pl = dict(form.course.choices).get(int(form.course.data))
            p = pl.split(", ")
            course = p[0]
            term = p[1][0]
            new_term = form.term.data or None
            lec = form.lec.data or None
            lab = form.lab.data or None
            att = dict(form.att.choices).get(int(form.att.data))

            with psycopg.connect(host=app.config['DB_SERVER'], user=app.config['DB_USER'],
                                 password=app.config['DB_PASSWORD'], dbname=app.config['DB_NAME']) as con:
                cur = con.cursor()

                if lec is not None:
                    cur.execute('UPDATE term_stream_by_course '
                                'SET lec_hours = %s '
                                'WHERE stream_dir_code = %s AND stream_entry_year = %s '
                                'AND course_name = %s AND term_number = %s', (lec, dir, year, course, term,))

                if lab is not None:
                    cur.execute('UPDATE term_stream_by_course '
                                'SET lab_hours = %s '
                                'WHERE stream_dir_code = %s AND stream_entry_year = %s '
                                'AND course_name = %s AND term_number = %s', (lab, dir, year, course, term,))

                if att != "не выбрано":
                    cur.execute('UPDATE term_stream_by_course '
                                'SET att_type = %s '
                                'WHERE stream_dir_code = %s AND stream_entry_year = %s '
                                'AND course_name = %s AND term_number = %s', (att, dir, year, course, term,))

                if new_term is not None:
                    cur.execute('UPDATE term_stream_by_course '
                                'SET term_number = %s '
                                'WHERE stream_dir_code = %s AND stream_entry_year = %s '
                                'AND course_name = %s AND term_number = %s', (new_term, dir, year, course, term,))

            flash('Данные успешно обновлены', 'success')
            redirect(url_for('updatePlanForm', dir=dir, year=year))

    return render_template('renderForm.html', title='Редактирование существующего учебного плана', form=form)