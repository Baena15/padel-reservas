from django.urls import path
from .views import ReservaListView

urlpatterns = [
    path("", ReservaListView.as_view(), name="reserva_list"),
]
