from app import app
from flask import render_template, flash, redirect, url_for, abort
import psycopg
from app.forms import InsertGroupForm
from app.tupleproc import tupleProc
from flask_login import login_required

@app.route('/edit/group/insert', methods=['GET', 'POST'])
@login_required
def insertGroupForm():
    with psycopg.connect(host=app.config['DB_SERVER'], user=app.config['DB_USER'],
                         password=app.config['DB_PASSWORD'], dbname=app.config['DB_NAME']) as con:
        cur = con.cursor()
        directions = tupleProc(cur.execute('SELECT code FROM direction ORDER BY code').fetchall())
        groups = cur.execute('SELECT group_number FROM group_tb').fetchall()
        streams = cur.execute('SELECT * FROM stream').fetchall()

    if directions is None:
        abort(404)

    form = InsertGroupForm()
    form.dir.choices = directions

    if form.validate_on_submit():
        gr = (form.group.data,)
        term = form.curr_term.data
        dir = dict(form.dir.choices).get(int(form.dir.data))
        year = form.year.data
        st = (year, dir)

        if form.dir.data == 0:
            flash('Выберите направление', 'danger')
            redirect(url_for('insertGroupForm'))

        elif groups is not None and gr in groups:
            flash('Группа с таким номером уже существует', 'danger')
            redirect(url_for('insertGroupForm'))

        elif streams is not None and st not in streams:
            flash(f'Не существует потока {year} года направления {dir}', 'danger')
            redirect(url_for('insertGroupForm'))

        else:
            with psycopg.connect(host=app.config['DB_SERVER'], user=app.config['DB_USER'],
                                 password=app.config['DB_PASSWORD'], dbname=app.config['DB_NAME']) as con:
                cur = con.cursor()
                cur.execute('INSERT INTO group_tb VALUES (%s, %s, %s, %s)', (form.group.data, term, dir, year,))

            flash('Данные успешно обновлены', 'success')
            redirect(url_for('insertGroupForm'))

    return render_template('insertGroupForm.html', title='Добавление новой группы', form=form)