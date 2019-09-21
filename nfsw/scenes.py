from nfsw.redis import redis as r, key as k

def get_scene(name):
    scenes = {
        'sexshop': sexshop
    }

    return scenes.get(name, None)


def current_scene():
    return get_scene(
        r().get(k('scene')).decode()
    )


def sexshop(q):
    return q  + ' you are fucked'
