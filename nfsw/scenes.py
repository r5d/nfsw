from nfsw.redis import redis as r, key as k
from nfsw.util import read_junk


def get_scene(name):
    scenes = {
        'sexshop': sexshop
    }

    return scenes.get(name, None)


def current_scene():
    return get_scene(
        r().get(k('scene')).decode()
    )


def sexshop(o):
    def intro():
        return read_junk('sexshop/intro')

    def process(q):
        return ''

    if 'intro' in o:
        return intro()

    if 'q' in o:
        return process(o['q'])


