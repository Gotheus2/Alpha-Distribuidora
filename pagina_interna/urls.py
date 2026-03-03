from django.urls import path
from . import views

urlpatterns = [
    path('clientes/', views.cadastro_clientes, name="cadastro_clientes"),
]