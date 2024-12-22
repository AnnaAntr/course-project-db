from app import app
from flask import render_template
import psycopg

@app.get('/groups')
def groups():
    with psycopg.connect(host=app.config['DB_SERVER'], user=app.config['DB_USER'],
                         password=app.config['DB_PASSWORD'], dbname=app.config['DB_NAME']) as con:
        cur = con.cursor()
        groups = cur.execute('SELECT group_number, curr_term, group_dir_code, entry_year, direction_dep_number '
                             'FROM group_tb JOIN stream ON group_dir_code = stream_dir_code AND group_entry_year = entry_year '
                             'JOIN direction ON stream_dir_code = code '
                             'JOIN direction_department ON code = dir_code '
                             'ORDER BY group_number').fetchall()

    return render_template('groups.html', title='Группы', groups=groups)