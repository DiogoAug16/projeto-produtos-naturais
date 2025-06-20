
from carrinho.models import CarItem, Carrinho
from carrinho.views import getCarId


def contador(request):
    contador = 0
    try:
        car = Carrinho.objects.filter(car_id = getCarId(request))
        car_items = CarItem.objects.all().filter(carrinho=car[:1])

        for car_item in car_items:
            contador += car_item.quantidade
    except Carrinho.DoesNotExist:
        contador = 0
    return dict(car_contador = contador)

def valorTotalCarrinho(request):
    total = 0
    imposto = 0
    
    try:
        car = Carrinho.objects.filter(car_id=getCarId(request))
        car_items = CarItem.objects.all().filter(carrinho=car[:1])

        for car_item in car_items:
            if car_item.produto.promocao_disponivel and car_item.produto.promocao_valor_porcentagem > 0:
                total += car_item.produto.preco_com_desconto() * car_item.quantidade
                imposto += (car_item.produto.preco_com_desconto() * car_item.quantidade) * (car_item.produto.imposto/100)
            else:
                total += car_item.produto.preco * car_item.quantidade   
                imposto += (car_item.produto.preco * car_item.quantidade) * (car_item.produto.imposto/100)
        total_com_imposto = total + imposto
    except Carrinho.DoesNotExist:
        total = 0
        imposto = 0
    return dict(valor_total_carrinho=total_com_imposto)