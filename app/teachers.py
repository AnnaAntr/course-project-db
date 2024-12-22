from app import app
from flask import render_template
import psycopg
from collections import defaultdict

@app.get('/teachers')
def teachers():
    with psycopg.connect(host=app.config['DB_SERVER'], user=app.config['DB_USER'], password=app.config['DB_PASSWORD'],
                         dbname=app.config['DB_NAME']) as con:
        cur = con.cursor()
        teachers = cur.execute('SELECT full_name, position, teacher_dep_number FROM teacher JOIN teacher_department '
                               'ON emp_record_num = teacher_emp_record_num ORDER BY full_name').fetchall()

        grouped = defaultdict(list)
        for i in range(len(teachers)):
            key = (teachers[i][0], teachers[i][1])
            grouped[key].append(teachers[i][2])

        return render_template('teachers.html', title='Преподаватели', teachers=grouped)