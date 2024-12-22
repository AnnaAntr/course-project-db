from app import app
import psycopg
from app.forms import AdminRegForm
from flask import render_template, flash, redirect, url_for
from flask_login import current_user
from werkzeug.security import generate_password_hash

@app.route('/registration', methods=['GET', 'POST'])
def adminRegForm():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    with psycopg.connect(host=app.config['DB_SERVER'], user=app.config['DB_USER'],
                         password=app.config['DB_PASSWORD'], dbname=app.config['DB_NAME']) as con:
        cur = con.cursor()
        admins = cur.execute('SELECT username FROM admin').fetchall()

    form = AdminRegForm()

    if form.validate_on_submit():
        pwd_hash = generate_password_hash(form.password.data)
        uname = form.username.data
        adm = (uname,)

        if adm in admins:
            flash('Администратор с таким именем существует', 'danger')
            redirect('adminRegForm')

        else:
            with psycopg.connect(host=app.config['DB_SERVER'], user=app.config['DB_USER'],
                                 password=app.config['DB_PASSWORD'], dbname=app.config['DB_NAME']) as con:
                cur = con.cursor()
                cur.execute('INSERT INTO admin(username, password) '
                            'VALUES (%s, %s)', (uname, pwd_hash))

            flash('Регистрация прошла успешно', 'success')
            return redirect(url_for('index'))

    return render_template('adminRegForm.html', title='Регистрация', form=form)
