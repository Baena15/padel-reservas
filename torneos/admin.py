from django.contrib import admin
from .models import Torneo, PartidoTorneo, InscripcionTorneo


class PartidoTorneoInline(admin.TabularInline):
    model = PartidoTorneo
    extra = 0


class InscripcionTorneoInline(admin.TabularInline):
    model = InscripcionTorneo
    extra = 0


@admin.register(Torneo)
class TorneoAdmin(admin.ModelAdmin):
    list_display = ["nombre", "tipo", "fecha_inicio", "fecha_fin", "estado"]
    list_filter = ["tipo", "estado"]
    inlines = [InscripcionTorneoInline, PartidoTorneoInline]


@admin.register(PartidoTorneo)
class PartidoTorneoAdmin(admin.ModelAdmin):
    list_display = ["torneo", "jugador1", "jugador2", "pista", "fecha", "resultado"]


@admin.register(InscripcionTorneo)
class InscripcionTorneoAdmin(admin.ModelAdmin):
    list_display = ["torneo", "jugador", "pareja", "fecha_inscripcion"]
    list_filter = ["torneo"]
