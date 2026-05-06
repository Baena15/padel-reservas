from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import registro_view, perfil_view, perfil_editar_view

urlpatterns = [
    path("login/", LoginView.as_view(template_name="usuarios/login.html"), name="login"),
    path("logout/", LogoutView.as_view(next_page="home"), name="logout"),
    path("registro/", registro_view, name="registro"),
    path("perfil/", perfil_view, name="perfil"),
    path("perfil/editar/", perfil_editar_view, name="perfil_editar"),
]
