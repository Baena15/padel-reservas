from django.urls import path
from .views import PagoListView, simular_pago, crear_pago_reserva

urlpatterns = [
    path("", PagoListView.as_view(), name="pago_list"),
    path("<int:pk>/pagar/", simular_pago, name="simular_pago"),
    path("reserva/<int:reserva_id>/crear/", crear_pago_reserva, name="crear_pago_reserva"),
]
