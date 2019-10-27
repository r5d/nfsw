# -*- coding: utf-8 -*-
#
#   SPDX-License-Identifier: ISC
#
#   Copyright (C) 2019 rsiddharth <s@ricketyspace.net>
#
#   This file is part of dingy.
#

from nfsw.auth import login_required
from nfsw.redis import redis


from flask import (
    Blueprint, render_template, redirect, url_for
)

bp = Blueprint('epilogue', __name__)


@bp.route('/epilogue', endpoint='epilogue')
@login_required
def epilogue():
    r = redis()

    if r.exists('epilogue:done'):
        return redirect(url_for('io'))

    r.set('epilogue:done', 1)

    return render_template('epilogue.html')
