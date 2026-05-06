from django.urls import path
from .views import ClaseListView, ClaseDetailView, inscribir_clase, desinscribir_clase

urlpatterns = [
    path("", ClaseListView.as_view(), name="clase_list"),
    path("<int:pk>/", ClaseDetailView.as_view(), name="clase_detail"),
    path("<int:pk>/inscribir/", inscribir_clase, name="inscribir_clase"),
    path("<int:pk>/desinscribir/", desinscribir_clase, name="desinscribir_clase"),
]
