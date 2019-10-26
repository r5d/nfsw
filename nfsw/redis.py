from redis import Redis

from flask import current_app, g, session


def redis():
    if 'redisc' in g:
        return g.redisc

    g.redisc = RedisC()

    return g.redisc


class RedisC:
    r = None

    def __init__(self):
        self.r = Redis()


    def keys(self):
        return [
            'log',

            'scene',
            'scene:sexshop:gg',
            'scene:garden:gg',
            'scene:nymphomaniac:gg',
            'scene:nymphomaniac:gg-hunk',
            'scene:coitus:gg',
            'scene:coitus:fucked',
            'scene:strayed:gg',
            'scene:xkcd:gg',
            'scenes:done',

            'player:type',
            'player:type:body',
            'player:type:mind',
        ]



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
