# carrinho/views.py
from django.shortcuts import get_object_or_404, redirect, render
from .models import CarItem, Carrinho
from produto.models import Produto

def _get_or_create_carrinho(request):
    if request.user.is_authenticated:
        carrinho, _ = Carrinho.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            session_key = request.session.create()
        carrinho, _ = Carrinho.objects.get_or_create(car_id=session_key)
    return carrinho

def visualizarCarrinho(request, total=0, quantidade=0, imposto=0, total_com_imposto=0):
    car_items = []
    try:
        carrinho = _get_or_create_carrinho(request)
        car_items = CarItem.objects.filter(carrinho=carrinho, esta_disponivel=True)
        for item in car_items:
            total += item.getSubTotal()
            imposto += item.getSubTotal() * (item.produto.imposto / 100)
            quantidade += item.quantidade
        total_com_imposto = total + imposto
    except Carrinho.DoesNotExist:
        pass  # Se o carrinho não existe, as listas ficarão vazias

    context = {
        'imposto': imposto,
        'total': total,
        'total_com_imposto': total_com_imposto,
        'car_items': car_items,
    }
    return render(request, 'loja/shoping-cart.html', context)

def adicionarItemCarrinho(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    quantidade = int(request.POST.get('quantidade', 1))
    carrinho = _get_or_create_carrinho(request)

    try:
        car_item = CarItem.objects.get(produto=produto, carrinho=carrinho)
        car_item.quantidade += quantidade
        car_item.save()
    except CarItem.DoesNotExist:
        car_item = CarItem.objects.create(
            produto=produto,
            quantidade=quantidade,
            carrinho=carrinho,
        )
    return redirect('carrinho')

def diminuirQuantidadeProdutoCarrinho(request, produto_id):
    carrinho = _get_or_create_carrinho(request)
    produto = get_object_or_404(Produto, id=produto_id)
    try:
        car_item = CarItem.objects.get(produto=produto, carrinho=carrinho)
        if car_item.quantidade > 1:
            car_item.quantidade -= 1
            car_item.save()
        else:
            car_item.delete()
    except CarItem.DoesNotExist:
        pass
    return redirect('carrinho')

def removerItemCarrinho(request, produto_id):
    carrinho = _get_or_create_carrinho(request)
    produto = get_object_or_404(Produto, id=produto_id)
    CarItem.objects.filter(produto=produto, carrinho=carrinho).delete()
    return redirect('carrinho')