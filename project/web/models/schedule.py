from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from zone import Zone

def validate_time(value):
    if value.minute % 15 != 0:
        raise ValidationError(
            'Invalid time',
            params={'value':value}
        )

class Schedule(models.Model):
    DAYS_OF_WEEK_CHOICES = [
        (0,'Monday'),
        (1,'Tuesday'),
        (2,'Wednesday'),
        (3,'Thursday'),
        (4,'Friday'),
        (5,'Saturday'),
        (6,'Sunday')
    ]

    zone_id = models.ForeignKey(Zone, on_delete=models.CASCADE)
    day_of_week = models.IntegerField(choices=DAYS_OF_WEEK_CHOICES)
    time = models.TimeField(validators=[validate_time])
    duration = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    is_active = models.BooleanField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    deleted_on = models.DateTimeField(null=True)
