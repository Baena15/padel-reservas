from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.db.models import Count, Q
from datetime import date

from .models import Clase, InscripcionClase
from pagos.models import Pago


class ClaseListView(ListView):
    model = Clase
    template_name = "clases/clase_list.html"
    context_object_name = "clases"

    def get_queryset(self):
        queryset = Clase.objects.filter(fecha__gte=date.today()).order_by("fecha", "hora_inicio")
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context["mis_inscripciones"] = InscripcionClase.objects.filter(
                alumno=self.request.user
            ).values_list("clase_id", flat=True)
        else:
            context["mis_inscripciones"] = []
        return context


class ClaseDetailView(DetailView):
    model = Clase
    template_name = "clases/clase_detail.html"
    context_object_name = "clase"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["inscritos"] = self.object.inscripciones.select_related("alumno")
        if self.request.user.is_authenticated:
            context["ya_inscrito"] = self.object.inscripciones.filter(
                alumno=self.request.user
            ).exists()
        else:
            context["ya_inscrito"] = False
        return context


@login_required
def inscribir_clase(request, pk):
    clase = get_object_or_404(Clase, pk=pk)
    if clase.fecha < date.today():
        messages.error(request, "No puedes inscribirte a una clase pasada.")
        return redirect("clase_list")
    if clase.inscripciones.filter(alumno=request.user).exists():
        messages.info(request, "Ya estás inscrito en esta clase.")
        return redirect("clase_detail", pk=pk)
    if clase.plazas_disponibles <= 0:
        messages.error(request, "Esta clase ya no tiene plazas disponibles.")
        return redirect("clase_list")
    InscripcionClase.objects.create(clase=clase, alumno=request.user)
    if clase.precio and clase.precio > 0:
        Pago.objects.create(
            usuario=request.user,
            concepto="clase",
            referencia_id=clase.pk,
            monto=clase.precio,
            estado="pendiente",
        )
        messages.info(request, f"Se ha generado un pago de {clase.precio}€ por la clase. Ve a 'Mis pagos' para completarlo.")
    messages.success(request, f"Te has inscrito en la clase del {clase.fecha}.")
    return redirect("clase_detail", pk=pk)


@login_required
def desinscribir_clase(request, pk):
    clase = get_object_or_404(Clase, pk=pk)
    inscripcion = clase.inscripciones.filter(alumno=request.user).first()
    if inscripcion:
        inscripcion.delete()
        messages.success(request, "Te has desinscrito de la clase.")
    else:
        messages.info(request, "No estabas inscrito en esta clase.")
    return redirect("clase_detail", pk=pk)
