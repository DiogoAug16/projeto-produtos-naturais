from django.db import models

from categoria.admin import Categoria

# Create your models here.
class Produto(models.Model):
    produto_nome = models.CharField(max_length=50, unique=True)
    produto_imagem = models.ImageField(upload_to='fotos/produtos', blank=True)
    descricao = models.CharField(max_length=1000, blank=True)
    slug = models.SlugField(max_length=100, unique=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    estoque = models.IntegerField(default=0)
    esta_disponivel = models.BooleanField(default=True)
    promocao_disponivel = models.BooleanField(default=False)
    promocao_valor_porcentagem = models.DecimalField(max_digits=2, decimal_places=0, default=0, blank=True)

    def __str__(self):
        return self.produto_nome
