from django.db import models
from django.contrib.auth.models import User
from pistas.models import Pista


class Monitor(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={"perfil__rol": "monitor"},
        related_name="monitor",
    )
    bio = models.TextField(blank=True)
    foto = models.ImageField(upload_to="monitores/", blank=True)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ["user__first_name", "user__last_name"]

    def __str__(self):
        return self.user.get_full_name() or self.user.username


class Clase(models.Model):
    monitor = models.ForeignKey(Monitor, on_delete=models.CASCADE, related_name="clases")
    pista = models.ForeignKey(Pista, on_delete=models.CASCADE, related_name="clases")
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    max_alumnos = models.PositiveIntegerField(default=4)
    precio = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["fecha", "hora_inicio"]

    def __str__(self):
        return f"Clase {self.monitor} - {self.fecha} {self.hora_inicio}"

    @property
    def plazas_disponibles(self):
        return self.max_alumnos - self.inscripciones.count()


class InscripcionClase(models.Model):
    clase = models.ForeignKey(Clase, on_delete=models.CASCADE, related_name="inscripciones")
    alumno = models.ForeignKey(User, on_delete=models.CASCADE, related_name="inscripciones_clase")
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["clase", "alumno"]

    def __str__(self):
        return f"{self.alumno.username} en {self.clase}"
