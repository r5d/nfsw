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

    return render_template('epilogue.html')
