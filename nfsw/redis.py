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

def key(prefix):
    if 'user_id' in session:
        return '{}:{}'.format(prefix, session['user_id'])
    else:
        return prefix


def redisc():
    if 'redisc' in g:
        return g.redisc

    g.redisc = RedisC()

    return g.redisc


class RedisC:
    r = None

    def __init__(self):
        self.r = Redis()


    def key(self, k):
        if 'user_id' in session:
            return '{}:{}'.format(k, session['user_id'])
        else:
            return k


    def exists(self, k):
        k = self.key(k)

        return self.r.exists(k)


    def set(self, k, v):
        k = self.key(k)

        return self.r.set(k, v)


    def get(self, k):
        k = self.key(k)

        return self.r.get(k)


    def delete(self, k):
        k = self.key(k)

        return self.r.delete(k)


    def rpush(self, k, v):
        k = self.key(k)

        return self.r.rpush(k, v)


    def sadd(self, k, v):
        k = self.key(k)

        return self.r.sadd(k, v)


    def sismember(self, k, v):
        k = self.key(k)

        return self.r.sismember(k, v)
