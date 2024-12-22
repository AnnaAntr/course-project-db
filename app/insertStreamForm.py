from app import app
from flask import render_template, flash, redirect, url_for, abort
import psycopg
from app.forms import InsertStreamForm
from app.tupleproc import tupleProc
from flask_login import login_required

@app.route('/edit/stream/insert', methods=['GET', 'POST'])
@login_required
def insertStreamForm():
    with psycopg.connect(host=app.config['DB_SERVER'], user=app.config['DB_USER'], password=app.config['DB_PASSWORD'],
                         dbname=app.config['DB_NAME']) as con:
        cur = con.cursor()
        directions = tupleProc(cur.execute('SELECT code FROM direction ORDER BY code').fetchall())
        streams = cur.execute('SELECT * FROM stream').fetchall()

    if directions is None:
        abort(404)

    form = InsertStreamForm()
    form.dir.choices = directions

    if form.validate_on_submit():
        st = (form.year.data, dict(form.dir.choices).get(int(form.dir.data)),)
        dir = dict(form.dir.choices).get(int(form.dir.data))
        year = form.year.data

        if form.dir.data == 0:
            flash('Выберите направление', 'danger')
            redirect(url_for('insertStreamForm'))

        elif streams is not None and st in streams:
            flash('Такой поток уже существует', 'danger')
            redirect(url_for('insertStreamForm'))

        else:
            with psycopg.connect(host=app.config['DB_SERVER'], user=app.config['DB_USER'],
                                 password=app.config['DB_PASSWORD'], dbname=app.config['DB_NAME']) as con:
                cur = con.cursor()
                cur.execute('INSERT INTO stream VALUES (%s, %s)', (year, dir,))

            flash('Данные успешно обновлены', 'success')
            redirect(url_for('insertStreamForm'))

    return render_template('renderForm.html', title='Добавление нового потока', form=form)