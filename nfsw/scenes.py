from nfsw.redis import redis as r, redisc, key as k
from nfsw.util import read_junk


def get_scene(name):
    scenes = {
        'sexshop': sexshop,
        'garden': garden
    }

    return scenes.get(name, None)


def current_scene():
    r = redisc()

    return get_scene(
        r.get('scene').decode()
    )


def sexshop(o):
    r = redisc()

    gobbledygook = [
        'I just got raped in the'
        '\narse by 9238 sentinels.'
        '\nPlease don\'t fuck with me like that'
        '\n\nIt\'s easy.'
        ]


    def rj(name):
        return read_junk('sexshop/{}'.format(name))


    def gg():
        l = len(gobbledygook)

        for i in range(0, l):
            if r.sismember('scene:sexshop:gg', i):
                continue

            r.sadd('scene:sexshop:gg', i)
            return gobbledygook[i]

        return 'I\'m outta words.'


    def intro():
        return rj('intro')


    def p_done(q):
        if r.sismember('scenes:done', 'sexshop'):
            return rj('done')

        # Set player type.
        type = '{}{}'.format(r.get('player:type:body').decode(),
                             r.get('player:type:mind').decode())
        r.set('player:type', type)

        # Mark scene done
        r.sadd('scenes:done', 'sexshop')

        # Move to next scene
        r.set('scene', 'garden')

        return garden({'intro': 1})


    def p_body(q):
        if 'female' in q:
            r.set('player:type:body', 'f')

            return '\n\n'.join([
                rj('body-f-done'),
                rj('mind-q')
            ])

        if 'male' in q:
            r.set('player:type:body', 'm')

            return '\n\n'.join([
                rj('body-m-done'),
                rj('mind-q')
            ])

        return '\n'.join([gg(), rj('body-q')])


    def p_mind(q):
        if 'women' in q:
            r.set('player:type:mind', 'w')

            return '\n\n'.join([
                rj('mind-f-done'),
                p_done(q)
            ])

        if 'men' in q:
            r.set('player:type:mind', 'm')

            return '\n\n'.join([
                rj('mind-m-done'),
                p_done(q)
            ])

        return '\n'.join([gg(), rj('mind-q')])


    def p(q):
        if r.exists('player:type'):
            return p_done(q)

        if not r.exists('player:type:body'):
            return p_body(q)

        if not r.exists('player:type:mind'):
            return p_mind(q)

        return p_done(q)


    if 'intro' in o:
        return intro()

    if 'q' in o:
        return p(o['q'])


def garden(o):
    return 'The Garden'
