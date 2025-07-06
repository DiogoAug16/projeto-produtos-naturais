from django.db import models
from django.contrib.auth.models import User

from produto.models import Produto

# Create your models here.

class Favoritos(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    fav_id = models.CharField(max_length=250, blank=True)
    data_criado = models.DateField(auto_now_add=True)
    
class FavItem(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    favoritos = models.ForeignKey(Favoritos, on_delete=models.CASCADE, null=True)
    esta_disponivel = models.BooleanField(default=True)
    quantidade = models.PositiveIntegerField(default=0, null=False)
