from django.shortcuts import get_object_or_404, render

from categoria.admin import Categoria
from produto.admin import Produto

# Create your views here.
def visualizarLoja(request, categoria_slug=None):
    categorias = None
    produtos = None
    
    if categoria_slug != None:
        categorias = get_object_or_404(Categoria, slug = categoria_slug)
        produtos = Produto.objects.filter(categoria = categorias, esta_disponivel = True)
        produto_quant = produtos.count()
    else:
        produtos = Produto.objects.all().filter(esta_disponivel = True)
        produtos_quant = produtos.count()
        
    
    
    return render(request, 'shop-grid.html')