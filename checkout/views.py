from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages

from .models import Pedido, ItemPedido
from carrinho.models import CarItem
from carrinho.views import _get_or_create_carrinho

def checkout_view(request):
    # Verifica se o usuário está autenticado
    if not request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'unauthenticated'}, status=403)
        return redirect('login')

    # 1. Obter o carrinho e os itens do carrinho
    carrinho = _get_or_create_carrinho(request)
    car_items = CarItem.objects.filter(carrinho=carrinho, esta_disponivel=True)

    if not car_items.exists():
        messages.warning(request, "Seu carrinho está vazio.")
        return redirect('carrinho')

    # 2. Calcular totais
    subtotal = 0
    valor_imposto = 0
    for item in car_items:
        subtotal += item.getSubTotal()
        valor_imposto += item.getSubTotal() * (item.produto.imposto / 100)

    valor_total = subtotal + valor_imposto

    # 3. Processar pedido
    if request.method == 'POST':
        pedido = Pedido(
            user=request.user,
            nome=request.POST.get('nome'),
            sobrenome=request.POST.get('sobrenome'),
            endereco=request.POST.get('endereco'),
            numero_endereco=request.POST.get('numero_endereco'),
            complemento_endereco=request.POST.get('complemento_endereco'),
            estado=request.POST.get('estado'),
            cidade=request.POST.get('cidade'),
            cep=request.POST.get('cep'),
            telefone=request.POST.get('telefone'),
            cpf=request.POST.get('cpf'),
            metodo_pagamento=request.POST.get('metodo_pagamento'),
            subtotal=subtotal,
            valor_imposto=valor_imposto,
            valor_total=valor_total,
        )
        pedido.save()

        for item in car_items:
            ItemPedido.objects.create(
                pedido=pedido,
                produto=item.produto,
                preco_item=item.produto.preco_com_desconto(),
                quantidade=item.quantidade
            )

        car_items.delete()

        return JsonResponse({
            'status': 'success',
            'message': 'Pedido criado com sucesso! Aguardando pagamento.'
        })

    # GET
    context = {
        'car_items': car_items,
        'subtotal': subtotal,
        'valor_imposto': valor_imposto,
        'valor_total': valor_total,
    }
    return render(request, 'loja/checkout.html', context)