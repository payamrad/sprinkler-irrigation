from django.views.generic import TemplateView, DetailView
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404
from web.models.zone import Zone
import web.cache as cache



class ZoneCreateView(TemplateView):
    template_name = 'web/zone.html'

    def post(self, request, *args, **kwargs):
        data = request.POST
        zone = Zone()
        zone.number = data.get('number')
        zone.name = data.get('name')
        zone.gpio_pin = data.get('gpio_pin')
        zone.save()
        cache.invalidate()
        
        return HttpResponseRedirect(reverse('homepage'))

class ZoneUpdateView(TemplateView):
    template_name = 'web/zone.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['zone'] = Zone.objects.get(id=kwargs.get('id'))
        return context
    
    def post(self, request, *args, **kwargs):
        data = request.POST
        zone = get_object_or_404(Zone, id=kwargs.get('id'))
        zone.number = data.get('number')
        zone.name = data.get('name')
        zone.gpio_pin = data.get('gpio_pin')
        zone.is_active = True if data.get('is_active') else False
        zone.save()
        cache.invalidate()
        
        return HttpResponseRedirect(reverse('homepage'))
    