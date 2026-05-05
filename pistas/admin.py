from django.contrib import admin
from .models import Pista, Bloqueo


@admin.register(Pista)
class PistaAdmin(admin.ModelAdmin):
    list_display = ["nombre", "tipo", "disponible"]
    list_filter = ["tipo", "disponible"]


@admin.register(Bloqueo)
class BloqueoAdmin(admin.ModelAdmin):
    list_display = ["pista", "fecha_inicio", "fecha_fin", "motivo"]
    list_filter = ["pista"]
