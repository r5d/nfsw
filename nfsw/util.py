import os

from flask import current_app

def read_junk(key):
    r = os.path.join('junk', key)

    with current_app.open_resource(r) as f:
        return f.read().decode()
