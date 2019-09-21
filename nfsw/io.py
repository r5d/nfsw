from nfsw.auth import login_required, login_required_ajax

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
    cmd = request.get_data(as_text=True)

    return {
        'ans': cmd
    }


def setup():
    """Setup user's state"""
    if not r().exists(k('scene')):
        r().set(k('scene'), 'sexshop')
