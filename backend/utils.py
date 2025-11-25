import redis


def get_redis_connector() -> redis.Redis:
    REDIS_HOSTNAME = 'localhost'
    REDIS_PORT = 6379

    r = redis.StrictRedis(host=REDIS_HOSTNAME, port=REDIS_PORT, db=0, encoding="utf-8", decode_responses=True)
    r.ping()
    return r