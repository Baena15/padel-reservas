from django.contrib import admin
from .models import Partido, JugadorPartido


@admin.register(Partido)
class PartidoAdmin(admin.ModelAdmin):
    list_display = ["creador", "pista", "fecha", "hora_inicio", "estado", "plazas_disponibles"]
    list_filter = ["estado", "fecha"]


@admin.register(JugadorPartido)
class JugadorPartidoAdmin(admin.ModelAdmin):
    list_display = ["partido", "jugador", "confirmado"]
