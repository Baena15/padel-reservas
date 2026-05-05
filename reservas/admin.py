from django.contrib import admin
from .models import Reserva, ReservaRecurrente


@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ["usuario", "pista", "fecha", "hora_inicio", "tipo", "estado"]
    list_filter = ["tipo", "estado", "fecha"]
    search_fields = ["usuario__username", "pista__nombre"]


@admin.register(ReservaRecurrente)
class ReservaRecurrenteAdmin(admin.ModelAdmin):
    list_display = ["reserva_padre", "frecuencia", "duracion", "fecha_fin"]
