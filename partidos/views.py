from django.views.generic import ListView
from .models import Partido


class PartidoListView(ListView):
    model = Partido
    template_name = "partidos/partido_list.html"
    context_object_name = "partidos"
