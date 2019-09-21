import functools

import nfsw.scenes as scenes

from nfsw.auth import login_required, login_required_ajax
from nfsw.redis import redis as r, key as k
from nfsw.scenes import current_scene

from flask import (
    Blueprint, render_template, request
)

bp = Blueprint('io', __name__)


def preprocess(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        setup()

        return view(**kwargs)

    return wrapped_view


@bp.route('/io', endpoint='io')
@login_required
def io():
    return render_template('io.html')


@bp.route('/io/query', methods=['POST'])
@login_required_ajax
@preprocess
def query():
    q = request.get_data(as_text=True)

    # Log query.
    r().rpush(k('log'), q)

    # Get current scene.
    scene = current_scene()
    if scene is None:
        return {
            'ans': 'Your game state is fucked. Ping Siddharth.'
        }

    # Respond.
    return {
        'ans': scene(q)
    }


def setup():
    """Setup user's state"""
    if not r().exists(k('scene')):
        r().set(k('scene'), 'sexshop')
