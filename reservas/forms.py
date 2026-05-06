from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Q
from datetime import datetime, date, time, timedelta
from .models import Reserva
from pistas.models import Pista, Bloqueo


DURACION_RESERVA = timedelta(minutes=90)
HORA_APERTURA = time(9, 0)
HORA_CIERRE = time(21, 0)
HORA_DESCANSO_INICIO = time(13, 30)
HORA_DESCANSO_FIN = time(16, 0)

FRANJAS_HORARIAS = [
    ("09:00", "09:00"),
    ("09:30", "09:30"),
    ("10:00", "10:00"),
    ("10:30", "10:30"),
    ("11:00", "11:00"),
    ("11:30", "11:30"),
    ("12:00", "12:00"),
    ("16:00", "16:00"),
    ("16:30", "16:30"),
    ("17:00", "17:00"),
    ("17:30", "17:30"),
    ("18:00", "18:00"),
    ("18:30", "18:30"),
    ("19:00", "19:00"),
    ("19:30", "19:30"),
    ("21:00", "21:00"),
]


class ReservaForm(forms.ModelForm):
    DURACIONES = [
        ("", "--- No recurrente ---"),
        ("6m", "6 Meses"),
        ("1a", "1 Año"),
    ]

    es_recurrente = forms.BooleanField(required=False, label="¿Reserva recurrente?")
    duracion = forms.ChoiceField(choices=DURACIONES, required=False, label="Duración recurrente")

    class Meta:
        model = Reserva
        fields = ["pista", "fecha", "hora_inicio"]
        widgets = {
            "fecha": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "hora_inicio": forms.Select(choices=FRANJAS_HORARIAS, attrs={"class": "form-select"}),
            "pista": forms.Select(attrs={"class": "form-select"}),
        }

    def __init__(self, *args, **kwargs):
        self.usuario = kwargs.pop("usuario", None)
        super().__init__(*args, **kwargs)
        self.fields["pista"].queryset = Pista.objects.filter(disponible=True)
        # Mostrar hora fin como campo readonly si es edición
        if self.instance and self.instance.pk:
            self.fields["hora_inicio"].help_text = f"Fin automático: {self.instance.hora_fin.strftime('%H:%M')} (90 min)"
        else:
            self.fields["hora_inicio"].help_text = "Horario mañana: 9:00 – 12:00 | Tarde: 16:00 – 21:00. Duración 90 min."

    def clean_hora_inicio(self):
        hora = self.cleaned_data.get("hora_inicio")
        if not hora:
            return hora

        if hora < HORA_APERTURA:
            raise ValidationError("El club abre a las 9:00.")
        if hora > HORA_CIERRE:
            raise ValidationError("La última reserva es a las 21:00.")
        if hora.minute not in (0, 30):
            raise ValidationError("Las reservas solo pueden empezar en punto o en media hora (ej. 10:00, 10:30).")

        hora_fin = (datetime.combine(date.today(), hora) + DURACION_RESERVA).time()

        # No puede empezar antes del descanso y terminar después
        if hora < HORA_DESCANSO_INICIO and hora_fin > HORA_DESCANSO_INICIO:
            raise ValidationError("La reserva cruza el horario de cierre (13:30-16:00).")
        if HORA_DESCANSO_INICIO <= hora < HORA_DESCANSO_FIN:
            raise ValidationError("El club cierra de 13:30 a 16:00.")
        if HORA_DESCANSO_INICIO < hora_fin <= HORA_DESCANSO_FIN:
            raise ValidationError("La reserva termina durante el horario de cierre (13:30-16:00).")

        return hora

    def clean(self):
        cleaned = super().clean()
        pista = cleaned.get("pista")
        fecha = cleaned.get("fecha")
        hora_inicio = cleaned.get("hora_inicio")

        if not all([pista, fecha, hora_inicio]):
            return cleaned

        from datetime import datetime, date
        hora_fin = (datetime.combine(date.today(), hora_inicio) + DURACION_RESERVA).time()

        # Validar solapamiento con otras reservas activas
        solapadas = Reserva.objects.filter(
            pista=pista,
            fecha=fecha,
            estado__in=["pendiente", "confirmada"],
        ).exclude(pk=self.instance.pk if self.instance else None).filter(
            Q(hora_inicio__lt=hora_fin, hora_fin__gt=hora_inicio)
        )
        if solapadas.exists():
            raise ValidationError("La pista ya está reservada en ese horario.")

        # Validar bloqueos (torneos / mantenimiento)
        bloqueos = Bloqueo.objects.filter(
            pista=pista,
            fecha_inicio__lte=fecha,
            fecha_fin__gte=fecha,
            hora_inicio__lt=hora_fin,
            hora_fin__gt=hora_inicio,
        )
        if bloqueos.exists():
            raise ValidationError("La pista está bloqueada en ese horario (torneo o mantenimiento).")

        # Guardar hora_fin en cleaned_data para usar en la vista
        cleaned["hora_fin"] = hora_fin
        return cleaned
