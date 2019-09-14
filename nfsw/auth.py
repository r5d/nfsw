import functools

import os

from flask import (
    Blueprint, flash, g, redirect, render_template, request,
    session, url_for
)
from werkzeug.security import (
    check_password_hash, generate_password_hash
)

from nfsw.db import get_db


bp = Blueprint('auth', __name__)


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('index'))

        return view(**kwargs)

    return wrapped_view


def anon_only(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is not None:
            return redirect(url_for('io'))

        return view(**kwargs)

    return wrapped_view


def not_agreed(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user['terms_agreed']:
            return redirect(url_for('io'))

        return view(**kwargs)

    return wrapped_view


@bp.route('/login', methods=('GET', 'POST'))
@anon_only
def login():
    def render(e=''):
        if e:
            flash(e)

        return render_template('login.html')

    db = get_db()

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        # Validate
        if not username:
            return render('Name is required')
        elif not password:
            return render('Password is required')

        user  = db.execute('SELECT * FROM user WHERE username=?',
                           (username,)).fetchone()

        if user is None:
            return render('User not found')
        elif not check_password_hash(user['password'], password):
            return render('Password is incorrect')

        session.clear()
        session['user_id'] = user['id']

    return render()


@bp.route('/register', methods=('GET', 'POST'))
@anon_only
def register():
    def render(e=''):
        if e:
            flash(e)

        return render_template('register.html')

    db = get_db()

    if request.method == 'POST':
        print(request.form)

        username = request.form['username']
        password = request.form['password']

        # Validate
        if not username:
            return render('Name is required')
        elif db.execute('SELECT id FROM user where username=?',
                        (username,)).fetchone() is not None:
            return render('Name already taken')

        # Generate password if empty.
        if not password:
            password = os.urandom(4).hex()


        r = db.execute('INSERT INTO user (username, password)'
                       ' VALUES (?, ?)',
                       (username, generate_password_hash(password)))
        db.commit()

        if r.lastrowid < 1:
            return render('Unable to create user')

        session.clear()
        session['user_id'] = r.lastrowid

        return redirect(url_for('auth.terms'))

    return render()


@bp.route('/terms', methods=('GET', 'POST'))
@login_required
@not_agreed
def terms():
    if request.method == 'POST':
        if 'agree' not in request.form:
            return redirect(url_for('auth.sorry'))

        # Mark terms agreed.
        db = get_db()
        r = db.execute(
            'UPDATE user SET terms_agreed=1 WHERE id=?',
            (g.user['id'],))
        db.commit()

        return redirect(url_for('io'))

    return render_template('terms.html')


@bp.route('/sorry')
@login_required
@not_agreed
def sorry():
    session.clear()
    return render_template('sorry.html')


@bp.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect(url_for('index'))


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id=?', (user_id,)
        ).fetchone()

        if (request.endpoint not in ['auth.terms', 'auth.sorry']
            and g.user['terms_agreed'] != 1):
            return redirect(url_for('auth.terms'))
