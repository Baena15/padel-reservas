from django.db import models
from django.contrib.auth.models import User
from pistas.models import Pista


class Torneo(models.Model):
    TIPOS = [("mini", "Mini"), ("custom", "Personalizado")]
    ESTADOS = [
        ("planificado", "Planificado"),
        ("en_curso", "En curso"),
        ("finalizado", "Finalizado"),
    ]

    nombre = models.CharField(max_length=100)
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name="torneos_creados")
    tipo = models.CharField(max_length=20, choices=TIPOS)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    hora_inicio = models.TimeField(default="09:00")
    hora_fin = models.TimeField(default="14:00")
    estado = models.CharField(max_length=20, choices=ESTADOS, default="planificado")
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-fecha_inicio"]

    def __str__(self):
        return f"{self.nombre} ({self.get_tipo_display()})"


class PartidoTorneo(models.Model):
    torneo = models.ForeignKey(Torneo, on_delete=models.CASCADE, related_name="partidos")
    jugador1 = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="partidos_torneo_j1"
    )
    jugador2 = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="partidos_torneo_j2"
    )
    pista = models.ForeignKey(Pista, on_delete=models.CASCADE, related_name="partidos_torneo")
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    resultado = models.CharField(max_length=50, blank=True)

    class Meta:
        ordering = ["fecha", "hora_inicio"]

    def __str__(self):
        return f"{self.jugador1.username} vs {self.jugador2.username} ({self.torneo.nombre})"


class InscripcionTorneo(models.Model):
    torneo = models.ForeignKey(Torneo, on_delete=models.CASCADE, related_name="inscripciones")
    jugador = models.ForeignKey(User, on_delete=models.CASCADE, related_name="inscripciones_torneo")
    pareja = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True,
        related_name="inscripciones_torneo_pareja"
    )
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["torneo", "jugador"]
        ordering = ["fecha_inscripcion"]

    def __str__(self):
        return f"{self.jugador.username} en {self.torneo.nombre}"
