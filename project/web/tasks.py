from celery import shared_task
from web.models.schedule import Schedule
from web.models.zone import Zone
from web.relay import ZonalRelayArray, MultipleZonesActiveError
import web.cache as cache
import time
import logging

LOG = logging.getLogger(__name__)

def format_zone(id, number=None, name=None):
    return f'{id}/{number}-{name}'

@shared_task
def run_zone(zone_id, duration):
    # Run a zone for a set amount of time
    zones = Zone.get_all()
    relay = ZonalRelayArray(zones)
    try:
        zone = zones.get(id=zone_id)
        LOG.info(f'Running zone {format_zone(zone_id, zone.number, zone.name)}')
        relay.activate_zone(zone_id)
    except MultipleZonesActiveError:
        LOG.exception('Multiple zones are active. Aborting')
        return
    # Blocking the task and the queue
    time.sleep(duration * 60)
    
    relay.deactivate_zone(zone_id)
    LOG.info(f'Zone {format_zone(zone_id, zone.number, zone.name)} has finished running')

@shared_task
def run_schedules():
    # Queue schedules to run
    LOG.info('Checking for schedules')
    schedules = Schedule.get_schedules_to_run()
    for schedule in schedules:
        LOG.info(f'Scheduling zone {format_zone(schedule.zone.id, schedule.zone.number, schedule.zone.name)} to run for {schedule.duration} minutes')
        run_zone.apply_async(schedule.zone.id, schedule.duration)
