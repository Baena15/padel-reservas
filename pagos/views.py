from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.urls import reverse

from .models import Pago


class PagoListView(LoginRequiredMixin, ListView):
    model = Pago
    template_name = "pagos/pago_list.html"
    context_object_name = "pagos"

    def get_queryset(self):
        return Pago.objects.filter(usuario=self.request.user)


@login_required
def simular_pago(request, pk):
    pago = get_object_or_404(Pago, pk=pk, usuario=request.user)
    if pago.estado == "pendiente":
        pago.estado = "pagado"
        pago.save()
        messages.success(request, "Pago realizado correctamente (simulado).")
    else:
        messages.info(request, f"El pago ya está {pago.get_estado_display()}.")
    return redirect("pago_list")


@login_required
def crear_pago_reserva(request, reserva_id):
    """Utilidad para crear un pago pendiente desde una reserva."""
    from reservas.models import Reserva
    reserva = get_object_or_404(Reserva, pk=reserva_id, usuario=request.user)
    pago, created = Pago.objects.get_or_create(
        usuario=request.user,
        concepto="reserva",
        referencia_id=reserva.pk,
        defaults={"monto": 15.00, "estado": "pendiente"},
    )
    if created:
        messages.success(request, "Se ha generado el pago de la reserva.")
    return redirect("pago_list")
