from django.urls import path
from .views import (
    PartidoListView, PartidoDetailView, PartidoCreateView,
    unirse_partido, abandonar_partido, cerrar_partido,
)

urlpatterns = [
    path("", PartidoListView.as_view(), name="partido_list"),
    path("nuevo/", PartidoCreateView.as_view(), name="partido_create"),
    path("<int:pk>/", PartidoDetailView.as_view(), name="partido_detail"),
    path("<int:pk>/unirse/", unirse_partido, name="unirse_partido"),
    path("<int:pk>/abandonar/", abandonar_partido, name="abandonar_partido"),
    path("<int:pk>/cerrar/", cerrar_partido, name="cerrar_partido"),
]
