from django.db import models


class Pista(models.Model):
    TIPOS = [("indoor", "Indoor"), ("outdoor", "Outdoor")]

    nombre = models.CharField(max_length=50)
    tipo = models.CharField(max_length=20, choices=TIPOS)
    disponible = models.BooleanField(default=True)

    class Meta:
        ordering = ["tipo", "nombre"]
        verbose_name = "pista"
        verbose_name_plural = "pistas"

    def __str__(self):
        return f"{self.nombre} ({self.get_tipo_display()})"


class Bloqueo(models.Model):
    pista = models.ForeignKey(Pista, on_delete=models.CASCADE, related_name="bloqueos")
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    motivo = models.CharField(max_length=200)

    class Meta:
        ordering = ["-fecha_inicio"]

    def __str__(self):
        return f"Bloqueo {self.pista} ({self.fecha_inicio} - {self.fecha_fin})"
