from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Perfil
from .constants import CATEGORIAS


class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={"class": "form-control"}))
    categoria = forms.ChoiceField(choices=CATEGORIAS, label="Nivel de juego", widget=forms.Select(attrs={"class": "form-select"}))
    telefono = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Ej. 612345678"}))

    class Meta:
        model = User
        fields = ("username", "email", "telefono", "categoria", "password1", "password2")
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].widget.attrs["class"] = "form-control"
        self.fields["password2"].widget.attrs["class"] = "form-control"

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
            user.perfil.categoria = self.cleaned_data["categoria"]
            user.perfil.telefono = self.cleaned_data["telefono"]
            user.perfil.save()
        return user


class PerfilUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={"class": "form-control"}))

    class Meta:
        model = Perfil
        fields = ["categoria", "telefono", "foto"]
        widgets = {
            "categoria": forms.Select(attrs={"class": "form-select"}),
            "telefono": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ej. 612345678"}),
            "foto": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields["email"].initial = self.instance.user.email

    def save(self, commit=True):
        perfil = super().save(commit=False)
        perfil.user.email = self.cleaned_data["email"]
        if commit:
            perfil.user.save()
            perfil.save()
        return perfil
