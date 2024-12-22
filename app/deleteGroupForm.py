from app import app
from flask import render_template, flash, redirect, url_for, abort
import psycopg
from app.forms import DeleteGroupForm
from app.tupleproc import tupleProc
from flask_login import login_required

@app.route('/edit/group/delete', methods=['GET', 'POST'])
@login_required
def deleteGroupForm():
    with psycopg.connect(host=app.config['DB_SERVER'], user=app.config['DB_USER'],
                         password=app.config['DB_PASSWORD'], dbname=app.config['DB_NAME']) as con:
        cur = con.cursor()
        groups = tupleProc(cur.execute('SELECT group_number FROM group_tb ORDER BY group_number').fetchall())

    if groups is None:
        abort(404)

    form = DeleteGroupForm()
    form.group.choices = groups

    if form.validate_on_submit():
        if form.group.data == 0:
            flash('Выберите группу', 'danger')
            redirect(url_for('deleteGroupForm'))
        else:
            gr = dict(form.group.choices).get(int(form.group.data))
            with psycopg.connect(host=app.config['DB_SERVER'], user=app.config['DB_USER'],
                                 password=app.config['DB_PASSWORD'], dbname=app.config['DB_NAME']) as con:
                cur = con.cursor()
                cur.execute('DELETE FROM class '
                            'WHERE (week_day, class_number, week_type, room_number, building_address) IN '
                            '('
                                'SELECT week_day, class_number, week_type, room_number, building_address '
                                'FROM group_class '
                                'WHERE group_number = %s'
                            ')', (gr,))

                cur.execute('DELETE FROM group_tb '
                            'WHERE group_number = %s', (gr,))

            flash('Данные успешно обновлены', 'success')
            redirect(url_for('deleteGroupForm'))

    flash('При удалении группы будет удалено связанное с ней расписание!', 'warning')
    return render_template('renderForm.html', title='Удаление существующей группы', form=form)