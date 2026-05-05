from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .constants import CATEGORIAS, ROLES


class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="perfil")
    rol = models.CharField(max_length=20, choices=ROLES, default="jugador")
    categoria = models.CharField(max_length=20, choices=CATEGORIAS, default="5b")
    telefono = models.CharField(max_length=20, blank=True)
    foto = models.ImageField(upload_to="perfiles/", blank=True)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["user__username"]

    def __str__(self):
        return f"{self.user.username} ({self.get_categoria_display()})"


@receiver(post_save, sender=User)
def crear_perfil(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(user=instance)


@receiver(post_save, sender=User)
def guardar_perfil(sender, instance, **kwargs):
    instance.perfil.save()
