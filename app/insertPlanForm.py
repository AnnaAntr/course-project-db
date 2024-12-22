from app import app
from flask import render_template, flash, redirect, url_for, abort
import psycopg
from app.forms import InsertPlanForm
from app.tupleproc import tupleProc
from flask_login import login_required

@app.route('/edit/edplan/insert', methods=['GET', 'POST'])
@login_required
def insertPlanForm():
    with psycopg.connect(host=app.config['DB_SERVER'], user=app.config['DB_USER'],
                         password=app.config['DB_PASSWORD'], dbname=app.config['DB_NAME']) as con:
        cur = con.cursor()
        streams = cur.execute('SELECT stream_dir_code, entry_year FROM stream ORDER BY stream_dir_code, entry_year').fetchall()
        courses = tupleProc(cur.execute('SELECT * FROM course ORDER BY name').fetchall())
        plans = cur.execute('SELECT term_number, stream_dir_code, stream_entry_year, course_name '
                            'FROM term_stream_by_course').fetchall()

    if streams is None or courses is None:
        abort(404)

    result = [(0, 'не выбрано' + '')]
    result += [(i + 1, f"{item[0]}, {item[1]}") for i, item in enumerate(streams)]

    form = InsertPlanForm()
    form.stream.choices = result
    form.course.choices = courses

    if form.validate_on_submit():
        st = dict(form.stream.choices).get(int(form.stream.data))
        s = st.split(", ")
        dir = s[0]
        year = s[1]
        course = dict(form.course.choices).get(int(form.course.data))
        term = form.term.data
        att = dict(form.att.choices).get(int(form.att.data)) or None
        lec = form.lec.data or None
        lab = form.lab.data or None

        pl = (term, dir, int(year), course,)

        if form.stream.data == 0 or form.course.data == 0:
            flash('Выберите поток и предмет', 'danger')
            redirect(url_for('insertPlanForm'))

        elif plans is not None and pl in plans:
            flash('Семестр по этому предмету с данными параметрами уже существует', 'danger')
            redirect(url_for('insertPlanForm'))

        else:
            with psycopg.connect(host=app.config['DB_SERVER'], user=app.config['DB_USER'],
                                 password=app.config['DB_PASSWORD'], dbname=app.config['DB_NAME']) as con:
                cur = con.cursor()
                cur.execute('INSERT INTO term_stream_by_course (term_number, stream_dir_code, stream_entry_year, course_name) '
                            'VALUES (%s, %s, %s, %s)', (term, dir, year, course))

                if att is not None:
                    cur.execute('UPDATE term_stream_by_course '
                                'SET att_type = %s '
                                'WHERE term_number = %s AND stream_dir_code = %s '
                                'AND stream_entry_year = %s AND course_name = %s', (att, term, dir, year, course))

                if lec is not None:
                    cur.execute('UPDATE term_stream_by_course '
                                'SET lec_hours = %s '
                                'WHERE term_number = %s AND stream_dir_code = %s '
                                'AND stream_entry_year = %s AND course_name = %s', (lec, term, dir, year, course))

                if lab is not None:
                    cur.execute('UPDATE term_stream_by_course '
                                'SET lab_hours = %s '
                                'WHERE term_number = %s AND stream_dir_code = %s '
                                'AND stream_entry_year = %s AND course_name = %s', (lab, term, dir, year, course))

            flash('Данные успешно обновлены', 'success')
            redirect(url_for('insertPlanForm'))

    return render_template('renderForm.html', title='Добавление нового учебного плана', form=form)