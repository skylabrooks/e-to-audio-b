import redis
import json
import hashlib
import logging
from typing import Optional, Any
from functools import wraps
import os

logger = logging.getLogger(__name__)

class CacheManager:
    def __init__(self):
        redis_url = os.environ.get('REDIS_URL', 'redis://localhost:6379')
        try:
            self.redis_client = redis.from_url(redis_url, decode_responses=True)
            self.redis_client.ping()
            self.enabled = True
            logger.info("Redis cache enabled")
        except Exception as e:
            logger.warning(f"Redis unavailable, caching disabled: {e}")
            self.redis_client = None
            self.enabled = False
    
    def get(self, key: str) -> Optional[Any]:
        if not self.enabled:
            return None
        try:
            data = self.redis_client.get(key)
            return json.loads(data) if data else None
        except Exception as e:
            logger.error(f"Cache get error: {e}")
            return None
    
    def set(self, key: str, value: Any, ttl: int = 3600):
        if not self.enabled:
            return
        try:
            self.redis_client.setex(key, ttl, json.dumps(value))
        except Exception as e:
            logger.error(f"Cache set error: {e}")
    
    def delete(self, key: str):
        if not self.enabled:
            return
        try:
            self.redis_client.delete(key)
        except Exception as e:
            logger.error(f"Cache delete error: {e}")

cache = CacheManager()

def cached(ttl: int = 3600, key_prefix: str = ""):
    """Decorator for caching function results."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generate cache key
            key_data = f"{key_prefix}:{func.__name__}:{str(args)}:{str(sorted(kwargs.items()))}"
            cache_key = hashlib.md5(key_data.encode()).hexdigest()
            
            # Try to get from cache
            result = cache.get(cache_key)
            if result is not None:
                logger.debug(f"Cache hit for {func.__name__}")
                return result
            
            # Execute function and cache result
            result = func(*args, **kwargs)
            cache.set(cache_key, result, ttl)
            logger.debug(f"Cache miss for {func.__name__}, result cached")
            return result
        return wrapper
    return decorator