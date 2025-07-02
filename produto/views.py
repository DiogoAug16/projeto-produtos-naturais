from ast import expr
from decimal import Decimal
from departamento.models import Departamento
from categoria.models import Categoria
from produto.models import Produto
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db.models import *
import requests

def visualizar_loja(request, departamento_slug=None, categoria_slug=None):
    departamento = None
    categoria = None
    produtos_list = Produto.objects.filter(esta_disponivel=True)

    if departamento_slug:
        departamento = get_object_or_404(Departamento, slug=departamento_slug)
        categorias_do_departamento = Categoria.objects.filter(departamento=departamento)
        produtos_list = produtos_list.filter(categoria__in=categorias_do_departamento)

    if categoria_slug:
        categoria = get_object_or_404(Categoria, slug=categoria_slug)
        produtos_list = produtos_list.filter(categoria=categoria)

    produtos, paginator = filtrar_produtos(request, produtos_list)

    produtos_promocao = Produto.objects.filter(
        esta_disponivel=True,
        promocao_disponivel=True,
        promocao_valor_porcentagem__gt=0,
    ).order_by('?')[:9]

    context = {
        'produtos': produtos,
        'produto_quant': paginator.count,
        'departamento_atual': departamento,
        'categoria_atual': categoria,
        'produtos_promocao': produtos_promocao,
        'preco_min': request.GET.get('preco_min'),
        'preco_max': request.GET.get('preco_max'),
        'ordenar': request.GET.get('ordenar'),
    }

    return render(request, 'shop-grid.html', context)


def buscar_produtos(request, keyword):
    produtos_list = Produto.objects.filter(
        esta_disponivel=True,
        produto_nome__icontains=keyword
    )

    produtos, paginator = filtrar_produtos(request, produtos_list)

    produtos_promocao = Produto.objects.filter(
        esta_disponivel=True,
        promocao_disponivel=True,
        promocao_valor_porcentagem__gt=0,
    )

    context = {
        'produtos': produtos,
        'produto_quant': paginator.count,
        'keyword': keyword,
        'preco_min': request.GET.get('preco_min'),
        'preco_max': request.GET.get('preco_max'),
        'ordenar': request.GET.get('ordenar'),
        'produtos_promocao': produtos_promocao,
    }

    return render(request, 'shop-grid.html', context)

def visualizar_detalhe_produto (request, categoria_slug, produto_slug, departamento_slug):
    produto = Produto.objects.get(slug = produto_slug, categoria__slug = categoria_slug)
    context = {
        'produto': produto,
    }

    return render(request, 'shop-details.html', context)
    
def calcular_frete(request):
    cep = request.GET.get('cep')

    if not cep or len(cep) != 8:
        return JsonResponse({'erro': 'CEP inválido'}, status=400)

    try:
        response = requests.get(f'https://viacep.com.br/ws/{cep}/json/')
        data = response.json()
        
        if data.get('erro'):
            return JsonResponse({'erro': 'CEP não encontrado'}, status=404)
        
        uf = data.get('uf', '')

        precos_frete = {
            'SP': 10.0,
            'RJ': 12.0,
            'MG': 14.0,
            'RS': 18.0,
            'MT': "Gratis",
            'DEFAULT': 25.0,
        }
        
        valor = precos_frete.get(uf, precos_frete['DEFAULT'])
        if isinstance(valor, (int,float)):
            valor_formatado = f'R${valor:.2f}'
        else:
            valor_formatado = str(valor)
            
        return JsonResponse({'valor_frete': valor_formatado, 'uf': uf})
    except Exception:
        return JsonResponse({'erro': 'Erro ao consultar o CEP'}, status=500)

def filtrar_produtos(request, queryset):
    preco_min = request.GET.get('preco_min')
    preco_max = request.GET.get('preco_max')
    ordenar = request.GET.get('ordenar')

    if preco_min:
        queryset = queryset.filter(preco__gte=preco_min)
    if preco_max:
        queryset = queryset.filter(preco__lte=preco_max)

    queryset = queryset.annotate(
        preco_efetivo=ExpressionWrapper(
            Case(
                When(
                    promocao_disponivel=True,
                    then=F('preco') * (Value(1) - F('promocao_valor_porcentagem') / Value(100.0))
                ),
                default=F('preco'),
                output_field=DecimalField(max_digits=10, decimal_places=2)
            ),
            output_field=DecimalField(max_digits=10, decimal_places=2)
        )
    )

    if ordenar == 'preco_crescente':
        queryset = queryset.order_by('preco_efetivo')
    elif ordenar == 'preco_decrescente':
        queryset = queryset.order_by('-preco_efetivo')
    else:
        queryset = queryset.order_by('produto_nome')


    paginator = Paginator(queryset, 9)
    pagina_num = request.GET.get('pagina')
    produtos = paginator.get_page(pagina_num)

    return produtos, paginator

    