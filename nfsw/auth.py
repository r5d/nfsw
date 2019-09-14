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


