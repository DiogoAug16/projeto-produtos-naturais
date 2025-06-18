from django.contrib import admin

from produto.models import Produto

# Register your models here.

class ProdutoAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ('produto_nome',)
    }
    list_display = ('produto_nome', 'slug', 'preco', 'imposto', 'promocao_valor_porcentagem', 'estoque', 'esta_disponivel','promocao_disponivel', 'categoria','get_departamento')
    list_filter = ('esta_disponivel', 'promocao_disponivel')
    search_fields = ('produto_nome',)
    list_editable = ('preco','promocao_valor_porcentagem', 'estoque', 'esta_disponivel', 'promocao_disponivel', 'imposto')
    
    def get_departamento(self, obj):
        return obj.categoria.departamento.nome
    get_departamento.short_description = 'Departamento'

admin.site.register(Produto, ProdutoAdmin)