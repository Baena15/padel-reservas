from django.views.generic import ListView
from .models import Clase


class ClaseListView(ListView):
    model = Clase
    template_name = "clases/clase_list.html"
    context_object_name = "clases"
