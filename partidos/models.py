from django.db import models
from django.contrib.auth.models import User
from pistas.models import Pista
from usuarios.constants import CATEGORIAS


class Partido(models.Model):
    ESTADOS = [("abierto", "Abierto"), ("cerrado", "Cerrado"), ("jugado", "Jugado")]

    creador = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="partidos_creados"
    )
    pista = models.ForeignKey(Pista, on_delete=models.CASCADE, related_name="partidos")
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    nivel_minimo = models.CharField(max_length=20, choices=CATEGORIAS, blank=True)
    max_jugadores = models.PositiveIntegerField(default=4)
    estado = models.CharField(max_length=20, choices=ESTADOS, default="abierto")
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-fecha", "hora_inicio"]

    def __str__(self):
        return f"Partido {self.fecha} {self.hora_inicio} ({self.estado})"

    @property
    def plazas_disponibles(self):
        return self.max_jugadores - self.jugadores.count()


class JugadorPartido(models.Model):
    partido = models.ForeignKey(Partido, on_delete=models.CASCADE, related_name="jugadores")
    jugador = models.ForeignKey(User, on_delete=models.CASCADE, related_name="partidos_unidos")
    confirmado = models.BooleanField(default=False)
    fecha_union = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["partido", "jugador"]

    def __str__(self):
        return f"{self.jugador.username} en {self.partido}"
