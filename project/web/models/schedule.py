from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from web.models.zone import Zone
from datetime import datetime

MINUTE_STEP = 5

def validate_time(value):
    if value.minute % MINUTE_STEP != 0:
        raise ValidationError(
            'Invalid time',
            params={'value':value}
        )
    
class Schedule(models.Model):
    """
    A schedule is a time and duration when a zone should be activated
    """
    DAYS_OF_WEEK_CHOICES = [
        (0,'Monday'),
        (1,'Tuesday'),
        (2,'Wednesday'),
        (3,'Thursday'),
        (4,'Friday'),
        (5,'Saturday'),
        (6,'Sunday')
    ]

    zone = models.ForeignKey(Zone, on_delete=models.CASCADE)
    day_of_week = models.IntegerField(choices=DAYS_OF_WEEK_CHOICES)
    time = models.TimeField(validators=[validate_time])
    duration = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    deleted_on = models.DateTimeField(default= None, blank=True, null=True)

    def __str__(self, weekdays = DAYS_OF_WEEK_CHOICES):
        _, weekday = weekdays[self.day_of_week]
        return ' '.join(['id:', str(self.id), ', zone:', self.zone.name, ', schduled on', weekday, str(self.time), ' for', str(self.duration), 'minutes'])

    @staticmethod
    def get_schedules_to_run():
        now = datetime.today()
        return Schedule.objects.select_related('zone') \
                    .filter(is_active=True, zone__is_active=True, deleted_on__isnull=True, day_of_week=now.weekday(), time__hour=now.hour, time__minute=now.minute)
    