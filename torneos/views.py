from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.db.models import Count

from .models import Torneo, PartidoTorneo


class TorneoListView(ListView):
    model = Torneo
    template_name = "torneos/torneo_list.html"
    context_object_name = "torneos"

    def get_queryset(self):
        return Torneo.objects.annotate(
            num_partidos=Count("partidos")
        ).order_by("-fecha_inicio")


class TorneoDetailView(DetailView):
    model = Torneo
    template_name = "torneos/torneo_detail.html"
    context_object_name = "torneo"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["partidos"] = self.object.partidos.select_related(
            "pista", "jugador1", "jugador2"
        ).order_by("fecha", "hora_inicio")
        return context
