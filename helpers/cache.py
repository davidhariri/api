import redis
import pickle
import os
from functools import wraps
import hashlib

cache = redis.StrictRedis(os.getenv("REDIS_URI", None))


def cached(expiry=24 * 60 * 60, namespace=None, debug=False):
    """
    Decorator function that can be used to cache the result of a
    function
    """
    def decorator(function):
        @wraps(function)
        def func(*args, **kwargs):
            args_list = map(lambda k: (k, kwargs[k]), kwargs.keys())
            args_key = str(pickle.dumps(sorted(list(args_list))))

            if debug:
                print(">> CACHE:ARGS:", [kwargs])

            cache_key = "{namespace}:{hash}".format(
                namespace=namespace or function.__name__,
                hash=hashlib.md5(args_key.encode("utf-8")).hexdigest()
            )

            try:
                cache_result = cache.get(cache_key)
            except Exception:
                cache_result = None

            # If the result was None, we need to evaluate the function
            if not cache_result:
                if debug:
                    print(">> CACHE:MISS: ", cache_key)

                func_result = function(*args, **kwargs)

                # Save the result to the cache
                cache.setex(cache_key, expiry, pickle.dumps(func_result))
            else:
                if debug:
                    print(">> CACHE:HIT: ", cache_key)

                func_result = pickle.loads(cache_result)

            return func_result
        return func
    return decorator
