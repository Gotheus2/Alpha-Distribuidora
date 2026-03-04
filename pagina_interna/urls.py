from django.urls import path
from . import views

urlpatterns = [
    path('clientes/', views.cadastro_clientes, name='cadastro_clientes'),
    path('vendedores/', views.vendedores, name='vendedores'),
    path('vendas/', views.vendas, name='vendas'),
    path('produtos/', views.produtos, name='produtos'),
    path('financeiro/', views.financeiro, name='financeiro'),
    path('', views.dashboard, name='dashboard'),
]