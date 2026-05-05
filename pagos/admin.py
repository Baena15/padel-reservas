from django.contrib import admin
from .models import Pago


@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ["usuario", "concepto", "monto", "estado", "fecha"]
    list_filter = ["concepto", "estado"]
