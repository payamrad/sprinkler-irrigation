from django.db import models

class Zone(models.Model):
    number = models.IntegerField(null=True)
    name = models.TextField(null=True)
    gpio_pin = models.IntegerField(unique=True)
    is_active = models.BooleanField(default=True)
        
    @staticmethod
    def get_all():
        return Zone.objects.all()
