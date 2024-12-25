from django.core.cache import cache

class CacheMissError(Exception):
    pass

ZONE_STATE_CACHE_KEY = 'zone_gpio_pin_state'

def set_zones(zones_state):
    cache.set(ZONE_STATE_CACHE_KEY, zones_state)

def set_zone(zone_id, state):
    cached_state = cache.get(ZONE_STATE_CACHE_KEY)
    if cached_state is None:
        raise CacheMissError(f'Could not find {ZONE_STATE_CACHE_KEY} key in cache')
    cached_state.update({zone_id:state})
    set_zones(cached_state)

def get_zones():
    return cache.get(ZONE_STATE_CACHE_KEY)
