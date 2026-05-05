from django.contrib import admin
from .models import Torneo, PartidoTorneo


@admin.register(Torneo)
class TorneoAdmin(admin.ModelAdmin):
    list_display = ["nombre", "tipo", "fecha_inicio", "fecha_fin", "estado"]
    list_filter = ["tipo", "estado"]


@admin.register(PartidoTorneo)
class PartidoTorneoAdmin(admin.ModelAdmin):
    list_display = ["torneo", "jugador1", "jugador2", "pista", "fecha", "resultado"]
