from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.views import View
from django.contrib import messages
from django.db.models import Count, Q, F

from .models import Torneo, PartidoTorneo, InscripcionTorneo
from .forms import TorneoForm, InscripcionParejaForm


def es_admin(user):
    if user.is_staff:
        return True
    return hasattr(user, "perfil") and user.perfil.rol == "admin"


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
        context["inscripciones"] = self.object.inscripciones.select_related(
            "jugador", "pareja"
        ).filter(
            Q(pareja__isnull=True) | Q(jugador__id__lt=F("pareja__id"))
        ).order_by("fecha_inscripcion")
        if self.request.user.is_authenticated:
            context["ya_inscrito"] = self.object.inscripciones.filter(
                jugador=self.request.user
            ).exists()
        else:
            context["ya_inscrito"] = False
        return context


class TorneoCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Torneo
    form_class = TorneoForm
    template_name = "torneos/torneo_form.html"
    success_url = reverse_lazy("torneo_list")

    def test_func(self):
        return es_admin(self.request.user)

    def form_valid(self, form):
        form.instance.admin = self.request.user
        return super().form_valid(form)


class TorneoInscribirView(LoginRequiredMixin, View):
    def post(self, request, pk):
        torneo = get_object_or_404(Torneo, pk=pk)
        if torneo.estado != "planificado":
            messages.error(request, "Las inscripciones para este torneo están cerradas.")
            return redirect("torneo_detail", pk=pk)
        if torneo.inscripciones.filter(jugador=request.user).exists():
            messages.warning(request, "Ya estás inscrito en este torneo.")
            return redirect("torneo_detail", pk=pk)
        InscripcionTorneo.objects.create(torneo=torneo, jugador=request.user)
        messages.success(request, "¡Te has inscrito al torneo!")
        return redirect("torneo_detail", pk=pk)


class TorneoInscribirParejaView(LoginRequiredMixin, FormView):
    template_name = "torneos/inscripcion_pareja_form.html"
    form_class = InscripcionParejaForm

    def dispatch(self, request, *args, **kwargs):
        self.torneo = get_object_or_404(Torneo, pk=self.kwargs["pk"])
        if self.torneo.estado != "planificado":
            messages.error(request, "Las inscripciones para este torneo están cerradas.")
            return redirect("torneo_detail", pk=self.torneo.pk)
        if self.torneo.inscripciones.filter(jugador=request.user).exists():
            messages.warning(request, "Ya estás inscrito en este torneo.")
            return redirect("torneo_detail", pk=self.torneo.pk)
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["torneo"] = self.torneo
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        pareja = form.cleaned_data["pareja"]
        if self.torneo.inscripciones.filter(jugador=pareja).exists():
            messages.error(self.request, "Tu pareja ya está inscrita en este torneo.")
            return redirect("torneo_detail", pk=self.torneo.pk)
        InscripcionTorneo.objects.create(torneo=self.torneo, jugador=self.request.user, pareja=pareja)
        InscripcionTorneo.objects.create(torneo=self.torneo, jugador=pareja, pareja=self.request.user)
        messages.success(self.request, f"¡Te has inscrito al torneo con {pareja.username}!")
        return redirect("torneo_detail", pk=self.torneo.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["torneo"] = self.torneo
        return context


class TorneoDesinscribirView(LoginRequiredMixin, View):
    def post(self, request, pk):
        torneo = get_object_or_404(Torneo, pk=pk)
        inscripcion = torneo.inscripciones.filter(jugador=request.user).first()
        if not inscripcion:
            messages.warning(request, "No estás inscrito en este torneo.")
            return redirect("torneo_detail", pk=pk)
        # Si tenía pareja, desinscribir también a la pareja
        if inscripcion.pareja:
            torneo.inscripciones.filter(jugador=inscripcion.pareja).delete()
        inscripcion.delete()
        messages.success(request, "Has cancelado tu inscripción al torneo.")
        return redirect("torneo_detail", pk=pk)
