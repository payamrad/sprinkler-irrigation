from django.db import models

class Zone(models.Model):
    number = models.IntegerField()
    name = models.TextField()
    is_active = models.BooleanField()
    gpio_pin = models.IntegerField(null=True, unique=True)
