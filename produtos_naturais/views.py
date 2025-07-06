from django.shortcuts import render

from categoria.models import Categoria
from departamento.models import Departamento
from produto.models import Produto

from django.db.models import *

def home(request):
    produto = Produto.objects.all().filter(esta_disponivel=True)
    categorias_com_produtos = Categoria.objects.annotate(
        num_produtos=Count('produto', filter=Q(produto__esta_disponivel=True))
    ).filter(num_produtos__gt=0)
    
    categorias_aleatorias = categorias_com_produtos.order_by('?')[:3]
    
    produto_destaque = []
    
    for categoria in categorias_aleatorias:
        produto = Produto.objects.filter(
            esta_disponivel=True,
            categoria=categoria
        ).annotate(
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
        ).order_by('?')[:4]
        
        produto_destaque.extend(produto)

    
    context = {
        'produto': produto,
        'produto_destaque': produto_destaque,
        'opcoes_cat_random': categorias_aleatorias,
        'departamentos': Departamento.objects.all(),
    }
    
    return render(request, 'loja/index.html', context)