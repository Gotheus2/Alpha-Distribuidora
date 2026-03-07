from django.db import models

from django.db import models

class Vendedor(models.Model):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=14)
    email = models.EmailField()
    telefone = models.CharField(max_length=20)

    ativo = models.BooleanField(default=True)  # <-- NOVO

    foto = models.ImageField(
        upload_to='vendedores/',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.nome


class Venda(models.Model):
    vendedor = models.ForeignKey(
        Vendedor,
        on_delete=models.CASCADE,
        related_name='vendas'
    )

    produto = models.CharField(max_length=100)
    valor = models.DecimalField(max_digits=10, decimal_places=2)

    data = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return self.produto
    

class MovimentacaoFinanceira(models.Model):
    TIPOS = (
        ("ENTRADA", "Entrada"),
        ("SAIDA", "Saída"),
    )

    tipo = models.CharField(max_length=10, choices=TIPOS, default="ENTRADA")
    categoria = models.CharField(max_length=60)
    descricao = models.CharField(max_length=150)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateField()

    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tipo} - {self.categoria} - {self.valor}"


class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    cpf_cnpj = models.CharField(max_length=18, unique=True)
    email = models.EmailField()
    telefone = models.CharField(max_length=20)
    criado_em = models.DateTimeField(auto_now_add=True)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome

class Produto(models.Model):
    CATEGORIA_CHOICES = [
        ("embalagens", "Embalagens"),
        ("papelaria", "Papelaria"),
        ("limpeza", "Limpeza"),
        ("outros", "Outros"),
    ]

    nome = models.CharField(max_length=200)
    sku = models.CharField(max_length=50, unique=True)
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES, default="outros")
    custo = models.DecimalField(max_digits=10, decimal_places=2)
    preco_venda = models.DecimalField(max_digits=10, decimal_places=2)
    estoque = models.PositiveIntegerField(default=0)
    imagem = models.ImageField(upload_to="produtos/", blank=False, null=False)
    criado_em = models.DateTimeField(auto_now_add=True)

    @property
    def margem(self):
        if self.preco_venda and self.custo > 0:
            return round((self.preco_venda - self.custo) / self.preco_venda * 100, 1)
        return 0.0
    
    def __str__(self):
        return self.nome