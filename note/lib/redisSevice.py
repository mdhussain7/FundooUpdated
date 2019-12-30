import redis
# import redis
#
#
# class RedisOperation:
#     redis = redis.StrictRedis(host='redis', port=6379, db=0)


# User Defined Redis Cache
class Cache:

    def __init__(self, host='redis', port=6379, db=0):
        self.host = host
        self.port = port
        self.db = db
        self.username = ''
        self.password = ''

    def connect(self):
        try:
            self.red = redis.StrictRedis(host=self.host, port=self.port, db=self.db)
            # ping = self.red.ping()

        except NameError:
            return {'error': 'cannot import redis library'}
        except ConnectionError as e:
            return {'error': str(e)}
        return self.red

    def set(self, key, value):
        self.red.set(key, value)

    def get(self, key):
        value = self.red.get(key)
        return key

    def delete(self, key):
        self.red.delete(key)

    def rpush(self, key, value):
        self.red.rpush(key, value)

    def hmset(self, key, value):
        self.red.hmset(key, value)

    def hget(self, key):
        value = self.red.hget(key)
        return value

    def hvals(self, key):
        value = self.red.hvals(key)
        return value
