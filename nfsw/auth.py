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

