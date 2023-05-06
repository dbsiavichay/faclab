from functools import reduce

from django.core.cache import cache


class CacheService:
    @classmethod
    def get(cls, cache_id):
        try:
            return cache.get(cache_id)
        except Exception:
            return None

    @classmethod
    def set(cls, cache_id, value, cache_ttl=None):
        cache.set(cache_id, value, cache_ttl)

    @classmethod
    def delete(cls, cache_id):
        cache.delete(cache_id)

    @classmethod
    def generate_key(cls, key, complementary_keys, **kwargs):
        cache_key = key

        cache_key = (
            reduce(
                lambda acc, c_key: "{0}_{1}".format(acc, kwargs[c_key]),
                complementary_keys,
                cache_key,
            )
            .replace(" ", "_")
            .replace(",", "_")
        )

        return cache_key

    def set_cache(self, key: str, complementary_keys=[], cache_ttl=None):
        """
        It caches the response of the decorated function:
        - `key` (required): main unique string.
        - `complementary_keys`: It expects a string array that matches the key_arguments
        of your decorated function.
        """

        def decorator(function):
            def wrapper(*args, **kwargs):
                cache_key = self.generate_key(key, complementary_keys, **kwargs)
                cached_result = self.get(cache_key)

                if cached_result is None:
                    cached_result = function(*args, **kwargs)
                    self.set(cache_key, cached_result, cache_ttl)

                return cached_result

            return wrapper

        return decorator
