from app import app
from flask import render_template
import psycopg

@app.get('/courses')
def courses():
    with psycopg.connect(host=app.config['DB_SERVER'], user=app.config['DB_USER'],
                         password=app.config['DB_PASSWORD'], dbname=app.config['DB_NAME']) as con:
        cur = con.cursor()
        courses = cur.execute('SELECT * FROM course ORDER BY name').fetchall()

    return render_template('courses.html', title='Предметы', courses=courses)