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


bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('start', methods=('GET', 'POST'))
def auth():
    if request.method == 'POST':
        username = request.form['username']

        password = None
        if 'password' in request.form:
            password = request.form['password']

        if not username:
            return {
                'status': 'error',
                'msg': 'Name is required',
                'fields': ['username']
            }
        elif username and password:
            return login(username, password)

        else:
            return register(username)

    return render_template('auth/index.html')


def login(username, password):
    db = get_db()

    user = db.execute('SELECT * FROM user WHERE username=?', (username,)
    ).fetchone()

    if user is None:
        return {
            'status': 'error',
            'msg': 'User not found',
            'fields': ['username']
        }

    if not check_password_hash(user['password'], password):
        return {
            'status': 'error',
            'msg': 'Password is incorrect',
            'fields': ['password']
        }

    session.clear()
    session['user_id'] = user['id']

    return {
        'status': 'ok',
        'url': url_for('hello')
    }


def register(username):
    db = get_db()

    if db.execute('SELECT id FROM user where username=?', (username,)
    ).fetchone() is not None:
        return {
            'status': 'pass',
            'msg': 'Looks you\'ve registered before!'
            + ' Gimme your password. Pretty please.'
        }

    password = os.urandom(4).hex()

    r = db.execute('INSERT INTO user (username, password) VALUES (?, ?)',
               (username, generate_password_hash(password)))
    db.commit()

    print(r.fetchone)
    print(password)

    session.clear()
    session['newuser'] = True

    return {
        'status': 'ok',
        'url': url_for('hello')
    }

