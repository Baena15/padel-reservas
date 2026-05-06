from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.db.models import Count, Q
from datetime import date

from .models import Partido, JugadorPartido
from .forms import PartidoForm


class PartidoListView(ListView):
    model = Partido
    template_name = "partidos/partido_list.html"
    context_object_name = "partidos"

    def get_queryset(self):
        queryset = Partido.objects.annotate(
            num_jugadores=Count("jugadores")
        ).order_by("-fecha", "hora_inicio")
        filtro = self.request.GET.get("filtro", "abiertos")
        if filtro == "abiertos":
            queryset = queryset.filter(estado="abierto", fecha__gte=date.today())
        elif filtro == "mis_partidos" and self.request.user.is_authenticated:
            queryset = queryset.filter(
                Q(creador=self.request.user) | Q(jugadores__jugador=self.request.user)
            ).distinct()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filtro"] = self.request.GET.get("filtro", "abiertos")
        if self.request.user.is_authenticated:
            context["mis_partidos_ids"] = JugadorPartido.objects.filter(
                jugador=self.request.user
            ).values_list("partido_id", flat=True)
        else:
            context["mis_partidos_ids"] = []
        return context


class PartidoDetailView(DetailView):
    model = Partido
    template_name = "partidos/partido_detail.html"
    context_object_name = "partido"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["jugadores"] = self.object.jugadores.select_related("jugador")
        if self.request.user.is_authenticated:
            context["ya_unido"] = self.object.jugadores.filter(
                jugador=self.request.user
            ).exists()
            context["es_creador"] = self.object.creador == self.request.user
        else:
            context["ya_unido"] = False
            context["es_creador"] = False
        return context


class PartidoCreateView(LoginRequiredMixin, CreateView):
    model = Partido
    form_class = PartidoForm
    template_name = "partidos/partido_form.html"
    success_url = reverse_lazy("partido_list")

    def form_valid(self, form):
        form.instance.creador = self.request.user
        form.instance.hora_fin = form.cleaned_data["hora_fin"]
        resp = super().form_valid(form)
        # El creador se une automáticamente como confirmado
        JugadorPartido.objects.create(
            partido=self.object, jugador=self.request.user, confirmado=True
        )
        messages.success(self.request, "Partido creado. ¡Ya estás apuntado!")
        return resp


@login_required
def unirse_partido(request, pk):
    partido = get_object_or_404(Partido, pk=pk)
    if partido.fecha < date.today():
        messages.error(request, "No puedes unirte a un partido pasado.")
        return redirect("partido_list")
    if partido.estado != "abierto":
        messages.error(request, "Este partido ya no está abierto.")
        return redirect("partido_list")
    if partido.jugadores.filter(jugador=request.user).exists():
        messages.info(request, "Ya estás en este partido.")
        return redirect("partido_detail", pk=pk)
    if partido.plazas_disponibles <= 0:
        messages.error(request, "El partido está completo.")
        return redirect("partido_list")
    JugadorPartido.objects.create(partido=partido, jugador=request.user)
    # Si se llena, cerrar partido
    if partido.plazas_disponibles <= 0:
        partido.estado = "cerrado"
        partido.save()
    messages.success(request, "Te has unido al partido.")
    return redirect("partido_detail", pk=pk)


@login_required
def abandonar_partido(request, pk):
    partido = get_object_or_404(Partido, pk=pk)
    jugador = partido.jugadores.filter(jugador=request.user).first()
    if jugador:
        jugador.delete()
        if partido.estado == "cerrado":
            partido.estado = "abierto"
            partido.save()
        messages.success(request, "Has abandonado el partido.")
    else:
        messages.info(request, "No estabas en este partido.")
    return redirect("partido_detail", pk=pk)


@login_required
def cerrar_partido(request, pk):
    partido = get_object_or_404(Partido, pk=pk, creador=request.user)
    partido.estado = "cerrado"
    partido.save()
    messages.success(request, "Partido cerrado.")
    return redirect("partido_detail", pk=pk)
