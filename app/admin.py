from app import app
import psycopg
from app import login_manager
from flask_login import UserMixin

class Admin(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

@login_manager.user_loader
def load_admin(id):
    with psycopg.connect(host=app.config['DB_SERVER'], user=app.config['DB_USER'],
                         password=app.config['DB_PASSWORD'], dbname=app.config['DB_NAME']) as con:
        cur = con.cursor()
        username, password = cur.execute('SELECT username, password '
                                         'FROM admin '
                                         'WHERE id = %s', (id,)).fetchone()

    return Admin(id, username, password)