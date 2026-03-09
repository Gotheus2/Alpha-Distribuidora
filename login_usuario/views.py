from django.shortcuts import render, redirect

def login_usuario(request):
    if request.method == "POST":
        email = request.POST.get("email")
        senha = request.POST.get("senha")

        return redirect("pagina_interna:relatorios")

    return render(request, "login_usuario/login.html")