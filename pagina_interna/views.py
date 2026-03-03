from django.shortcuts import render

# Create your views here.
def cadastro_clientes(request):
    return render(request, "cadastro_clientes.html")