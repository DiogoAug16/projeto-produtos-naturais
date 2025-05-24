from django.db import models
from django.urls import reverse

from departamento.admin import Departamento


# Create your models here.
class Categoria(models.Model):
    categoria_nome = models.CharField(max_length=50, unique=True)
    categoria_imagem = models.ImageField(upload_to='fotos/categorias', blank=True)
    descricao = models.CharField(max_length=1000, blank=True)
    slug = models.SlugField(max_length=100, unique=True)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, null=False)
    
    def __str__(self):
        return self.categoria_nome
    
    def get_url(self):
        return reverse('produtos_por_categoria', args=[ self.slug ])
