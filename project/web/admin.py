from django.contrib import admin
from web.models.schedule import Schedule
from web.models.zone import Zone

admin.site.register([Schedule, Zone])
