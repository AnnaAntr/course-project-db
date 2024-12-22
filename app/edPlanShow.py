from app import app
import psycopg
from flask import render_template

@app.get('/directions/edplan/<dir>/<year>')
def edPlanShow(dir, year):
    with psycopg.connect(host=app.config['DB_SERVER'], user=app.config['DB_USER'],
                         password=app.config['DB_PASSWORD'], dbname=app.config['DB_NAME']) as con:
        cur = con.cursor()
        plan = cur.execute('SELECT term_number, course_name, att_type, lec_hours, lab_hours '
                           'FROM term_stream_by_course '
                           'WHERE stream_dir_code = %s AND stream_entry_year = %s '
                           'ORDER BY stream_dir_code, stream_entry_year, term_number', (dir, year,)).fetchall()

    return render_template('edPlanShow.html', title=f'Учебный план направления {dir} на {year} год', plan=plan)