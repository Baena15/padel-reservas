from django import forms
from django.contrib.auth.models import User
from .models import Torneo


class TorneoForm(forms.ModelForm):
    class Meta:
        model = Torneo
        fields = ["nombre", "tipo", "fecha_inicio", "fecha_fin", "hora_inicio", "hora_fin"]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control", "placeholder": "Nombre del torneo"}),
            "tipo": forms.Select(attrs={"class": "form-select"}),
            "fecha_inicio": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "fecha_fin": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "hora_inicio": forms.TimeInput(attrs={"type": "time", "class": "form-control"}),
            "hora_fin": forms.TimeInput(attrs={"type": "time", "class": "form-control"}),
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
        label="Pareja registrada",
        required=False,
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    pareja_nombre = forms.CharField(
        label="Nombre pareja (externa)",
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Ej. Juan"}),
    )
    pareja_apellido = forms.CharField(
        label="Apellido pareja (externa)",
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Ej. García"}),
    )

    def __init__(self, torneo=None, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if torneo and user:
            inscritos = torneo.inscripciones.values_list("jugador_id", flat=True)
            self.fields["pareja"].queryset = User.objects.filter(
                perfil__rol="jugador"
            ).exclude(
                id__in=list(inscritos) + [user.id]
            ).order_by("username")

    def clean(self):
        cleaned = super().clean()
        pareja = cleaned.get("pareja")
        nombre = cleaned.get("pareja_nombre", "").strip()
        apellido = cleaned.get("pareja_apellido", "").strip()

        if pareja and nombre:
            raise forms.ValidationError("Elige una pareja registrada O introduce datos de una pareja externa, no ambas.")
        if not pareja and not nombre:
            raise forms.ValidationError("Debes seleccionar una pareja registrada o introducir los datos de una pareja externa.")
        if not pareja and (nombre and not apellido):
            raise forms.ValidationError("Si la pareja es externa, introduce nombre y apellido.")

        cleaned["pareja_nombre"] = nombre
        cleaned["pareja_apellido"] = apellido
        return cleaned
