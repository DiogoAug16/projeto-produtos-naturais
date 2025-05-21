from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator

from categoria.models import Categoria
from produto.models import Produto

# Create your views here.
from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator
from categoria.models import Categoria
from produto.models import Produto

def visualizarLoja(request, categoria_slug=None):
    categoria = None
    
    if categoria_slug:
        categoria = get_object_or_404(Categoria, slug=categoria_slug)
        produtos_list = Produto.objects.filter(categoria=categoria, esta_disponivel=True)
    else:
        produtos_list = Produto.objects.filter(esta_disponivel=True)

    paginator = Paginator(produtos_list, 9)  # 9 produtos por página
    pagina_num = request.GET.get('page')
    produtos = paginator.get_page(pagina_num)

    context = {
        'produtos': produtos,
        'produto_quant': paginator.count,
        'categoria_atual': categoria,
    }
    
    return render(request, 'shop-grid.html', context)

    
    