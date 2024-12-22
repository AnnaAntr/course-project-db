from werkzeug.security import check_password_hash
from app import app
import psycopg
from app.forms import AdminLoginForm
from app.admin import Admin
from flask import render_template, redirect, flash, url_for
from flask_login import login_user, current_user

@app.route('/login', methods=['GET', 'POST'])
def adminLoginForm():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = AdminLoginForm()

    if form.validate_on_submit():
        with psycopg.connect(host=app.config['DB_SERVER'], user=app.config['DB_USER'],
                             password=app.config['DB_PASSWORD'], dbname=app.config['DB_NAME']) as con:
            cur = con.cursor()
            res = cur.execute('SELECT id, username, password FROM admin '
                              'WHERE username = %s', (form.username.data,)).fetchone()

        if res is None or not check_password_hash(res[2], form.password.data):
            flash('Неверный логин или пароль', 'danger')
            return redirect(url_for('adminLoginForm'))

        id, username, password = res
        admin = Admin(id, username, password)
        login_user(admin, remember=form.remember_me.data)

        flash('Вы успешно вошли в систему', 'success')
        return redirect(url_for('index'))

    return render_template('adminLoginForm.html', title='Вход', form=form)