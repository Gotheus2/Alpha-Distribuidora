from django.shortcuts import render, redirect

def login_usuario(request):
    if request.method == "POST":
        return redirect("cadastro_clientes")

    return render(request, "login_usuario/login.html")