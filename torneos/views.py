from django.views.generic import ListView
from .models import Torneo


class TorneoListView(ListView):
    model = Torneo
    template_name = "torneos/torneo_list.html"
    context_object_name = "torneos"
