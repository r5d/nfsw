import functools

import nfsw.scenes as scenes

from nfsw.auth import login_required, login_required_ajax
from nfsw.redis import redis as r, redisc, key as k
from nfsw.scenes import current_scene
from nfsw.util import read_junk

from flask import (
    Blueprint, render_template, request
)


bp = Blueprint('io', __name__)


def preprocess(view):
    def setup():
        r = redisc()

        if not r.exists('scene'):
            r.set('scene', 'sexshop')


    @functools.wraps(view)
    def wrapped_view(**kwargs):
        setup()

        return view(**kwargs)

    return wrapped_view


@bp.route('/io', endpoint='io')
@login_required
def io():
    return render_template('io.html')


@bp.route('/io/reset')
@login_required
def reset():
    r().delete(k('scene'))
    r().delete(k('scene:sexshop:gg'))
    r().delete(k('scenes:done'))

    r().delete(k('player:type'))
    r().delete(k('player:type:body'))
    r().delete(k('player:type:mind'))
    r().delete(k('player:type:mind'))

    r().delete(k('log'))

    return 'Game reset'


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
        'ans': scene({'q': q})
    }


@bp.route('/io/intro', methods=['POST'])
@login_required_ajax
@preprocess
def intro():

    # Get current scene
    scene = current_scene()
    if scene is None:
        return {
            'intro': read_junk('foobar/god')
        }, 500

    return {
        'intro': scene({'intro': 1})
    }
