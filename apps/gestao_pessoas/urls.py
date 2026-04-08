from django.urls import path
from . import views
urlpatterns = [
    path("", views.gestao_list, name="listar_gestao")
]
