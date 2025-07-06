# checkout/views.py

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages

from .models import ItemPedido
from carrinho.models import CarItem
from carrinho.views import _get_or_create_carrinho
from .forms import PedidoForm

def checkout_view(request):
    if not request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'unauthenticated'}, status=403)
        return redirect('login')

    carrinho = _get_or_create_carrinho(request)
    car_items = CarItem.objects.filter(carrinho=carrinho, esta_disponivel=True)

    if not car_items.exists():
        messages.warning(request, "Seu carrinho está vazio.")
        return redirect('carrinho')

    subtotal = sum(item.getSubTotal() for item in car_items)
    valor_imposto = sum(item.getSubTotal() * (item.produto.imposto / 100) for item in car_items)
    valor_total = subtotal + valor_imposto

    if request.method == 'POST':
        # 1. Crie uma instância do formulário com os dados do POST
        form = PedidoForm(request.POST)

        # 2. Valide o formulário
        if form.is_valid():
            # 3. Use commit=False para criar o objeto em memória sem salvar no DB
            pedido = form.save(commit=False)

            # 4. Adicione os dados que não vieram do formulário
            pedido.user = request.user
            pedido.subtotal = subtotal
            pedido.valor_imposto = valor_imposto
            pedido.valor_total = valor_total
            
            # 5. Agora salve o objeto Pedido completo no DB
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
                'order_id': pedido.id,
                'message': 'Pedido criado com sucesso! Aguardando pagamento.'
            })
        else:
            return JsonResponse({
                'status': 'error',
                'errors': form.errors
            }, status=400) # status 400 indica uma "Bad Request"

    # GET request
    context = {
        'car_items': car_items,
        'subtotal': subtotal,
        'valor_imposto': valor_imposto,
        'valor_total': valor_total,
    }
    return render(request, 'loja/checkout.html', context)