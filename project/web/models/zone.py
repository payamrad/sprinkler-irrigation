from django.db import models

class Zone(models.Model):
    number = models.IntegerField(null=True)
    name = models.TextField(null=True)
    gpio_pin = models.IntegerField(unique=True)
    is_active = models.BooleanField(default=True)
        
    def __str__(self):
        number_text = f', number: {self.number}' if self.number is not None else None
        name_text = f', name: {self.name}' if self.name is not None else None
        return ''.join(filter(lambda x: x is not None, ['id: ', str(self.id), number_text, name_text]))
    
    @staticmethod
    def get_all():
        return Zone.objects.all()
