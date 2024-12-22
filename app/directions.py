from app import app
from flask import render_template
import psycopg
from collections import defaultdict

@app.get('/directions')
def directions():
    with psycopg.connect(host=app.config['DB_SERVER'], user=app.config['DB_USER'],
                         password=app.config['DB_PASSWORD'], dbname=app.config['DB_NAME']) as con:
        cur = con.cursor()
        directions = cur.execute('SELECT code, name, entry_year '
                                 'FROM direction JOIN stream ON code = stream_dir_code '
                                 'ORDER BY code, entry_year').fetchall()

    grouped = defaultdict(list)
    for i in range(len(directions)):
        key = (directions[i][0], directions[i][1])
        grouped[key].append(directions[i][2])

    return render_template('directions.html', title='Направления', directions=grouped)