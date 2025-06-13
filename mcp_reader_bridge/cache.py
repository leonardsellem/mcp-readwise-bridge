from cachetools import TTLCache
from functools import wraps
import json

def cached_ttl(ttl: int, maxsize: int = 128):
    cache = TTLCache(maxsize=maxsize, ttl=ttl)
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                key = (func.__name__, json.dumps(args, default=str), json.dumps(kwargs, sort_keys=True, default=str))
            except Exception:
                key = (func.__name__, str(args), str(kwargs))
            if key in cache:
                return cache[key]
            result = await func(*args, **kwargs)
            cache[key] = result
            return result
        wrapper.cache_clear = cache.clear
        return wrapper
    return decorator
