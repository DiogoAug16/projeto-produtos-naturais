from django.db import models

# Create your models here.
class Departamento(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    
    def __str__(self):
        return self.nome
    
