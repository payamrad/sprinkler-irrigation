from django.db import models

class Zone(models.Model):
    number = models.IntegerField()
    name = models.TextField()
    gpio_pin = models.IntegerField(null=True, unique=True)
