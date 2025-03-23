import os
import redis

def increment_counter() -> int:
    redis_url = os.getenv("REDIS_URL")

    if not redis_url:
        raise ValueError("REDIS_URL is not set")

    r = redis.Redis.from_url(redis_url)
    new_count = int(r.incr("puzzlepull_counter"))
    return new_count

def get_counter() -> int:
    redis_url = os.getenv("REDIS_URL")

    if not redis_url:
        raise ValueError("REDIS_URL is not set")

    r = redis.Redis.from_url(redis_url)
    return int(r.get("puzzlepull_counter"))
