from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.contrib.auth import get_user_model

User = get_user_model()

CACHE_TTL = 84400


def get_user_by_id_from_cache(user_id):
    cache_key = f"user_{user_id}"
    user = cache.get(cache_key)

    if user is None:
        try:
            user = User.objects.get(id=user_id)

            cache.set(cache_key, user, timeout=CACHE_TTL)
        except Exception as e:
            return f"에러가 발생했습니다: {e}"

    return user
