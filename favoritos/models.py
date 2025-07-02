from django.db import models

from produto.models import Produto

# Create your models here.

class Favoritos(models.Model):
    fav_id = models.CharField(max_length=250, blank=True)
    data_criado = models.DateField(auto_now_add=True)
    
class FavItem(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    favoritos = models.ForeignKey(Favoritos, on_delete=models.CASCADE, null=True)
    esta_disponivel = models.BooleanField(default=True)
    quantidade = models.IntegerField(default=0)