from django.urls import path
from .views import PartidoListView

urlpatterns = [
    path("", PartidoListView.as_view(), name="partido_list"),
]
