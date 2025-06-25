from django.shortcuts import get_object_or_404, redirect, render

from carrinho.models import CarItem, Carrinho
from django.core.exceptions import ObjectDoesNotExist

from produto.models import Produto

# Create your views here.

def getCarId(request):
    carSession = request.session.session_key
    if not carSession:
        carSession = request.session.create()
    return carSession

def visualizarCarrinho(request, total = 0, quantidade = 0, car_items = None, imposto = 0, total_com_imposto = 0):
    try:
        car = Carrinho.objects.get(car_id = getCarId(request))
        car_items = CarItem.objects.filter(carrinho = car, esta_disponivel = True)
        for item in car_items:
            if item.produto.promocao_disponivel and item.produto.promocao_valor_porcentagem > 0:
                total += (item.produto.preco_com_desconto() * item.quantidade)
                imposto += (item.produto.preco_com_desconto() * item.quantidade) * (item.produto.imposto/100)
            else:
                total += (item.produto.preco * item.quantidade)
                imposto += (item.produto.preco * item.quantidade) * (item.produto.imposto/100)
            total_com_imposto = total + imposto
            quantidade += item.quantidade
    except ObjectDoesNotExist:
        pass
    
    context = {
        'imposto': imposto,
        'total': total,
        'total_com_imposto': total_com_imposto,
        'car_items': car_items,
    }
    
    return render(request, 'shoping-cart.html', context)

def adicionarItemCarrinho(request, produto_id):
    produto = Produto.objects.get(id=produto_id)
    quantidade = int(request.POST.get('quantidade', 1))
    try:
        carrinho = Carrinho.objects.get(car_id = getCarId(request))
    except Carrinho.DoesNotExist:
        carrinho = Carrinho.objects.create(
            car_id = getCarId(request)
        )
    carrinho.save()

    try:
        car_item = CarItem.objects.get(produto=produto, carrinho=carrinho)
        car_item.quantidade += quantidade
        car_item.save()
    except CarItem.DoesNotExist:
        car_item = CarItem.objects.create(
            produto = produto,
            quantidade = quantidade,
            carrinho = carrinho,
        )
        car_item.save()
    return redirect('carrinho')

def diminuirQuantidadeProdutoCarrinho(request, produto_id):
    car = Carrinho.objects.get(car_id = getCarId(request))
    produto = get_object_or_404(Produto, id=produto_id)
    car_item = CarItem.objects.get(produto=produto, carrinho=car)
    if car_item.quantidade > 1:
        car_item.quantidade -= 1
        car_item.save()
    else:
        car_item.delete()
    return redirect('carrinho')

def removerItemCarrinho(request, produto_id):
    car = Carrinho.objects.get(car_id = getCarId(request))
    produto = get_object_or_404(Produto, id=produto_id)
    car_item = CarItem.objects.get(produto=produto, carrinho=car)
    if car_item.quantidade >= 1:
        car_item.delete()
    return redirect('carrinho')