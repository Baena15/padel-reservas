from django.db import models
from django.contrib.auth.models import User
from pistas.models import Pista


class Reserva(models.Model):
    TIPOS = [("simple", "Simple"), ("recurrente", "Recurrente")]
    ESTADOS = [("pendiente", "Pendiente"), ("confirmada", "Confirmada"), ("cancelada", "Cancelada")]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reservas")
    pista = models.ForeignKey(Pista, on_delete=models.CASCADE, related_name="reservas")
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    tipo = models.CharField(max_length=20, choices=TIPOS, default="simple")
    estado = models.CharField(max_length=20, choices=ESTADOS, default="pendiente")
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-fecha", "hora_inicio"]

    def __str__(self):
        return f"Reserva {self.usuario.username} - {self.pista} {self.fecha} {self.hora_inicio}"


class ReservaRecurrente(models.Model):
    FRECUENCIAS = [("semanal", "Semanal")]
    DURACIONES = [("6m", "6 Meses"), ("1a", "1 Año")]

    reserva_padre = models.ForeignKey(Reserva, on_delete=models.CASCADE, related_name="recurrentes")
    frecuencia = models.CharField(max_length=20, choices=FRECUENCIAS, default="semanal")
    duracion = models.CharField(max_length=20, choices=DURACIONES)
    fecha_fin = models.DateField()

    def __str__(self):
        return f"Recurrente {self.get_frecuencia_display()} hasta {self.fecha_fin}"
