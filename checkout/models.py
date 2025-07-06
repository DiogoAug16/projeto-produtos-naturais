from django.db import models
from django.conf import settings
from produto.models import Produto

class Pedido(models.Model):

    class MetodosPagamento(models.TextChoices):
        PIX = 'PIX', 'Pix'
        CARD = 'CARD', 'Crédito/Débito'

    class StatusPedido(models.TextChoices):
        PENDENTE = 'PENDENTE', 'Pendente'
        PAGO = 'PAGO', 'Pago'
        ENVIADO = 'ENVIADO', 'Enviado'
        ENTREGUE = 'ENTREGUE', 'Entregue'
        CANCELADO = 'CANCELADO', 'Cancelado'

    # Relação com o usuário
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Usuário")

    # Informações de cobrança do formulário
    nome = models.CharField("Nome", max_length=100)
    sobrenome = models.CharField("Sobrenome", max_length=100)
    endereco = models.CharField("Logradouro", max_length=255)
    numero_endereco = models.CharField("Número", max_length=20)
    complemento_endereco = models.CharField("Complemento", max_length=100, blank=True, null=True)
    estado = models.CharField("Estado", max_length=50)
    cidade = models.CharField("Cidade", max_length=100)
    cep = models.CharField("CEP", max_length=9)
    telefone = models.CharField("Telefone celular", max_length=20)
    cpf = models.CharField("CPF", max_length=14)

    # Informações financeiras do pedido (calculadas no momento da compra)
    subtotal = models.DecimalField("Subtotal", max_digits=10, decimal_places=2)
    valor_imposto = models.DecimalField("Valor do Imposto", max_digits=10, decimal_places=2)
    valor_frete = models.DecimalField("Valor do Frete", max_digits=10, decimal_places=2, default=0.00)
    valor_total = models.DecimalField("Valor Total", max_digits=10, decimal_places=2)
    
    # Detalhes do pedido
    metodo_pagamento = models.CharField("Método de Pagamento", max_length=20, choices=MetodosPagamento.choices)
    status = models.CharField("Status", max_length=20, choices=StatusPedido.choices, default=StatusPedido.PENDENTE)
    criado_em = models.DateTimeField("Criado em", auto_now_add=True)
    atualizado_em = models.DateTimeField("Atualizado em", auto_now=True)

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        ordering = ('-criado_em',)

    def __str__(self):
        return f"Pedido #{self.id} - {self.user.username if self.user else 'Convidado'}"

class ItemPedido(models.Model):

    pedido = models.ForeignKey(Pedido, related_name='itens', on_delete=models.CASCADE, verbose_name="Pedido")
    produto = models.ForeignKey(Produto, related_name='itens_pedido', on_delete=models.PROTECT, verbose_name="Produto")
    preco_item = models.DecimalField("Preço (unidade)", max_digits=10, decimal_places=2)
    quantidade = models.PositiveIntegerField("Quantidade", default=1)

    class Meta:
        verbose_name = "Item do Pedido"
        verbose_name_plural = "Itens do Pedido"

    def __str__(self):
        return f"Item {self.produto.produto_nome} no Pedido #{self.pedido.id}"

    def get_custo_total(self):
        return self.preco_item * self.quantidade