from django.views.generic import ListView
from .models import Pista


class PistaListView(ListView):
    model = Pista
    template_name = "pistas/pista_list.html"
    context_object_name = "pistas"
