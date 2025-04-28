import os
import redis
import logging

logger = logging.getLogger(__name__)

def get_redis_connection():
    redis_url = os.getenv("REDIS_URL")
    if not redis_url:
        logger.error("REDIS_URL is not set in environment variables")
        raise ValueError("REDIS_URL is not set")
    
    try:
        r = redis.Redis.from_url(redis_url)
        # Test the connection
        r.ping()
        return r
    except redis.ConnectionError as e:
        logger.error(f"Failed to connect to Redis: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error connecting to Redis: {str(e)}")
        raise

def increment_counter() -> int:
    try:
        r = get_redis_connection()
        new_count = int(r.incr("puzzlepull_counter"))
        logger.info(f"Counter incremented to: {new_count}")
        return new_count
    except Exception as e:
        logger.error(f"Error incrementing counter: {str(e)}")
        raise

def get_counter() -> int:
    try:
        r = get_redis_connection()
        count = r.get("puzzlepull_counter")
        if count is None:
            logger.warning("Counter key not found in Redis, initializing to 0")
            return 0
        return int(count)
    except Exception as e:
        logger.error(f"Error getting counter: {str(e)}")
        raise
