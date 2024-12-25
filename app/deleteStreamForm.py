from app import app
from flask import render_template, flash, redirect, url_for, abort
import psycopg
from app.forms import DeleteStreamForm
from flask_login import login_required

@app.route('/edit/stream/delete', methods=['GET', 'POST'])
@login_required
def deleteStreamForm():
    with psycopg.connect(host=app.config['DB_SERVER'], user=app.config['DB_USER'],
                         password=app.config['DB_PASSWORD'], dbname=app.config['DB_NAME']) as con:
        cur = con.cursor()
        streams = cur.execute('SELECT stream_dir_code, entry_year FROM stream ORDER BY stream_dir_code, entry_year').fetchall()

    if streams is None:
        abort(404)

    result = [(0, 'не выбрано' + '')]
    result += [(i + 1, f"{item[0]}, {item[1]}") for i, item in enumerate(streams)]

    form = DeleteStreamForm()
    form.stream.choices = result

    if form.validate_on_submit():
        if form.stream.data == 0:
            flash('Выберите поток', 'danger')
            redirect(url_for('deleteStreamForm'))
        else:
            st = dict(form.stream.choices).get(int(form.stream.data))
            s = st.split(", ")
            dir = s[0]
            year = s[1]

            with psycopg.connect(host=app.config['DB_SERVER'], user=app.config['DB_USER'],
                                 password=app.config['DB_PASSWORD'], dbname=app.config['DB_NAME']) as con:
                cur = con.cursor()
                cur.execute('DELETE FROM class '
                            'WHERE (week_day, class_number, week_type, room_number, building_address) IN '
                            '('
                                'SELECT week_day, class_number, week_type, room_number, building_address '
                                'FROM group_class JOIN group_tb USING (group_number) '
                                'WHERE group_dir_code = %s AND group_entry_year = %s'
                            ')', (dir, year))

                cur.execute('DELETE FROM stream '
                            'WHERE stream_dir_code = %s AND entry_year = %s', (dir, year,))

            flash('Данные успешно обновлены', 'success')
            redirect(url_for('deleteGroupForm'))

    flash('При удалении потока будут удалены связанные с ним группы и их расписание!', 'warning')
    return render_template('renderForm.html', title='Удаление существующего потока', form=form)