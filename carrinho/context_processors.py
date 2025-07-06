# carrinho/context_processors.py

from .models import CarItem, Carrinho
from favoritos.models import FavItem, Favoritos

def menu_context(request):
    """
    Um único context processor para fornecer os contadores do carrinho e favoritos,
    e o valor total do carrinho para todas as páginas.
    """
    car_contador = 0
    fav_contador = 0
    valor_total_carrinho = 0.0

    if 'admin' in request.path:
        return {}

    try:
        if request.user.is_authenticated:
            try:
                carrinho = Carrinho.objects.get(user=request.user)
                car_items = CarItem.objects.filter(carrinho=carrinho)
            except Carrinho.DoesNotExist:
                car_items = CarItem.objects.none()

            try:
                favoritos = Favoritos.objects.get(user=request.user)
                fav_items = FavItem.objects.filter(favoritos=favoritos)
            except Favoritos.DoesNotExist:
                fav_items = FavItem.objects.none()
        else:
            session_key = request.session.session_key
            if session_key:
                try:
                    carrinho = Carrinho.objects.get(car_id=session_key)
                    car_items = CarItem.objects.filter(carrinho=carrinho)
                except Carrinho.DoesNotExist:
                    car_items = CarItem.objects.none()

                try:
                    favoritos = Favoritos.objects.get(fav_id=session_key)
                    fav_items = FavItem.objects.filter(favoritos=favoritos)
                except Favoritos.DoesNotExist:
                    fav_items = FavItem.objects.none()
            else:
                car_items = CarItem.objects.none()
                fav_items = FavItem.objects.none()

        total = 0
        imposto = 0
        for item in car_items:
            car_contador += item.quantidade
            subtotal = item.getSubTotal()
            total += subtotal
            imposto += subtotal * (item.produto.imposto / 100)
        valor_total_carrinho = total + imposto
        
        fav_contador = fav_items.count()

    except Exception:
        pass

    return {
        'car_contador': car_contador,
        'fav_contador': fav_contador,
        'valor_total_carrinho': valor_total_carrinho,
    }