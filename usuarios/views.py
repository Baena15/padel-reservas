from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .forms import RegistroForm, PerfilUpdateForm


def registro_view(request):
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "¡Cuenta creada correctamente!")
            return redirect("home")
    else:
        form = RegistroForm()
    return render(request, "usuarios/registro.html", {"form": form})


@login_required
def perfil_view(request):
    return render(request, "usuarios/perfil.html", {"perfil": request.user.perfil})


@login_required
def perfil_editar_view(request):
    if request.method == "POST":
        form = PerfilUpdateForm(request.POST, request.FILES, instance=request.user.perfil)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil actualizado correctamente.")
            return redirect("perfil")
    else:
        form = PerfilUpdateForm(instance=request.user.perfil)
    return render(request, "usuarios/perfil_editar.html", {"form": form})
