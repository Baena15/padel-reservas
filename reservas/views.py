from django.views.generic import ListView
from .models import Reserva


class ReservaListView(ListView):
    model = Reserva
    template_name = "reservas/reserva_list.html"
    context_object_name = "reservas"
