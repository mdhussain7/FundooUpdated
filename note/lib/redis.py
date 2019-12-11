import redis


class RedisOperation:
    server = redis.StrictRedis(host='localhost', port=6379, db=0)


red = RedisOperation.server


# User Defined Redis Cache
class Cache:

    def __init__(self):
        self.host = 'localhost'
        self.port = 6379
        self.db = 0

    def connection(self):
        host = 'localhost'
        port = 6379
        db = 0

        try:
            redis_con = redis.StrictRedis(host=host, port=port, db=db)
            ping = redis_con.ping()

        except NameError:
            return {'error': 'cannot import redis library'}
        except ConnectionError as e:
            return {'error': str(e)}

        return {
            'ping': ping,
            'version': redis_con.info().get('redis_version')
        }

    def set(self, key, value):
        value = red.set(key, value)
        return value

    def get(self, key):
        value = red.get(key)
        return value

    def delete(self, key):
        value = red.delete(key)
        return value

    def rpush(self, key, value):
        value = red.rpush(key, value)
        return value

    def hmset(self, key, value):
        value = red.hmset(key, value)
        return value

    def hget(self, key):
        value = red.hget(key)
        return value

    def hvals(self, key):
        value = red.hvals(key)
        return value
