from django.core.cache import cache

class CacheMissError(Exception):
    pass

ZONE_STATE_CACHE_KEY = 'zone_gpio_pin_state'
CACHE_TIMEOUT = 60

def set_zones(zones_state):
    # Set the zone state dictionary in cache
    cache.set(ZONE_STATE_CACHE_KEY, zones_state, CACHE_TIMEOUT)

def set_zone(zone_id, state, task_id=None):
    # Update an individual zone state in the dictionary in cache
    cached_state = cache.get(ZONE_STATE_CACHE_KEY)
    if cached_state is None:
        raise CacheMissError(f'Could not find {ZONE_STATE_CACHE_KEY} key in cache')
    cached_state.update({zone_id:(state, task_id)})
    set_zones(cached_state)

def get_zones():
    # Return zone state dictionary from cache
    return cache.get(ZONE_STATE_CACHE_KEY)
