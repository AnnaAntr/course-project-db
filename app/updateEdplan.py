from app import app
from flask import render_template
import psycopg
from flask_login import login_required

@app.get('/edit/edplan/update')
@login_required
def updateEdplan():
    with psycopg.connect(host=app.config['DB_SERVER'], user=app.config['DB_USER'],
                         password=app.config['DB_PASSWORD'], dbname=app.config['DB_NAME']) as con:
        cur = con.cursor()
        streams = cur.execute('SELECT stream_dir_code, entry_year FROM stream '
                              'ORDER BY stream_dir_code, entry_year').fetchall()

    return render_template('updateEdplan.html', title='Учебные планы потоков', streams=streams)