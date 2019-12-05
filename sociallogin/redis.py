import redis


class RedisOperation:
    server = redis.StrictRedis(host='localhost', port=6379, db=0)
