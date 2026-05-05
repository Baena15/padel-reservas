from django.db import models
from django.contrib.auth.models import User


class Pago(models.Model):
    CONCEPTOS = [
        ("reserva", "Reserva"),
        ("clase", "Clase"),
        ("torneo", "Torneo"),
    ]
    ESTADOS = [
        ("pendiente", "Pendiente"),
        ("pagado", "Pagado"),
        ("fallido", "Fallido"),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="pagos")
    concepto = models.CharField(max_length=20, choices=CONCEPTOS)
    referencia_id = models.PositiveIntegerField(help_text="ID de la reserva, clase o torneo")
    monto = models.DecimalField(max_digits=8, decimal_places=2)
    estado = models.CharField(max_length=20, choices=ESTADOS, default="pendiente")
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-fecha"]

    def __str__(self):
        return f"Pago {self.concepto} {self.monto}€ ({self.estado})"
