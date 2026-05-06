from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.views import View
from django.views.generic import ListView
from .models import Pista


class PistaListView(ListView):
    model = Pista
    template_name = "pistas/pista_list.html"
    context_object_name = "pistas"


class PistaToggleDisponibleView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_staff or (
            hasattr(self.request.user, "perfil") and self.request.user.perfil.rol == "admin"
        )

    def post(self, request, pk):
        pista = get_object_or_404(Pista, pk=pk)
        pista.disponible = not pista.disponible
        pista.save()
        estado = "disponible" if pista.disponible else "no disponible"
        messages.success(request, f"'{pista.nombre}' ahora está {estado}.")
        return redirect("pista_list")
