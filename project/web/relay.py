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
    # Base Relay Array. Control a relay array through GPIO pins.
    def __init__(self, pin_numbers=[], mode=GPIO.BOARD):
        self.pins = pin_numbers
        GPIO.setmode(mode)
        for pin in self.pins:
            GPIO.setup(pin, GPIO.output)
        GPIO.cleanup()

    def _validate_pin(self, pin_number):
        if pin_number not in self.pins:
            raise InvalidPinError(f'Invalid pin number. Valid pins are {','.join(self.pins)}')

    def on(self, pin_number):
        self._validate_pin(pin_number)
        GPIO.output(pin_number, State.ON.value)
    
    def off(self, pin_number):
        self._validate_pin(pin_number)
        GPIO.output(pin_number, State.OFF.value)

    def get_pins_state(self):
        return {pin:State(GPIO.input(pin)).name for pin in self.pins}


class ZonalRelayArray(RelayArray):
    # Relay to control zones with cache update
    def __init__(self, zones:QuerySet):
        self.zones = zones
        cache.set_zones(self.get_zones_state()) # Initialize
        super().__init__([zone.gpio_pin for zone in zones])

    def get_zones_state(self):
        # Get all zones state
        pins_state = self.get_pins_state()
        return {zone.id: pins_state[zone.gpio_pin] for zone in self.zones}

    def activate_zone(self, zone_id):
        # Only one zone at a time can be set to ON
        for z_id, z_state in self.get_zones_state():
            if z_id != zone_id and z_state == State.ON.name:
                raise MultipleZonesActiveError(f'Zone {z_id} is already active')
        zone = self.zones.get(id=zone_id)
        self.on(zone.gpio_pin)
        cache.set_zone(zone_id, State.ON.name)

    def deactivate_zone(self, zone_id):
        zone = self.zones.get(id=zone_id)
        self.off(zone.gpio_pin)
        cache.set_zone(zone_id, State.OFF.name)
