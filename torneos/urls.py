from django.urls import path
from .views import (
    TorneoListView,
    TorneoDetailView,
    TorneoCreateView,
    TorneoInscribirView,
    TorneoInscribirParejaView,
    TorneoDesinscribirView,
)

urlpatterns = [
    path("", TorneoListView.as_view(), name="torneo_list"),
    path("<int:pk>/", TorneoDetailView.as_view(), name="torneo_detail"),
    path("nuevo/", TorneoCreateView.as_view(), name="torneo_create"),
    path("<int:pk>/inscribir/", TorneoInscribirView.as_view(), name="torneo_inscribir"),
    path("<int:pk>/inscribir/pareja/", TorneoInscribirParejaView.as_view(), name="torneo_inscribir_pareja"),
    path("<int:pk>/desinscribir/", TorneoDesinscribirView.as_view(), name="torneo_desinscribir"),
]
