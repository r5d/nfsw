from nfsw.auth import login_required, login_required_ajax

from flask import (
    Blueprint, render_template, request
)

bp = Blueprint('io', __name__)

@bp.route('/io', endpoint='io')
@login_required
def io():
    return render_template('io.html')


@bp.route('/io/query', methods=['POST'])
@login_required_ajax
def query():
    cmd = request.get_data(as_text=True)

    return {
        'ans': cmd
    }
