from django.urls import path
from . import views

app_name = "pagina_interna"

urlpatterns = [
    path('clientes/', views.cadastro_clientes, name='cadastro_clientes'),
    path("vendedores/", views.vendedores, name="vendedores"),
    path("vendedores/<int:id>/editar/", views.editar_vendedor, name="editar_vendedor"),
    path("vendedores/<int:id>/deletar/", views.deletar_vendedor, name="deletar_vendedor"),
    path('vendas/', views.vendas, name='vendas'),
    path('produtos/', views.produtos, name='produtos'),
    path('financeiro/', views.financeiro, name='financeiro'),
    path("financeiro/editar/<int:id>/", views.financeiro_editar, name="financeiro_editar"),
    path("financeiro/excluir/<int:id>/", views.financeiro_excluir, name="financeiro_excluir"),
    path('', views.dashboard, name='dashboard'),
]
