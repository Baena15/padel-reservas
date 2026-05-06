from django.urls import path
from .views import TorneoListView, TorneoDetailView

urlpatterns = [
    path("", TorneoListView.as_view(), name="torneo_list"),
    path("<int:pk>/", TorneoDetailView.as_view(), name="torneo_detail"),
]
