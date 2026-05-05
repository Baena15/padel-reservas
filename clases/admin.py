from django.contrib import admin
from .models import Monitor, Clase, InscripcionClase


@admin.register(Monitor)
class MonitorAdmin(admin.ModelAdmin):
    list_display = ["user", "activo"]
    search_fields = ["user__username", "user__first_name"]


@admin.register(Clase)
class ClaseAdmin(admin.ModelAdmin):
    list_display = ["monitor", "pista", "fecha", "hora_inicio", "precio", "plazas_disponibles"]
    list_filter = ["fecha"]


@admin.register(InscripcionClase)
class InscripcionClaseAdmin(admin.ModelAdmin):
    list_display = ["clase", "alumno", "fecha_inscripcion"]
