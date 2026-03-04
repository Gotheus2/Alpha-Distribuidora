from django.urls import path
from . import views

urlpatterns = [
    path('clientes/', views.cadastro_clientes, name="cadastro_clientes"),
    path('dashboards/', views.dashboards, name="dashboards"),
    path('relatorios/', views.relatorios, name="relatorios"),
]