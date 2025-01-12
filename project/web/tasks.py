from celery import shared_task
from web.models.schedule import Schedule
from web.models.zone import Zone
from web.relay import ZonalRelayArray, MultipleZonesActiveError
import web.cache as cache
import time
import logging

LOG = logging.getLogger(__name__)
SECONDS_IN_MINUTE = 60

@shared_task(bind=True)
def activate_zone(self, zone_id, duration):
    # Run a zone for a set amount of time
    zones = Zone.get_all()
    relay = ZonalRelayArray(zones)
    try:
        zone = zones.get(id=zone_id)
        LOG.info(f'Running zone {str(zone)}')
        relay.activate_zone(zone_id)
    except MultipleZonesActiveError:
        LOG.exception('Multiple zones are active. Aborting')
        return
    # Blocking the task and the queue
    time.sleep(duration * SECONDS_IN_MINUTE)
    
    relay.deactivate_zone(zone_id)
    LOG.info(f'Zone {str(zone)} has finished running')

@shared_task
def run_schedules():
    # Queue schedules to run
    LOG.info('Checking for schedules')
    schedules = Schedule.get_schedules_to_run()
    for schedule in schedules:
        LOG.info(f'Scheduling zone {str(schedule.zone)} to run for {schedule.duration} minutes')
        activate_zone.delay(schedule.zone.id, schedule.duration)
