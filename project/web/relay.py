import web.cache as cache
import RPi.GPIO as GPIO
from enum import Enum
from django.db.models import QuerySet


class State(Enum):
    OFF = 0
    ON = 1

class InvalidPinError(Exception):
    pass

class MultipleZonesActiveError(Exception):
    pass

class RelayArray():
    """
    Base Relay Array class to control a relay array through GPIO pins.
    """
    def __init__(self, pin_numbers=[], mode=GPIO.BOARD):
        self.pins = pin_numbers
        GPIO.setmode(mode)
        for pin in self.pins:
            GPIO.setup(pin, GPIO.OUT)

    def _validate_pin(self, pin_number):
        if pin_number not in self.pins:
            raise InvalidPinError(f'Invalid pin number. Valid pins are {','.join(self.pins)}')

    def on(self, pin_number):
        self._validate_pin(pin_number)
        GPIO.output(pin_number, State.ON.value)
    
    def off(self, pin_number):
        self._validate_pin(pin_number)
        GPIO.output(pin_number, State.OFF.value)

    def clear(self):
        GPIO.cleanup()

    def get_pins_state(self):
        return {pin:State(GPIO.input(pin)).name for pin in self.pins}


class ZonalRelayArray(RelayArray):
    """
    Relay array class to control zones with caching
    """
    def __init__(self, zones:QuerySet):
        self.zones = zones
        super().__init__([zone.gpio_pin for zone in zones])
        self.get_zones_state() # Initialize cache

    def get_zones_state(self, no_cache=False):
        # Get all zones state
        if not no_cache and cache.get_zones() is not None:
            return cache.get_zones()
        
        # Read from GPIO pins
        pins_state = self.get_pins_state()
        zones_state = {zone.id: pins_state[zone.gpio_pin] for zone in self.zones}
        cache.set_zones(zones_state)
        return zones_state

    def activate_zone(self, zone_id, task_id=None):
        # Only one zone at a time can be set to ON
        for z_id, z_state in self.get_zones_state().items():
            if z_id != zone_id and z_state == State.ON.name:
                raise MultipleZonesActiveError(f'Zone {z_id} is already active')
        zone = self.zones.get(id=zone_id)
        self.on(zone.gpio_pin)
        cache.set_zone(zone_id, (State.ON.name, task_id))

    def deactivate_zone(self, zone_id):
        zone = self.zones.get(id=zone_id)
        self.off(zone.gpio_pin)
        cache.set_zone(zone_id, (State.OFF.name, None))
