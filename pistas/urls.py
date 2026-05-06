from django.urls import path
from .views import PistaListView, PistaToggleDisponibleView

urlpatterns = [
    path("", PistaListView.as_view(), name="pista_list"),
    path("<int:pk>/toggle/", PistaToggleDisponibleView.as_view(), name="pista_toggle"),
]
