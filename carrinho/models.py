from django.db import models

from produto.models import Produto

# Create your models here.

class Carrinho(models.Model):
    car_id = models.CharField(max_length=250, blank=True)
    data_criado = models.DateField(auto_now_add=True)
    
class CarItem(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    carrinho = models.ForeignKey(Carrinho, on_delete=models.CASCADE, null=True)
    quantidade = models.IntegerField()
    esta_disponivel = models.BooleanField(default=True)
    
    def getSubTotal(self):
        if self.produto.promocao_disponivel and self.produto.promocao_valor_porcentagem > 0:
            preco_com_desconto = self.produto.preco_com_desconto()
            return preco_com_desconto * self.quantidade
        else:
            return self.produto.preco * self.quantidade