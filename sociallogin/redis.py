import redis


class RedisOperation:
    red = redis.StrictRedis(host='localhost', port=6379, db=0)
