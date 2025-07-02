from django.db import models
from django.urls import reverse

# Create your models here.
class Departamento(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    departamento_imagem = models.ImageField(upload_to='fotos/departamentos', blank=True)
    
    def __str__(self):
        return self.nome
    
    def get_url(self):
        return reverse('produtos_por_departamento', args=[self.slug])
    
