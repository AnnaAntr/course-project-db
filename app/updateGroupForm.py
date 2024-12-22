from app import app
from app.forms import UpdateGroupForm
from flask import render_template, flash, redirect, url_for, abort
import psycopg
from app.tupleproc import tupleProc
from flask_login import login_required

@app.route('/edit/group/update', methods=['GET', 'POST'])
@login_required
def updateGroupForm():
    with psycopg.connect(host=app.config['DB_SERVER'], user=app.config['DB_USER'],
                         password=app.config['DB_PASSWORD'], dbname=app.config['DB_NAME']) as con:
        cur = con.cursor()
        groups = tupleProc(cur.execute('SELECT group_number FROM group_tb ORDER BY group_number').fetchall())

    if groups is None:
        abort(404)

    form = UpdateGroupForm()
    form.group.choices = groups

    if form.validate_on_submit():
        if form.group.data == 0:
            flash('Выберите группу', 'danger')
            redirect(url_for('updateGroupForm'))

        else:
            gr = dict(form.group.choices).get(int(form.group.data))
            new_term = form.curr_term.data

            with psycopg.connect(host=app.config['DB_SERVER'], user=app.config['DB_USER'],
                                 password=app.config['DB_PASSWORD'], dbname=app.config['DB_NAME']) as con:
                cur = con.cursor()
                cur.execute('UPDATE group_tb '
                            'SET curr_term = %s '
                            'WHERE group_number = %s', (new_term, gr,))

            flash('Данные успешно обновлены', 'success')
            redirect(url_for('updateGroupForm'))

    return render_template('renderForm.html', title='Редактирование существующей группы', form=form)