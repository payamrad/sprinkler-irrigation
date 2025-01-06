from django.views.generic import TemplateView
from web.models.zone import Zone
from web.relay import ZonalRelayArray

class HomePageView(TemplateView):
    template_name = 'web/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['zones'] = Zone.get_all()
        context['zones_state'] = ZonalRelayArray(context['zones']).get_zones_state()
        return context
    