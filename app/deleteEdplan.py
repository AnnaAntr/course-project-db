from app import app
from flask import render_template
import psycopg

@app.get('/edit/edplan/delete')
def deleteEdplan():
    with psycopg.connect(host=app.config['DB_SERVER'], user=app.config['DB_USER'],
                         password=app.config['DB_PASSWORD'], dbname=app.config['DB_NAME']) as con:
        cur = con.cursor()
        streams = cur.execute('SELECT stream_dir_code, entry_year '
                              'FROM stream '
                              'ORDER BY stream_dir_code, entry_year').fetchall()

    return render_template('deleteEdplan.html', title='Выберите поток', streams=streams)