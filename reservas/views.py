from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db import transaction
from datetime import timedelta
from dateutil.relativedelta import relativedelta

from .models import Reserva, ReservaRecurrente
from .forms import ReservaForm
from pagos.models import Pago


class ReservaListView(LoginRequiredMixin, ListView):
    model = Reserva
    template_name = "reservas/reserva_list.html"
    context_object_name = "reservas"

    def get_queryset(self):
        return Reserva.objects.filter(usuario=self.request.user)


class ReservaDetailView(LoginRequiredMixin, DetailView):
    model = Reserva
    template_name = "reservas/reserva_detail.html"
    context_object_name = "reserva"
    pk_url_kwarg = "pk"


class ReservaCreateView(LoginRequiredMixin, CreateView):
    model = Reserva
    form_class = ReservaForm
    template_name = "reservas/reserva_form.html"
    success_url = reverse_lazy("reserva_list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["usuario"] = self.request.user
        return kwargs

    @transaction.atomic
    def form_valid(self, form):
        form.instance.usuario = self.request.user
        form.instance.tipo = "simple"
        form.instance.hora_fin = form.cleaned_data["hora_fin"]
        resp = super().form_valid(form)

        if form.cleaned_data.get("es_recurrente"):
            duracion = form.cleaned_data.get("duracion")
            fecha_inicio = form.instance.fecha
            if duracion == "6m":
                fecha_fin = fecha_inicio + relativedelta(months=6)
            elif duracion == "1a":
                fecha_fin = fecha_inicio + relativedelta(years=1)
            else:
                fecha_fin = fecha_inicio

            ReservaRecurrente.objects.create(
                reserva_padre=self.object,
                frecuencia="semanal",
                duracion=duracion,
                fecha_fin=fecha_fin,
            )

            # Crear reservas semanales
            from datetime import timedelta
            semana = timedelta(weeks=1)
            fecha_actual = fecha_inicio + semana
            while fecha_actual <= fecha_fin:
                Reserva.objects.create(
                    usuario=self.request.user,
                    pista=self.object.pista,
                    fecha=fecha_actual,
                    hora_inicio=self.object.hora_inicio,
                    hora_fin=self.object.hora_fin,
                    tipo="recurrente",
                    estado=self.object.estado,
                )
                fecha_actual += semana

            messages.success(self.request, "Reserva recurrente creada correctamente.")
        else:
            messages.success(self.request, "Reserva creada correctamente.")

        # Generar pago pendiente por la reserva
        Pago.objects.create(
            usuario=self.request.user,
            concepto="reserva",
            referencia_id=self.object.pk,
            monto=15.00,
            estado="pendiente",
        )
        messages.info(self.request, "Se ha generado un pago de 15€ por tu reserva. Ve a 'Mis pagos' para completarlo.")
        return resp


class ReservaUpdateView(LoginRequiredMixin, UpdateView):
    model = Reserva
    form_class = ReservaForm
    template_name = "reservas/reserva_form.html"
    success_url = reverse_lazy("reserva_list")
    pk_url_kwarg = "pk"

    def get_queryset(self):
        return Reserva.objects.filter(usuario=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["usuario"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.hora_fin = form.cleaned_data["hora_fin"]
        messages.success(self.request, "Reserva actualizada.")
        return super().form_valid(form)


class ReservaDeleteView(LoginRequiredMixin, DeleteView):
    model = Reserva
    template_name = "reservas/reserva_confirm_delete.html"
    success_url = reverse_lazy("reserva_list")
    pk_url_kwarg = "pk"

    def get_queryset(self):
        return Reserva.objects.filter(usuario=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Reserva cancelada.")
        return super().delete(request, *args, **kwargs)


@login_required
def reserva_cancelar(request, pk):
    reserva = get_object_or_404(Reserva, pk=pk, usuario=request.user)
    if reserva.estado != "cancelada":
        reserva.estado = "cancelada"
        reserva.save()
        messages.success(request, "Reserva cancelada.")
    else:
        messages.info(request, "La reserva ya estaba cancelada.")
    return redirect("reserva_list")
