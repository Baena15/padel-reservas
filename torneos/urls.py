from django.urls import path
from .views import TorneoListView

urlpatterns = [
    path("", TorneoListView.as_view(), name="torneo_list"),
]
