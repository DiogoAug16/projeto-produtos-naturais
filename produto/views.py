from multiprocessing import context
from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator
from categoria.models import Categoria
from produto.models import Produto

# Create your views here.

def visualizarLoja(request, categoria_slug=None):
    categoria = None
    ordenar = request.GET.get('ordenar')
    preco_min = request.GET.get('preco_min')
    preco_max = request.GET.get('preco_max')
    
    if categoria_slug:
        categoria = get_object_or_404(Categoria, slug=categoria_slug)
        produtos_list = Produto.objects.filter(categoria=categoria, esta_disponivel=True)
    else:
        produtos_list = Produto.objects.filter(esta_disponivel=True)
        
    if preco_min:
        produtos_list = produtos_list.filter(preco__gte=preco_min)
    if preco_max:
        produtos_list = produtos_list.filter(preco__lte=preco_max)

    if ordenar == 'preco_crescente':
        produtos_list = produtos_list.order_by('preco')
    elif ordenar == 'preco_decrescente':
        produtos_list = produtos_list.order_by('-preco')
        
    paginator = Paginator(produtos_list, 9)
    pagina_num = request.GET.get('page')
    produtos = paginator.get_page(pagina_num)
    produtos_promocao = Produto.objects.filter(
        esta_disponivel=True,
        promocao_disponivel=True,
        promocao_valor_porcentagem__gt=0,
    )

    context = {
        'produtos': produtos,
        'produto_quant': paginator.count,
        'categoria_atual': categoria,
        'produtos_promocao': produtos_promocao,
        'preco_min': preco_min,
        'preco_max': preco_max,
    }
    
    return render(request, 'shop-grid.html', context)

def  visualizarDetalheProduto (request, categoria_slug, produto_slug):
    produto = Produto.objects.get(slug = produto_slug, categoria__slug = categoria_slug)
    context = {
        'produto': produto,
    }

    return render(request, 'shop-details.html', context)
    
    