from django.contrib import admin

from produto.models import Produto

# Register your models here.

class ProdutoAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ('produto_nome',)
    }
    list_display = ('produto_nome', 'slug', 'preco', 'estoque', 'esta_disponivel', 'categoria')
    list_filter = ('esta_disponivel',)
    search_fields = ('produto_nome',)
    list_editable = ('preco', 'estoque', 'esta_disponivel')

admin.site.register(Produto, ProdutoAdmin)