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


