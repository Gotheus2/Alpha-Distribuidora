from django.urls import path
from . import views

app_name = "pagina_interna"

urlpatterns = [
    path('clientes/', views.cadastro_clientes, name='cadastro_clientes'),
    path("clientes/<int:id>/", views.cadastro_clientes, name="editar_cliente"),
    path("clientes/deletar/<int:id>/", views.deletar_cliente, name="deletar_cliente"),
    path("vendedores/", views.vendedores, name="vendedores"),
    path("vendedores/<int:id>/editar/", views.editar_vendedor, name="editar_vendedor"),
    path("vendedores/<int:id>/deletar/", views.deletar_vendedor, name="deletar_vendedor"),
    path('vendas/', views.vendas, name='vendas'),
    path("produtos/", views.produtos, name="produtos"),
    path("produtos/<int:id>/", views.produtos, name="editar_produto"),
    path("produtos/deletar/<int:id>/", views.deletar_produto, name="deletar_produto"),
    path('financeiro/', views.financeiro, name='financeiro'),
    path("financeiro/editar/<int:id>/", views.financeiro_editar, name="financeiro_editar"),
    path("financeiro/excluir/<int:id>/", views.financeiro_excluir, name="financeiro_excluir"),
    path('', views.dashboard, name='dashboard'),
]
