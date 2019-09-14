from nfsw.auth import login_required

from flask import (
    Blueprint, render_template
)

bp = Blueprint('io', __name__)

@bp.route('/io', endpoint='io')
@login_required
def console():
    return render_template('io.html')
