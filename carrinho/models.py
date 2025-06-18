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
        return self.produto.preco * self.quantidade