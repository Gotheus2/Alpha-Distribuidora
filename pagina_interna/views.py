from django.utils import timezone
from decimal import Decimal
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Sum

from .models import Vendedor, Cliente
from .models import MovimentacaoFinanceira
from .forms import VendedorForm, ClienteForm


def cadastro_clientes(request, id=None):
    cliente_selecionado = get_object_or_404(Cliente, id=id) if id else None

    if request.method == "POST":
        form = ClienteForm(request.POST, instance=cliente_selecionado)
        if form.is_valid():
            form.save()
            return redirect("pagina_interna:cadastro_clientes")
    else:
        form = ClienteForm(instance=cliente_selecionado)

    qs = Cliente.objects.all().order_by('nome')
    paginator = Paginator(qs, 5)
    page_number = request.GET.get("pag") or 1
    page_obj = paginator.get_page(page_number)

    total_clientes = Cliente.objects.count()

    hoje = timezone.now()
    novo_mes = Cliente.objects.filter(
        criado_em__year = hoje.year,
        criado_em__month = hoje.month,
    ).count()

    clientes_inativos = Cliente.objects.filter(ativo=False).count()

    return render(request, "cadastro_clientes.html", {
        "form": form,
        "clientes": page_obj.object_list,
        "page_obj": page_obj,
        "total_clientes": total_clientes,
        "novos_mes": novo_mes,
        "clientes_inativos": clientes_inativos,
    })

def deletar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    if request.method == "POST":
        cliente.delete()
    return redirect("pagina_interna:cadastro_clientes")


def vendas(request):
    return render(request, "vendas.html")

def produtos(request):
    return render(request, "produtos.html")


def dashboard(request):
    return render(request, "dashboard.html")


def _vendedores_context(page_number=1):
    
    qs = Vendedor.objects.all().order_by("nome")
    paginator = Paginator(qs, 5)
    page_obj = paginator.get_page(page_number)
    total_vendedores_ativos = Vendedor.objects.filter(ativo=True).count()
    return page_obj, total_vendedores_ativos


def vendedores(request):
    
    page_number = request.GET.get("page") or 1

    if request.method == "POST":
        form = VendedorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Vendedor cadastrado com sucesso!")
            return redirect("pagina_interna:vendedores")
    else:
        form = VendedorForm()

    page_obj, total_vendedores_ativos = _vendedores_context(page_number)

    return render(request, "vendedores.html", {
        "form": form,
        "editando": False,
        "vendedor_selecionado": None,
        "page_obj": page_obj,
        "vendedores": page_obj.object_list,
        "total_vendedores_ativos": total_vendedores_ativos,
        "historico_vendas": [],
    })


def editar_vendedor(request, id):
    
    vendedor = get_object_or_404(Vendedor, id=id)
    page_number = request.GET.get("page") or 1

    if request.method == "POST":
        form = VendedorForm(request.POST, request.FILES, instance=vendedor)
        if form.is_valid():
            form.save()
            messages.success(request, "Vendedor atualizado com sucesso!")
            return redirect("pagina_interna:vendedores")
    else:
        form = VendedorForm(instance=vendedor)

    page_obj, total_vendedores_ativos = _vendedores_context(page_number)
    historico_vendas = vendedor.vendas.all().order_by("-data")[:3]

    return render(request, "vendedores.html", {
        "form": form,
        "editando": True,
        "vendedor_selecionado": vendedor,
        "page_obj": page_obj,
        "vendedores": page_obj.object_list,
        "total_vendedores_ativos": total_vendedores_ativos,
        "historico_vendas": historico_vendas,
    })


def deletar_vendedor(request, id):
    vendedor = get_object_or_404(Vendedor, id=id)
    if request.method == "POST":
        vendedor.delete()
        messages.success(request, "Vendedor removido!")
    return redirect("pagina_interna:vendedores")


def financeiro(request):
    if request.method == "POST":
        tipo = (request.POST.get("tipo") or "ENTRADA").upper()
        categoria = (request.POST.get("categoria") or "").strip()
        descricao = (request.POST.get("descricao") or "").strip()
        valor_raw = (request.POST.get("valor") or "").replace(".", "").replace(",", ".").strip()
        data = request.POST.get("data") or None

        if tipo not in ("ENTRADA", "SAIDA"):
            messages.error(request, "Tipo inválido.")
            return redirect("pagina_interna:financeiro")

        if not categoria or not descricao or not valor_raw or not data:
            messages.error(request, "Preencha categoria, descrição, valor e data.")
            return redirect("pagina_interna:financeiro")

        try:
            valor = Decimal(valor_raw)
        except Exception:
            messages.error(request, "Valor inválido.")
            return redirect("pagina_interna:financeiro")

        MovimentacaoFinanceira.objects.create(
            tipo=tipo,
            categoria=categoria,
            descricao=descricao,
            valor=valor,
            data=data,
        )
        messages.success(request, "Movimentação adicionada com sucesso!")
        return redirect("pagina_interna:financeiro")

    movimentacoes_qs = MovimentacaoFinanceira.objects.all().order_by("-data", "-id")

    total_entradas = movimentacoes_qs.filter(tipo="ENTRADA").aggregate(
        s=Sum("valor")
    )["s"] or Decimal("0.00")

    total_saidas = movimentacoes_qs.filter(tipo="SAIDA").aggregate(
        s=Sum("valor")
    )["s"] or Decimal("0.00")

    saldo_atual = total_entradas - total_saidas

    return render(request, "financeiro.html", {
        "movimentacoes": movimentacoes_qs,
        "total_entradas": total_entradas,
        "total_saidas": total_saidas,
        "saldo_atual": saldo_atual,
        "ver_tudo_url": None,
    })


def financeiro_editar(request, id):
    mov = get_object_or_404(MovimentacaoFinanceira, id=id)

    if request.method == "POST":
        tipo = (request.POST.get("tipo") or mov.tipo).upper()
        categoria = (request.POST.get("categoria") or mov.categoria).strip()
        descricao = (request.POST.get("descricao") or mov.descricao).strip()
        valor_raw = (request.POST.get("valor") or str(mov.valor)).replace(".", "").replace(",", ".").strip()
        data = request.POST.get("data") or mov.data

        if tipo not in ("ENTRADA", "SAIDA"):
            messages.error(request, "Tipo inválido.")
            return redirect("pagina_interna:financeiro")

        try:
            valor = Decimal(valor_raw)
        except Exception:
            messages.error(request, "Valor inválido.")
            return redirect("pagina_interna:financeiro")

        mov.tipo = tipo
        mov.categoria = categoria
        mov.descricao = descricao
        mov.valor = valor
        mov.data = data
        mov.save()

        messages.success(request, "Movimentação atualizada!")
        return redirect("pagina_interna:financeiro")

    return redirect("pagina_interna:financeiro")


def financeiro_excluir(request, id):
    mov = get_object_or_404(MovimentacaoFinanceira, id=id)
    if request.method == "POST":
        mov.delete()
        messages.success(request, "Movimentação removida!")
    return redirect("pagina_interna:financeiro")