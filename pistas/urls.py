from django.urls import path
from .views import PistaListView

urlpatterns = [
    path("", PistaListView.as_view(), name="pista_list"),
]
