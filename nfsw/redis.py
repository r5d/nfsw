from redis import Redis

from flask import current_app, g, session

def redis():
    if 'redis' in g:
        return g.redis

    g.redis = Redis()

    return g.redis


def key(prefix):
    if 'user_id' in session:
        return '{}:{}'.format(prefix, session['user_id'])
    else:
        return prefix