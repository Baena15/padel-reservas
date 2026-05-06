from django import forms
from django.contrib.auth.models import User
from .models import Torneo


class TorneoForm(forms.ModelForm):
    class Meta:
        model = Torneo
        fields = ["nombre", "tipo", "fecha_inicio", "fecha_fin"]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control", "placeholder": "Nombre del torneo"}),
            "tipo": forms.Select(attrs={"class": "form-select"}),
            "fecha_inicio": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "fecha_fin": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
        }
        help_texts = {
            "fecha_inicio": "Fecha de inicio del torneo.",
            "fecha_fin": "Fecha de finalización.",
        }

    def clean(self):
        cleaned = super().clean()
        fecha_inicio = cleaned.get("fecha_inicio")
        fecha_fin = cleaned.get("fecha_fin")
        if fecha_inicio and fecha_fin and fecha_fin < fecha_inicio:
            raise forms.ValidationError("La fecha de fin no puede ser anterior a la de inicio.")
        return cleaned


class InscripcionParejaForm(forms.Form):
    pareja = forms.ModelChoiceField(
        queryset=User.objects.none(),
        label="Selecciona tu pareja",
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    def __init__(self, torneo=None, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if torneo and user:
            # Excluir: ya inscritos, el propio usuario, staff/admin
            inscritos = torneo.inscripciones.values_list("jugador_id", flat=True)
            self.fields["pareja"].queryset = User.objects.filter(
                perfil__rol="jugador"
            ).exclude(
                id__in=list(inscritos) + [user.id]
            ).order_by("username")
