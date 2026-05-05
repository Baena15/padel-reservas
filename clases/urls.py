from django.urls import path
from .views import ClaseListView

urlpatterns = [
    path("", ClaseListView.as_view(), name="clase_list"),
]
