# -*- coding: utf-8 -*-
#
#   SPDX-License-Identifier: ISC
#
#   Copyright (C) 2019 rsiddharth <s@ricketyspace.net>
#
#   This file is part of nfsw.
#

import functools

import nfsw.scenes as scenes

from nfsw.auth import login_required, login_required_ajax, logout
from nfsw.redis import redis
from nfsw.scenes import current_scene
from nfsw.util import read_junk

from flask import (
    Blueprint, render_template, request
)


bp = Blueprint('io', __name__)


def preprocess(view):
    def setup():
        r = redis()

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
    r = redis()

    for k in r.keys():
        r.delete(k)

    return 'Game reset'


@bp.route('/io/query', methods=['POST'])
@login_required_ajax
@preprocess
def query():
    r = redis()

    def sanitize(q):
        return q.strip().lower()

    r = redis()
    q = request.get_data(as_text=True)

    # Log query.
    r.rpush('log', q)


    # logout
    if q == 'nfsw logout':
        logout()
        return {
            'ans': 'Logging you out...',
            'logout': True
        }


    # help.
    if q == 'help':
        return {
            'ans': read_junk('help/senditdown')
        }

    # reset.
    if q == 'nfsw reset':
        reset()
        return {
            'ans': 'Initiating game reset...',
            'reset': True
        }

    # colophon
    if q == 'colophon':
        return {
            'ans': read_junk('colophon/ohno')
        }

    # Get current scene.
    scene = current_scene()
    if scene is None:
        return {
            'ans': 'Your game state is fucked. Ping Siddharth.'
        }

    # Respond.
    return {
        'ans': scene({'q': sanitize(q)})
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
