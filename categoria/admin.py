from django.contrib import admin

from categoria.models import Categoria

# Register your models here.
class CategoriaAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug':('categoria_nome',)

    }
    list_display=('categoria_nome', 'slug', 'departamento', 'descricao')
    search_fields=('categoria_nome',)

admin.site.register(Categoria, CategoriaAdmin)