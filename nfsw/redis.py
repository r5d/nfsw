from redis import Redis

from flask import current_app, g, session

def keys():
    """List of keys used by nfsw"""
    return [
        k('log'),

        k('scene'),
        k('scene:sexshop:gg'),
        k('scenes:done'),


        k('player:type'),
        k('player:type:body'),
        k('player:type:mind'),


    ]

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
