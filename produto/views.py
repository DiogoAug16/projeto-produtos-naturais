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
    ordenar = request.GET.get('ordenar')
    
    if categoria_slug:
        categoria = get_object_or_404(Categoria, slug=categoria_slug)
        produtos_list = Produto.objects.filter(categoria=categoria, esta_disponivel=True)

    else:
        produtos_list = Produto.objects.filter(esta_disponivel=True)

    if ordenar == 'preco_crescente':
        produtos_list = produtos_list.order_by('preco')
    elif ordenar == 'preco_decrescente':
        produtos_list = produtos_list.order_by('-preco')

    paginator = Paginator(produtos_list, 9)
    pagina_num = request.GET.get('page')
    produtos = paginator.get_page(pagina_num)

    context = {
        'produtos': produtos,
        'produto_quant': paginator.count,
        'categoria_atual': categoria,
    }
    
    return render(request, 'shop-grid.html', context)

    
    