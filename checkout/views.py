from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Pedido, ItemPedido

from carrinho.models import CarItem
from carrinho.views import _get_or_create_carrinho

@login_required
def checkout_view(request):
    # 1. Obter o carrinho e os itens do carrinho
    carrinho = _get_or_create_carrinho(request)
    car_items = CarItem.objects.filter(carrinho=carrinho, esta_disponivel=True)

    if not car_items.exists():
        messages.warning(request, "Seu carrinho está vazio.")
        return redirect('carrinho')

    # 2. Calcular totais (lógica similar à sua view 'visualizarCarrinho')
    subtotal = 0
    valor_imposto = 0
    for item in car_items:
        subtotal += item.getSubTotal()
        valor_imposto += item.getSubTotal() * (item.produto.imposto / 100)

    valor_total = subtotal + valor_imposto
    # Adicionar lógica de frete aqui se necessário
    
    if request.method == 'POST':
        # 3. Processar o formulário quando enviado
        
        # 4. Criar o objeto Pedido
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
            
            # Use os valores calculados no servidor, NUNCA do formulário
            subtotal=subtotal,
            valor_imposto=valor_imposto,
            valor_total=valor_total,
            # valor_frete=... # Adicione se tiver
        )
        pedido.save() # Salva o pedido para obter um ID

        # 5. Criar os Itens do Pedido (ItemPedido)
        for item in car_items:
            ItemPedido.objects.create(
                pedido=pedido,
                produto=item.produto,
                preco_item=item.produto.preco_com_desconto(), # Use o preço efetivo (com promoção)
                quantidade=item.quantidade
            )

        # 6. Limpar o carrinho (deletando os CarItem)
        car_items.delete()

        return JsonResponse({
            'status': 'success',
            'message': 'Pedido criado com sucesso! Aguardando pagamento.'
        })

    # Se for um GET, apenas renderiza a página com os dados
    context = {
        'car_items': car_items,
        'subtotal': subtotal,
        'valor_imposto': valor_imposto,
        'valor_total': valor_total,
    }
    return render(request, 'loja/checkout.html', context)