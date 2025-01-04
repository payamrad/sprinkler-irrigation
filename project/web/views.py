from django.shortcuts import render
from web.models.zone import Zone
from web.relay import ZonalRelayArray

def index(request):
    zones = Zone.get_all()
    relay = ZonalRelayArray(zones)
    zones_state = relay.get_zones_state()
    
    context = {
        zones: zones,
        zones_state: zones_state
        }

    return render(request, 'web/index.html', context)
