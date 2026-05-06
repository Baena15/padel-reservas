from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Q
from datetime import datetime, date, time, timedelta
from .models import Partido
from pistas.models import Pista, Bloqueo


HORA_APERTURA = time(9, 0)
HORA_CIERRE = time(21, 0)
HORA_DESCANSO_INICIO = time(13, 30)
HORA_DESCANSO_FIN = time(16, 0)
DURACION_PARTIDO = timedelta(minutes=90)


class PartidoForm(forms.ModelForm):
    class Meta:
        model = Partido
        fields = ["pista", "fecha", "hora_inicio", "nivel_minimo", "max_jugadores"]
        widgets = {
            "fecha": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "hora_inicio": forms.TimeInput(attrs={"type": "time", "class": "form-control"}),
            "pista": forms.Select(attrs={"class": "form-select"}),
            "nivel_minimo": forms.Select(attrs={"class": "form-select"}),
            "max_jugadores": forms.NumberInput(attrs={"class": "form-control", "min": 2, "max": 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["pista"].queryset = Pista.objects.filter(disponible=True)
        self.fields["nivel_minimo"].required = False
        self.fields["hora_inicio"].help_text = "El partido dura 90 minutos."

    def clean_hora_inicio(self):
        hora = self.cleaned_data.get("hora_inicio")
        if not hora:
            return hora
        if hora < HORA_APERTURA:
            raise ValidationError("El club abre a las 9:00.")
        if hora > HORA_CIERRE:
            raise ValidationError("La última hora es a las 21:00.")
        hora_fin = (datetime.combine(date.today(), hora) + DURACION_PARTIDO).time()
        if hora < HORA_DESCANSO_INICIO and hora_fin > HORA_DESCANSO_INICIO:
            raise ValidationError("El partido cruza el horario de cierre (13:30-16:00).")
        if HORA_DESCANSO_INICIO <= hora < HORA_DESCANSO_FIN:
            raise ValidationError("El club cierra de 13:30 a 16:00.")
        return hora

    def clean_fecha(self):
        fecha = self.cleaned_data.get("fecha")
        if fecha and fecha < date.today():
            raise ValidationError("No puedes crear un partido en una fecha pasada.")
        return fecha

    def clean(self):
        cleaned = super().clean()
        pista = cleaned.get("pista")
        fecha = cleaned.get("fecha")
        hora_inicio = cleaned.get("hora_inicio")
        if all([pista, fecha, hora_inicio]):
            hora_fin = (datetime.combine(date.today(), hora_inicio) + DURACION_PARTIDO).time()
            # Validar solapamiento con reservas
            from reservas.models import Reserva
            solapadas = Reserva.objects.filter(
                pista=pista, fecha=fecha, estado__in=["pendiente", "confirmada"]
            ).filter(
                Q(hora_inicio__lt=hora_fin, hora_fin__gt=hora_inicio)
            )
            if solapadas.exists():
                raise ValidationError("La pista ya está reservada en ese horario.")
            # Validar bloqueos
            bloqueos = Bloqueo.objects.filter(
                pista=pista,
                fecha_inicio__lte=fecha, fecha_fin__gte=fecha,
                hora_inicio__lt=hora_fin, hora_fin__gt=hora_inicio,
            )
            if bloqueos.exists():
                raise ValidationError("La pista está bloqueada en ese horario.")
            cleaned["hora_fin"] = hora_fin
        return cleaned
